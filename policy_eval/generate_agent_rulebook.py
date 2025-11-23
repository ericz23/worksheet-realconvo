import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


POLICY_COMPILER_PROMPT = """
You are a Policy Compiler for a medical appointment scheduling agent.

Your job is to take a list of raw natural-language rules and produce a cleaned,
deduplicated, and sensibly ordered set of policies. The goal is clarity and completeness.

Instructions:
- Merge duplicates or near-duplicates.
- Remove contradictions or resolve them by choosing the most general consistent form.
- Keep the rules concise but precise.
- Do not create new rules; only reorganize and clean the given ones.
- Output a simple bullet list of cleaned rules.
Here are the raw rules:
"""


RULEBOOK_SYNTHESIZER_PROMPT = """
You are a Rulebook Synthesizer.

Given a cleaned list of agent policies, produce a short, structured, and easy-to-follow
rulebook for a medical appointment scheduling agent.

Guidelines:
- Group rules into meaningful sections (e.g. identity verification, scheduling logic, doctor preferences, insurance).
- For each rule, provide:
  * Short Rule Title
  * When: the condition
  * Action: what the agent should do
  * Example: 1 short sample response
- Keep it concise and readable.
- Do not add new rules — only organize and express clearly.

Return the rulebook in Markdown.
"""


def compile_policies(policy_rules):
    rules_text = "\n".join(f"- {r}" for r in policy_rules)
    full_prompt = POLICY_COMPILER_PROMPT + "\n" + rules_text

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    return response.text


def synthesize_rulebook(cleaned_rules):
    full_prompt = RULEBOOK_SYNTHESIZER_PROMPT + "\n\n" + cleaned_rules

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    return response.text


def generate_rulebook(policy_rules, output_path="agent_rulebook_db.md"):
    print("Compiling raw policies...")
    cleaned_rules = compile_policies(policy_rules)

    print("\nSynthesizing rulebook...")
    rulebook = synthesize_rulebook(cleaned_rules)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rulebook)

    print(f"\nRulebook saved to {output_path}")

def normalize_bullet_list(raw_text):
    """
    Convert a block of '- ' bullet-point lines into a
    clean Python list of strings (without the '- ' prefix).
    """
    lines = raw_text.strip().split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()
        if line.startswith("- "):
            cleaned.append(line[2:].strip())
        elif line:  # fallback for edge cases
            cleaned.append(line)
    
    return cleaned


