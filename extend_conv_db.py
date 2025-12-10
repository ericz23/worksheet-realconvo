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

You will:
1) Generate the agent's SINGLE next reply to continue the conversation.
2) Infer ONLY the new policies that are implied by THIS NEW REPLY ALONE.

CRITICAL RULES:
- "inferred_policies" must capture behavior that is NEWLY REVEALED by the reply you generate.
- Do NOT include generic policies about asking if the patient is new, insurance, PPO/HMO, etc. unless they are expressed for the first time in THIS new reply.
- Do NOT restate or summarize behaviors that were already clearly implied by earlier turns in the conversation or by the examples.
- If the new reply does not introduce any new behavior, return an empty list for "inferred_policies".

You must respond with STRICT JSON containing:
- "simulated_agent_response": the agent's most reasonable next reply based on the examples and behavior style.
- "inferred_policies": a list of short natural-language rules that are newly implied only by this reply.

Past examples of the agent's behavior:
{ex_text}

Current conversation so far:
{conv_text}

Respond with strict JSON.
"""

def build_single_client_response_prompt(conversation, examples):
    conv_text = "\n".join(f"{m['role'].capitalize()}: {m['text']}" for m in conversation)
    ex_text = "\n\n".join([f"Context:\n{e['prev']}\nClient reply:\n{e['reply']}" for e in examples])
    return f"""
You are generating a single realistic client response for a scheduling conversation.

You are given real examples of client replies as references. Use them to stay realistic, but you should primarily optimize for:
- answering the agent's questions
- moving the scheduling process forward
- staying consistent with the conversation so far.

IMPORTANT:
- Generate EXACTLY ONE client response.
- Do NOT branch into multiple options.
- The response should be something that a real patient might say next.

Here are reference client responses:
{ex_text}

Current conversation:
{conv_text}

Respond with strict JSON with a single field:
- "client_response": the next client message as a string.
"""

def build_rulebook_revision_prompt(rulebook_markdown, inferred_policies):
    policies_text = "\n".join(f"- {p}" for p in inferred_policies)
    return f"""
You are a Rulebook Refiner for a medical scheduling agent.

You are given:
1) The CURRENT agent rulebook in markdown.
2) A list of newly inferred agent policies that were discovered from additional interactions.

Your tasks:

1. Reasoning & New Rules
   - Compare the inferred policies against the existing rulebook.
   - Explain step by step how these inferred policies suggest new or refined rules relative to the current rulebook.
   - For each new or refined rule, specify:
     - A short title
     - A "condition" (when this applies)
     - An "action"
     - An "example" utterance

2. Updated Rulebook
   - Using the schema (sections -> rules), produce a FULL updated rulebook that:
     - Retains all still-relevant existing rules
     - Incorporates and organizes the inferred policies into rules
     - Is organized into sections with clear names
   - Do NOT delete rules unless the inferred policies clearly contradict them; if you must merge rules, explain why in your reasoning.

Current Rulebook (markdown):
{rulebook_markdown}

Newly inferred policies:
{policies_text}

