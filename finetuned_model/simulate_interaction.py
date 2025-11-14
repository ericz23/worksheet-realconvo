from vertexai.generative_models import GenerativeModel
from chat_finetuned_gemini_v1 import FinetunedGeminiClient
from dotenv import load_dotenv
import json

# Initialize both models
load_dotenv()
customer_model = GenerativeModel("gemini-2.5-flash")
agent_model = FinetunedGeminiClient()

# System prompt for the customer LLM
base_customer_instruction = """
You are simulating a customer calling a medical scheduling agent.
Your goal is to discover the agent’s behavioral policies — what it asks for, what it refuses,
how it responds to special cases — by interacting naturally as a caller.

After each full interaction (up to 10 turns), you will extract new policies as natural language
rules based on what the agent said and how it behaved.

Each rule should be phrased like:
- "If the customer does not provide date of birth, the agent requests it before proceeding."
- "If the schedule is full, the agent suggests the next available day."

You already know these rules:
{known_policies}

During the next conversation, try to expose new behaviors not yet covered by existing rules.
Do not restate known rules.
"""

policy_rules = [] 
NUM_INTERACTIONS = 5
MAX_TURNS = 10

for i in range(NUM_INTERACTIONS):
    print(f"\n=== Interaction {i+1} ===")

    # Build the current prompt with known rules
    customer_instruction = base_customer_instruction.format(
        known_policies="\n".join(f"- {r}" for r in policy_rules) if policy_rules else "(none yet)"
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
        user_reply = customer_model.generate_content(user_prompt).text
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

    extraction_response = customer_model.generate_content(extraction_prompt).text
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