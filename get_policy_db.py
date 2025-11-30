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


def get_db_connection_agent():
    url = os.getenv("DATABASE_URL_AGENT")
    if not url:
        raise RuntimeError("DATABASE_URL_AGENT not set")
    return psycopg2.connect(url)

def get_db_connection_client():
    url = os.getenv("DATABASE_URL_CLIENT")
    if not url:
        raise RuntimeError("DATABASE_URL_CLIENT not set")
    return psycopg2.connect(url)


def ensure_vector_extension(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()

async def retrieve_top_k_examples_for_agent(conn, query_text, turn_index, top_k):
    embedding = encode_sentences([query_text], model)[0].tolist()
    def _execute():
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
            return cur.fetchall()
    rows = await asyncio.to_thread(_execute)
    return [{"prev": r[0], "reply": r[1]} for r in rows]

async def retrieve_top_k_examples_for_client(conn, query_text, turn_index, top_k):
    embedding = encode_sentences([query_text], model)[0].tolist()
    def _execute():
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
            return cur.fetchall()
    rows = await asyncio.to_thread(_execute)
    return [{"prev": r[0], "reply": r[1]} for r in rows]


def build_agent_synthesis_prompt(conversation, examples):
    conv_text = "\n".join(f"{m['role'].capitalize()}: {m['text']}" for m in conversation)
    ex_text = "\n\n".join([f"Context:\n{e['prev']}\nAgent reply:\n{e['reply']}" for e in examples])
    return f"""
You are analyzing behavior of a scheduling agent.

You should use the given past examples of similar interactions to produce STRICTLY a JSON response with a "responses" key containing an array of exactly 1 response object.

Each response object should have 2 keys:
1. "simulated_agent_response": the agent's most reasonable next reply based on the examples and behavior style.
2. "inferred_policies": a list of short natural-language rules inferred ONLY from the examples. Do not invent new behavior outside what examples imply.

Generate ONE response based on the examples.

Past examples of the agent's behavior:
{ex_text}

Current conversation:
{conv_text}

Respond with strict JSON containing exactly 1 response.
"""

def build_client_response_prompt(conversation, examples):
    conv_text = "\n".join(f"{m['role'].capitalize()}: {m['text']}" for m in conversation)
    ex_text = "\n\n".join([f"Context:\n{e['prev']}\nClient reply:\n{e['reply']}" for e in examples])
    return f"""
You are generating client responses for a scheduling conversation.

Use the given actual client responses as references to figure out the most appropriate client responses with maximum coverage. These actual client responses are only references and you should still think about the coverage.

Generate 2 or 3 different client response options based on the examples and conversation context.

For example: if the agent asked if the pateint is new or established, the client should cover "new patient" and "established patient" in two different responses;
if the agent asks about whether the patient has PPO or HMO, the client should cover "PPO plan", "HMO plan", and "I don't know" in three different responses;
you may also consider different client tones such as providing the information eagerly, reluctantly, or refusal.

Here is the context of past examples of client responses:
{ex_text}

Current conversation:
{conv_text}

Respond on current conversation with strict JSON containing 2 or 3 client response variations.
"""

class SingleAgentResponse(BaseModel):
    simulated_agent_response: str
    inferred_policies: List[str]

class ClientResponseFormat(BaseModel):
    client_response: str

class MultipleClientResponses(BaseModel):
    responses: List[ClientResponseFormat]

async def main():
    load_dotenv()
    gem = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    conn_agent = get_db_connection_agent()
    ensure_vector_extension(conn_agent)
    register_vector(conn_agent)

    conn_client = get_db_connection_client()
    ensure_vector_extension(conn_client)
    register_vector(conn_client)

    NUM_TURNS = 11
    TOP_K = 5

    starting_conversation = [
        {"role": "agent", "text": "Thank you for calling [ORGANIZATION]. How can I assist you today?"},
        {"role": "user", "text": "Hi, I’d like to book a medical appointment."}
    ]

    conversation_count = 0
    
    os.makedirs("conversation_branches", exist_ok=True)
    with open("conversation_branches/all_conversations.json", "w") as f:
        f.write("[\n")
    
    async def branching_exploration(curr_conv, curr_policies):
        nonlocal conversation_count
        turn_num = len(curr_conv)
        conv_id = hash(str(curr_conv)) % 10000
        print(f"[Conv {conv_id}] Turn {turn_num}/{NUM_TURNS}")
        
        if len(curr_conv) >= NUM_TURNS:
            conversation_count += 1
            print(f"[Conv {conv_id}] Completed #{conversation_count}")
            
            conversation_data = {"conversation": curr_conv.copy(), "policies": curr_policies.copy()}
            with open("conversation_branches/all_conversations.json", "a") as f:
                if conversation_count > 1:
                    f.write(",\n")
                json.dump(conversation_data, f, indent=2)
                f.flush()
            
            unique_policies = list(dict.fromkeys(curr_policies))
            os.makedirs("agent_rulebook_db_new", exist_ok=True)
            generate_rulebook(unique_policies, output_path=f"agent_rulebook_db_new/rulebook_branch_{conversation_count}.md")
            return
        
        query_context = "\n".join(f"{m['role']}: {m['text']}" for m in curr_conv)
        agent_examples = await retrieve_top_k_examples_for_agent(conn_agent, query_context, len(curr_conv), TOP_K)
        agent_prompt = build_agent_synthesis_prompt(curr_conv, agent_examples)

        agent_result = await asyncio.to_thread(
            gem.models.generate_content,
            model="gemini-2.5-flash",
            contents=agent_prompt,
            config={"response_mime_type": "application/json", "response_json_schema": SingleAgentResponse.model_json_schema()}
        )
        agent_output = SingleAgentResponse.model_validate_json(agent_result.text)

        new_conv_with_agent = curr_conv.copy()
        new_conv_with_agent.append({"role": "agent", "text": agent_output.simulated_agent_response})

        new_policies_after_agent = curr_policies.copy()
        new_policies_after_agent.extend(agent_output.inferred_policies)

        if len(new_conv_with_agent) >= NUM_TURNS:
            conversation_count += 1
            print(f"[Conv {conv_id}] Completed #{conversation_count}")
            
            conversation_data = {"conversation": new_conv_with_agent.copy(), "policies": new_policies_after_agent.copy()}
            with open("conversation_branches/all_conversations.json", "a") as f:
                if conversation_count > 1:
                    f.write(",\n")
                json.dump(conversation_data, f, indent=2)
                f.flush()
            
            unique_policies = list(dict.fromkeys(new_policies_after_agent))
            os.makedirs("agent_rulebook_db_new", exist_ok=True)
            generate_rulebook(unique_policies, output_path=f"agent_rulebook_db_new/rulebook_branch_{conversation_count}.md")
            return
        
        client_query_context = "\n".join(f"{m['role']}: {m['text']}" for m in new_conv_with_agent)
        client_task = process_client_responses(conn_client, new_conv_with_agent, client_query_context, new_policies_after_agent, agent_output, TOP_K, conv_id, 0)
        
        result = await client_task
        print(f"[Conv {conv_id}] -> {len(result)} branches")
        
        for new_conv, new_policies in result:
            await branching_exploration(new_conv, new_policies)
    
    async def process_client_responses(conn_client, new_conv_with_agent, client_query_context, curr_policies, agent_response, TOP_K, conv_id, agent_idx):
        client_examples = await retrieve_top_k_examples_for_client(conn_client, client_query_context, len(new_conv_with_agent), TOP_K)
        client_prompt = build_client_response_prompt(new_conv_with_agent, client_examples)

        client_result = await asyncio.to_thread(
            gem.models.generate_content,
            model="gemini-2.5-flash",
            contents=client_prompt,
            config={"response_mime_type": "application/json", "response_json_schema": MultipleClientResponses.model_json_schema()}
        )
        client_output = MultipleClientResponses.model_validate_json(client_result.text)
        
        print(f"[Conv {conv_id}] Client responses:")
        for i, response in enumerate(client_output.responses, 1):
            print(f"  {i}. {response.client_response}")

        results = []
        for client_response in client_output.responses:
            new_conv = new_conv_with_agent.copy()
            new_conv.append({"role": "user", "text": client_response.client_response})
            new_policies = curr_policies.copy()
            new_policies.extend(agent_response.inferred_policies)
            results.append((new_conv, new_policies))
        return results
    
    await branching_exploration(starting_conversation, [])
    
    with open("conversation_branches/all_conversations.json", "a") as f:
        f.write("\n]")
    
    print(f"\nComplete. Generated {conversation_count} conversations and {conversation_count} rulebooks")
    conn_agent.close()
    conn_client.close()
    
    print("All done!")


if __name__ == "__main__":
    asyncio.run(main())