Respond with STRICT JSON with the following structure:
- "reasoning": a natural-language explanation of your thought process.
- "inferred_new_rules": a list of new or refined rules (using the Rule schema).
- "updated_rulebook": the full updated Rulebook.
"""

class SingleAgentResponse(BaseModel):
    simulated_agent_response: str
    inferred_policies: List[str]

class SingleClientResponse(BaseModel):
    client_response: str

class Rule(BaseModel):
    title: str
    condition: str
    action: str
    example: str

class Section(BaseModel):
    name: str
    rules: List[Rule]

class Rulebook(BaseModel):
    sections: List[Section]

class RulebookRevision(BaseModel):
    reasoning: str
    inferred_new_rules: List[Rule]
    updated_rulebook: Rulebook

def rulebook_to_markdown(rulebook: Rulebook) -> str:
    lines = ["# Agent Rulebook", ""]
    for section in rulebook.sections:
        lines.append(f"## {section.name}")
        lines.append("")
        for rule in section.rules:
            lines.append(f"### {rule.title}")
            lines.append(f"**When:** {rule.condition}")
            lines.append(f"**Action:** {rule.action}")
            lines.append(f"**Example:** {rule.example}")
            lines.append("")
    return "\n".join(lines).strip() + "\n"

TARGET_TURNS = 15
TOP_K = 5

async def extend_single_conversation(
    gem: genai.Client,
    conn_agent,
    conn_client,
    base_conv,
    base_policies
):
    conversation = [m.copy() for m in base_conv]
    all_policies = list(base_policies)
    new_policies = []
    is_client_turn = True
    while len(conversation) < TARGET_TURNS:
        if is_client_turn:
            query_context = "\n".join(f"{m['role']}: {m['text']}" for m in conversation)
            client_examples = await retrieve_top_k_examples_for_client(
                conn_client, query_context, len(conversation), TOP_K
            )
            client_prompt = build_single_client_response_prompt(conversation, client_examples)
            client_result = await asyncio.to_thread(
                gem.models.generate_content,
                model="gemini-2.5-flash",
                contents=client_prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": SingleClientResponse.model_json_schema()
                }
            )
            client_output = SingleClientResponse.model_validate_json(client_result.text)
            conversation.append({"role": "user", "text": client_output.client_response})
            is_client_turn = False
        else:
            query_context = "\n".join(f"{m['role']}: {m['text']}" for m in conversation)
            agent_examples = await retrieve_top_k_examples_for_agent(
                conn_agent, query_context, len(conversation), TOP_K
            )
            agent_prompt = build_agent_synthesis_prompt(conversation, agent_examples)
            agent_result = await asyncio.to_thread(
                gem.models.generate_content,
                model="gemini-2.5-flash",
                contents=agent_prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": SingleAgentResponse.model_json_schema()
                }
            )
            agent_output = SingleAgentResponse.model_validate_json(agent_result.text)
            conversation.append({"role": "agent", "text": agent_output.simulated_agent_response})
            all_policies.extend(agent_output.inferred_policies)
            new_policies.extend(agent_output.inferred_policies)
            is_client_turn = True
    return conversation, all_policies, new_policies

async def revise_single_rulebook(
    gem: genai.Client,
    rulebook_md_text: str,
    inferred_policies: List[str]
):
    dedup_policies = list(dict.fromkeys(inferred_policies))
    prompt = build_rulebook_revision_prompt(rulebook_md_text, dedup_policies)
    result = await asyncio.to_thread(
        gem.models.generate_content,
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": RulebookRevision.model_json_schema()
        }
    )
    revision = RulebookRevision.model_validate_json(result.text)
    return revision

async def main():
    load_dotenv()
    gem = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    conn_agent = get_db_connection_agent()
    conn_client = get_db_connection_client()
    ensure_vector_extension(conn_agent)
    ensure_vector_extension(conn_client)
    register_vector(conn_agent)
    register_vector(conn_client)
    with open(os.path.join("conversation_branches", "all_conversations.json"), "r") as f:
        all_conversations = json.load(f)
    extended_conversations = []
    os.makedirs("conversation_branches", exist_ok=True)
    os.makedirs("agent_rulebook_db_revised", exist_ok=True)
    os.makedirs("agent_rulebook_db_revised_json", exist_ok=True)
    for idx, entry in enumerate(all_conversations, start=1):
        base_conv = entry["conversation"]
        base_policies = entry.get("policies", [])
        extended_conv, all_policies, new_policies = await extend_single_conversation(
            gem,
            conn_agent,
            conn_client,
            base_conv,
            base_policies
        )
        extended_conversations.append({
            "conversation": extended_conv,
            "policies": all_policies
        })
        print(f"Extended turns for conversation {idx}:")
        for m in extended_conv[len(base_conv):]:
            print(f"{m['role']}: {m['text']}")
        print(f"New inferred policies for conversation {idx}:")
        for p in new_policies:
            print(f"- {p}")
        rulebook_md_path = os.path.join("agent_rulebook_db_new", f"rulebook_branch_{idx}.md")
        with open(rulebook_md_path, "r") as rb_f:
            rulebook_md_text = rb_f.read()
        revision = await revise_single_rulebook(
            gem,
            rulebook_md_text,
            new_policies
        )
        updated_rulebook = revision.updated_rulebook
        updated_md = rulebook_to_markdown(updated_rulebook)
        updated_md_path = os.path.join(
            "agent_rulebook_db_revised",
            f"rulebook_branch_{idx}.md"
        )
        with open(updated_md_path, "w") as rb_md_f:
            rb_md_f.write(updated_md)
        updated_json_path = os.path.join(
            "agent_rulebook_db_revised_json",
            f"rulebook_branch_{idx}.json"
        )
        with open(updated_json_path, "w") as rb_json_f:
            json.dump(updated_rulebook.model_dump(), rb_json_f, indent=2)
    extended_json_path = os.path.join("conversation_branches", "all_conversations_extended.json")
    with open(extended_json_path, "w") as f:
        json.dump(extended_conversations, f, indent=2)
    conn_agent.close()
    conn_client.close()
    print("Done")

if __name__ == "__main__":
    asyncio.run(main())