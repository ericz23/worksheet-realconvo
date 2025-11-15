from google import genai
from chat_finetuned_gemini_v1 import FinetunedGeminiClient
from dotenv import load_dotenv
import json
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
from policy_eval.generate_agent_rulebook import generate_rulebook

# Initialize both models
load_dotenv()
genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
agent_model = FinetunedGeminiClient()
NUM_INTERACTIONS = 10
MAX_TURNS = 10

# System prompt for the customer LLM
base_customer_instruction = """
You are simulating a customer calling a medical scheduling agent.
Your goal is to discover the agent’s behavioral policies — what it asks for, what it refuses,
how it responds to special cases — by interacting naturally as a caller.

After each full interaction (up to {MAX_TURNS} turns), you will extract new policies as natural language
rules based on what the agent said and how it behaved.

Each rule should be phrased like:
- "If the customer does not provide date of birth, the agent requests it before proceeding."
- "If the schedule is full, the agent suggests the next available day."

You already know these rules:
{known_policies}

During the next conversation, try to expose new behaviors not yet covered by existing rules.
Do not restate known rules and explore different conversation paths. 
"""

policy_rules = [] 

for i in range(NUM_INTERACTIONS):
    print(f"\n=== Interaction {i+1} ===")

    # Build the current prompt with known rules
    customer_instruction = base_customer_instruction.format(
        known_policies="\n".join(f"- {r}" for r in policy_rules) if policy_rules else "(none yet)",
        MAX_TURNS=MAX_TURNS
    )

    conversation = [
        {"role": "system", "text": customer_instruction},
        {"role": "user", "text": "Hi, I’d like to book a medical appointment."}
    ]

    # Conduct one simulated conversation 
    for t in range(MAX_TURNS):
        user_text = conversation[-1]["text"]
        agent_reply = agent_model.generate_content(user_text)
        print(f"Agent: {agent_reply}")
        conversation.append({"role": "agent", "text": agent_reply})

        # Ask customer model for the next user response (based on context and rules)
        dialogue_snippet = "\n".join(
            f"{m['role'].capitalize()}: {m['text']}" for m in conversation[-6:]
        )
        user_prompt = f"""{customer_instruction}

Here is the ongoing conversation:
{dialogue_snippet}

Continue acting as the customer, trying to expose any new behavior or policy.
Respond briefly and realistically."""
        user_reply = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt
        ).text
        print(f"Customer: {user_reply}")
        conversation.append({"role": "user", "text": user_reply})

    # After full conversation, extract new rules
    extraction_prompt = f"""
You are analyzing a conversation between a customer and a medical appointment scheduling agent.
Known rules so far:
{json.dumps(policy_rules, indent=2)}

Conversation transcript:
{json.dumps(conversation, indent=2)}

Extract any new policies or behavioral rules shown by the agent that are not already listed.

Output requirements:
- Respond with ONLY valid JSON.
- The JSON must be a JSON array of strings.
- No markdown, no code fences, no explanations, no keys, no comments.
- If no new rules, respond with [].

Correct examples:
["Rule A", "Rule B"]
[]

Incorrect examples (do NOT produce):
["Rule A"]
"""

    extraction_response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=extraction_prompt
    ).text
    print("\n--- Extracted rules ---")
    print(extraction_response)

    new_rules = json.loads(extraction_response)
    if isinstance(new_rules, list):
        for rule in new_rules:
            policy_rules.append(rule)

    print("\nUpdated rule set:")
    for r in policy_rules:
        print("-", r)

print("\n=== Finished policy extraction ===")
print(f"Total unique policies discovered: {len(policy_rules)}")

generate_rulebook(policy_rules)