import os
import sys
import json
from dotenv import load_dotenv
from google import genai
import psycopg2
from pgvector.psycopg2 import register_vector
from pydantic import BaseModel
from typing import List

import asyncio

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
You are analyzing behavior of a scheduling agent.

You should use the given past examples of similar interactions to produce STRICTLY a JSON response with a "responses" key containing an array of exactly 2 different response objects.

Each response object should have 3 keys:
1. "simulated_agent_response": the agent's most reasonable next reply based on the examples and behavior style.
2. "inferred_policies": a list of short natural-language rules inferred ONLY from the examples. Do not invent new behavior outside what examples imply.
3. "new_customer_message": a short customer follow-up message that tries to expose or challenge new agent behavior.

Generate TWO different versions to explore different possible agent behaviors and customer responses based on the examples.

Past examples of the agent's behavior:
{ex_text}

Current conversation:
{conv_text}

Respond with strict JSON containing exactly 2 response variations.
"""

class ResponseFormat(BaseModel):
    simulated_agent_response: str
    inferred_policies: List[str]
    new_customer_message: str

class MultipleResponses(BaseModel):
    responses: List[ResponseFormat]

def main():
    load_env()
    gem = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    conn = get_db_connection()
    ensure_vector_extension(conn)
    register_vector(conn)

    NUM_TURNS = 10
    TOP_K = 5

    starting_conversation = [
        {"role": "agent", "text": "Thank you for calling [ORGANIZATION]. How can I assist you today?"},
        {"role": "user", "text": "Hi, I’d like to book a medical appointment."}
    ]

    all_conversations = []
    all_policy_sets = []
    
    def branching_exploration(curr_conv, curr_policies):
        if len(curr_conv) >= NUM_TURNS:
            all_conversations.append({"conversation": curr_conv.copy(), "policies": curr_policies.copy()})
            all_policy_sets.append(curr_policies.copy())
            return
        
        turn_index = len(curr_conv)
        query_context = "\n".join(f"{m['role']}: {m['text']}" for m in curr_conv)
        examples = retrieve_top_k_examples(conn, query_context, turn_index, TOP_K)
        prompt = build_llm_poke_prompt(curr_conv, examples)

        result = gem.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"response_mime_type": "application/json", "response_json_schema": MultipleResponses.model_json_schema()}
        )
        output = MultipleResponses.model_validate_json(result.text)

        count = 0

        for response in output.responses:
            count += 1
            if count > 2:
                break
            new_conv = curr_conv.copy()
            new_conv.append({"role": "agent", "text": response.simulated_agent_response})
            new_conv.append({"role": "user", "text": response.new_customer_message})
            new_policies = curr_policies.copy()
            new_policies.extend(response.inferred_policies)
            branching_exploration(new_conv, new_policies)
    
    branching_exploration(starting_conversation, [])
    conn.close()
    
    os.makedirs("agent_rulebook_db", exist_ok=True)
    os.makedirs("conversation_branches", exist_ok=True)
    
    with open("conversation_branches/all_conversations.json", "w") as f:
        json.dump(all_conversations, f, indent=2)
    
    for i, policies in enumerate(all_policy_sets):
        unique_policies = list(dict.fromkeys(policies))
        generate_rulebook(unique_policies, output_path=f"agent_rulebook_db/rulebook_branch_{i+1}.md")


if __name__ == "__main__":
    main()