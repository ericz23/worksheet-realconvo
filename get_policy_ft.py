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
from finetuned_model.chat_finetuned_gemini_v1 import FinetunedGeminiClient

def get_db_connection_client():
    url = os.getenv("DATABASE_URL_CLIENT")
    if not url:
        raise RuntimeError("DATABASE_URL_CLIENT not set")
    return psycopg2.connect(url)


def ensure_vector_extension(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()

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


def build_client_response_prompt(conversation, examples, single_response=False):
    conv_text = "\n".join(f"{m['role'].capitalize()}: {m['text']}" for m in conversation)
    ex_text = "\n\n".join([f"Context:\n{e['prev']}\nClient reply:\n{e['reply']}" for e in examples])
    
    if single_response:
        return f"""
You are generating client responses for a scheduling conversation.

Use the given actual client responses as references to generate the most appropriate single client response.

Here is the context of past examples of client responses:
{ex_text}

Current conversation:
{conv_text}

Respond on current conversation with strict JSON containing exactly 1 client response.
"""
    
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

class ClientResponseFormat(BaseModel):
    client_response: str

class MultipleClientResponses(BaseModel):
    responses: List[ClientResponseFormat]

async def main():
    load_dotenv()
    gem = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    finetuned_client = FinetunedGeminiClient()

    conn_client = get_db_connection_client()
    ensure_vector_extension(conn_client)
    register_vector(conn_client)

    NUM_TURNS = 15
    TOP_K = 5

    starting_conversation = [
        {"role": "agent", "text": "Thank you for calling [ORGANIZATION]. How can I assist you today?"},
        {"role": "user", "text": "Hi, I’d like to book a medical appointment."}
    ]

    conversation_count = 0
    
    os.makedirs("conversation_branches_ft", exist_ok=True)
    with open("conversation_branches_ft/all_conversations.json", "w") as f:
        f.write("[\n")
    
    async def branching_exploration(curr_conv, curr_policies):
        nonlocal conversation_count
        turn_num = len(curr_conv)
        conv_id = hash(str(curr_conv)) % 10000
        print(f"[Conv {conv_id}] Turn {turn_num}/15")
        
        if len(curr_conv) >= 15:
            conversation_count += 1
            print(f"[Conv {conv_id}] Completed #{conversation_count}")
            
            conversation_data = {"conversation": curr_conv.copy(), "policies": curr_policies.copy()}
            with open("conversation_branches_ft/all_conversations.json", "a") as f:
                if conversation_count > 1:
                    f.write(",\n")
                json.dump(conversation_data, f, indent=2)
                f.flush()
            
            unique_policies = list(dict.fromkeys(curr_policies))
            os.makedirs("agent_rulebook_ft", exist_ok=True)
            generate_rulebook(unique_policies, output_path=f"agent_rulebook_ft/rulebook_branch_{conversation_count}.md")
            return
        
        for message in curr_conv:
            if message['role'] == 'user':
                finetuned_client.history.append({"role": "user", "parts": [{"text": message['text']}]})
            elif message['role'] == 'agent':
                finetuned_client.history.append({"role": "model", "parts": [{"text": message['text']}]})
        
        agent_response = await asyncio.to_thread(finetuned_client.generate_content, curr_conv[-1]['text'])

        new_conv_with_agent = curr_conv.copy()
        new_conv_with_agent.append({"role": "agent", "text": agent_response})

        new_policies_after_agent = curr_policies.copy()
        
        rulebook_content = await asyncio.to_thread(
            gem.models.generate_content,
            model="gemini-2.5-flash",
            contents=f"""Based on this agent response: "{agent_response}"
            
Generate 2-3 short natural-language policy rules that describe the agent's behavior. Return as a JSON array of strings.""",
            config={"response_mime_type": "application/json"}
        )
        try:
            inferred_policies = json.loads(rulebook_content.text)
            new_policies_after_agent.extend(inferred_policies)
        except:
            pass

        if len(new_conv_with_agent) >= 15:
            conversation_count += 1
            print(f"[Conv {conv_id}] Completed #{conversation_count}")
            
            conversation_data = {"conversation": new_conv_with_agent.copy(), "policies": new_policies_after_agent.copy()}
            with open("conversation_branches_ft/all_conversations.json", "a") as f:
                if conversation_count > 1:
                    f.write(",\n")
                json.dump(conversation_data, f, indent=2)
                f.flush()
            
            unique_policies = list(dict.fromkeys(new_policies_after_agent))
            os.makedirs("agent_rulebook_ft", exist_ok=True)
            generate_rulebook(unique_policies, output_path=f"agent_rulebook_ft/rulebook_branch_{conversation_count}.md")
            return
        
        client_query_context = "\n".join(f"{m['role']}: {m['text']}" for m in new_conv_with_agent)
        is_final_turns = len(new_conv_with_agent) >= 12
        client_task = process_client_responses(conn_client, new_conv_with_agent, client_query_context, new_policies_after_agent, TOP_K, conv_id, 0, is_final_turns)
        
        result = await client_task
        print(f"[Conv {conv_id}] -> {len(result)} branches")
        
        for new_conv, new_policies in result:
            await branching_exploration(new_conv, new_policies)
    
    async def process_client_responses(conn_client, new_conv_with_agent, client_query_context, curr_policies, TOP_K, conv_id, agent_idx, single_response=False):
        client_examples = await retrieve_top_k_examples_for_client(conn_client, client_query_context, len(new_conv_with_agent), TOP_K)
        client_prompt = build_client_response_prompt(new_conv_with_agent, client_examples, single_response)

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
            results.append((new_conv, new_policies))
        return results
    
    await branching_exploration(starting_conversation, [])
    
    with open("conversation_branches_ft/all_conversations.json", "a") as f:
        f.write("\n]")
    
    print(f"\nComplete. Generated {conversation_count} conversations and {conversation_count} rulebooks")
    conn_client.close()
    
    print("All done!")


if __name__ == "__main__":
    asyncio.run(main())