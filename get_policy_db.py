import os
import sys
import json
from dotenv import load_dotenv
from google import genai
import psycopg2
from pgvector.psycopg2 import register_vector

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from db.process_data import model, encode_sentences
from policy_eval.generate_agent_rulebook import generate_rulebook


def load_env():
    load_dotenv()


def get_db_connection():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set")
    return psycopg2.connect(url)


def ensure_vector_extension(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()


def retrieve_top_k_examples(conn, query_text, turn_index, top_k):
    embedding = encode_sentences([query_text], model)[0].tolist()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT prev_context_text, new_turn_text
            FROM appointment_turns
            WHERE abs(turn_index - %s) <= 2
            ORDER BY prev_context_embedding <=> (%s::vector)
            LIMIT %s;
            """,
            (turn_index, embedding, top_k),
        )
        rows = cur.fetchall()
    return [{"prev": r[0], "reply": r[1]} for r in rows]


def build_llm_poke_prompt(conversation, examples):
    conv_text = "\n".join(f"{m['role'].capitalize()}: {m['text']}" for m in conversation)
    ex_text = "\n\n".join([f"Context:\n{e['prev']}\nAgent reply:\n{e['reply']}" for e in examples])
    return f"""
You are analyzing behavior of a medical appointment scheduling agent.

Using the examples of past agent responses and the current conversation, produce a JSON response with 3 keys:

1. "simulated_agent_response": the agent's most reasonable next reply based on the examples and behavior style.
2. "inferred_policies": a list of short natural-language rules inferred ONLY from the examples. Do not invent new behavior outside what examples imply.
3. "new_customer_message": a short customer follow-up message that tries to expose or challenge new agent behavior.

Rules:
- Output must be pure JSON with keys exactly as specified.
- Do not include explanations, markdown, comments, or reasoning text outside JSON.

Past examples of the agent's behavior:
{ex_text}

Current conversation:
{conv_text}

Respond with strict JSON now.
"""


def main():
    load_env()
    gem = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    conn = get_db_connection()
    ensure_vector_extension(conn)
    register_vector(conn)

    NUM_TURNS = 10
    TOP_K = 5

    conversation = [
        {"role": "agent", "text": "Thank you for calling [ORGANIZATION]. How can I assist you today?"},
        {"role": "user", "text": "Hi, I’d like to book a medical appointment."}
    ]

    global_policies = []

    for t in range(2, NUM_TURNS + 2):
        query_context = "\n".join(f"{m['role']}: {m['text']}" for m in conversation)
        examples = retrieve_top_k_examples(conn, query_context, t, TOP_K)
        prompt = build_llm_poke_prompt(conversation, examples)

        result = gem.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"response_mime_type": "application/json"}
        ).text

        output = json.loads(result)

        conversation.append({"role": "agent", "text": output["simulated_agent_response"]})
        conversation.append({"role": "user", "text": output["new_customer_message"]})

        for p in output["inferred_policies"]:
            global_policies.append(p)

        print(f"\nTurn {t}")
        print("Agent:", output["simulated_agent_response"])
        print("Customer:", output["new_customer_message"])
        print("Inferred policies:", output["inferred_policies"])

    conn.close()

    global_policies = list(dict.fromkeys(global_policies))
    print("\n=== Discovered Policies ===")
    for p in global_policies:
        print("-", p)

    generate_rulebook(global_policies)


if __name__ == "__main__":
    main()