if __name__ == "__main__":
    policy_rules = """
    - If the customer indicates they are a new patient, the agent requests their date of birth.
- If the agent states they did not hear a previously provided piece of information, they request it again and ask for it to be spelled.
- If the customer does not have an email address, the agent offers to send new patient paperwork via text message.
- The agent requests the customer's address after gathering contact information and before discussing appointment specifics for a new patient.
- If a new patient's date of birth is not immediately provided, the agent states that an appointment cannot be booked without it.
- If the customer requests to be put on hold to retrieve necessary information, the agent agrees to the hold.
- After obtaining the date of birth for a new patient, the agent requests their first and last name.
- After obtaining the patient's name for a new patient, the agent requests a contact phone number.
- After obtaining the patient's address for a new patient, the agent requests a contact email address.
- If the customer questions the necessity of requested information, the agent explains its purpose.
- After gathering contact information for a new patient, the agent offers options to send new patient paperwork via email or text message.
- If the customer prefers to complete new patient paperwork at the office, the agent permits it but advises arriving early.
- If a new patient requests appointment availability before providing their date of birth, the agent provides the available times.
- After a new patient selects an appointment time, the agent requests their first and last name before re-requesting their date of birth.
- The agent states that for patients under a certain age, a parent or legal guardian must be present at the appointment.
- The agent permits a minor patient to provide appointment booking details, provided a guardian will accompany them to the appointment.
- If pressed for the specific age threshold for guardian presence, the agent continues to use placeholder terms.
- If the customer states they are an existing patient, the agent requests their date of birth.
- If an existing patient questions why their name is requested after selecting an appointment time, the agent states they are confirming the patient's chart.
- If the customer asks the agent to confirm information on file, the agent reads out the stored information for verification.
- If the customer expresses discomfort providing a piece of information due to incorrect records, the agent offers to use an alternative piece of information to locate their chart.
- If the customer questions the necessity of alternative verification information due to incorrect records, the agent apologizes, explains its purpose, and offers additional alternative verification options.
- If the customer indicates they might be an existing patient but state it has been a long time since their last visit, the agent requests their first and last name to search for their chart.
- If the agent cannot find an existing patient's chart using an alternative piece of information, they inform the customer of the failure and suggest possible reasons such as purging or incorrect details.
- If the agent consistently fails to locate an existing patient's chart after multiple alternative verification attempts, the agent concludes the chart is likely purged and states that a new patient chart will be created.
- If the customer asks about the nature or duration of an appointment type, the agent explains what it involves and its estimated length.
- If the customer questions the necessity of providing their date of birth and suggests providing their name first, the agent agrees to ask for the name first.
- If the customer asks about an emancipated minor, the agent states they are treated as an adult and requires emancipation documentation.
- If asked about providing emancipation documentation, the agent specifies preferred timing (before appointment) and acceptable methods of submission (email, fax, in-person with early arrival).
- If emancipation documentation is not provided or verified, the agent states that a parent or legal guardian is still required, and the appointment may need to be rescheduled if none is present.
- If the customer asks if another adult (e.g., grandparent, sibling) can accompany a minor patient, the agent explains that typically only a parent or legal guardian can provide consent, but an authorized adult may do so with a specific signed consent form.
- If the customer asks if another adult can accompany a minor, the agent offers to check the policy on authorized adults and provide a consent form.
- If the customer expresses a preference for a specific provider type or gender, the agent checks and provides availability accordingly.
- If the customer requests to be placed on a waitlist, the agent offers to add them to it.
- The agent offers the customer the option to book a placeholder appointment with another provider while being on a waitlist, and clarifies that the cancellation policy will be flexible if the customer switches to an appointment from the waitlist.
- When adding a customer to a waitlist, the agent first requests their first and last name, then specifies the duration the customer will remain on the waitlist, and then requests their date of birth.
- If the customer requests to check information or book an appointment for a second family member while in the process of booking for the first, the agent agrees to help with the second request but prioritizes completing the first booking.
- If the customer requests a specific provider and time slot that is unavailable, the agent offers alternative times with the preferred provider or alternative providers for the requested time slot.
- If the customer is booking for multiple siblings, the agent states that their contact information is typically linked in the system and confirms the shared contact details on file.
- If the customer asks about using a specific email address for paperwork for an existing patient or providing a different one, the agent requests the desired email address.
- If the customer asks about appointment preparation, the agent provides detailed information before continuing with the booking process.
- If the customer questions the purpose of their date of birth in relation to insurance verification, the agent clarifies its use for chart creation and patient identification, and states that insurance verification typically occurs later with full policy details.
- When booking an appointment for a minor, the agent states that the minor's date of birth is crucial for creating their patient chart and scheduling the appropriate appointment for their age.
- When booking an appointment for a minor, the agent states that the parent or legal guardian's information, including name, date of birth, and contact details, will also be collected as they are the responsible party for the child's care.
- When booking for a minor, the agent specifies that the parent or legal guardian's date of birth is collected after the minor's patient chart is created and their appointment is booked.
- If the customer questions the mandatory nature of the parent or legal guardian's date of birth when booking for a minor, the agent explains its importance for identity verification, insurance, legal consent, and family charting.
- The agent clarifies that while a minor's appointment can be initially booked with only the minor's date of birth, the parent or legal guardian's date of birth is required to complete the full new patient registration process.
- After a new patient selects an appointment time, the agent may request their date of birth directly without first requesting their name.
- If the customer describes symptoms, the agent asks for more details about the symptoms (e.g., new vs. old).
- If the customer describes severe symptoms or expresses concern, the agent provides advice on when to seek urgent medical care (e.g., ER visit or calling emergency services).
- If the customer asks about completing new patient paperwork online, the agent confirms it is an option and explains its benefit.
- If the customer requests to receive paperwork via text message, the agent clarifies that a mobile number is required.
- If the customer requests the new patient paperwork link, the agent states it will be sent after the appointment booking process is complete.
    """

    policy_rules = normalize_bullet_list(policy_rules)

    generate_rulebook(policy_rules)