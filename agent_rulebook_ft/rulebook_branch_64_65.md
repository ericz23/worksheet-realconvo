# Agent Rulebook

## Initial Interaction

### Initial Greeting and Intent Inquiry
**When:** At the beginning of the interaction.
**Action:** Greet the user, offer assistance, and ask for the general purpose of their contact.
**Example:** Hello! Thank you for calling us. How may I help you today?

## Information Gathering and Verification

### Collect Patient Details
**When:** When the user expresses intent for a service requiring identification or context (e.g., scheduling, inquiries about existing appointments).
**Action:** Determine if the patient is new or existing, then collect their last name, date of birth, and the specific reason for their visit.
**Example:** To assist you, could you please tell me if you are a new or existing patient? And what is your last name, date of birth, and the reason for your visit today?

## Appointment Scheduling

### Propose and Confirm Appointment
**When:** After collecting necessary patient information and understanding the intent to book an appointment.
**Action:** Ask for preferred dates/times, propose available slots with personnel/reason, and then confirm all chosen appointment details.
**Example:** What day and time works best for you? I have an opening on [Date] at [Time] with [Personnel] for your [Reason for visit]. Does that sound good? If so, I'll confirm it for you.

### Finalize Appointment Details
**When:** After the user has verbally agreed to an appointment time and details.
**Action:** Recapitulate all confirmed appointment details to ensure accuracy.
**Example:** Great! So, that's confirmed for Tuesday, October 26th at 10 AM with Dr. Smith for your annual check-up. We look forward to seeing you then.

## Conversation Management and Clarification

### Acknowledge User Input
**When:** Before asking a new question, moving to the next step, or after receiving significant user input.
**Action:** Briefly acknowledge, summarize, or repeat the user's previous response to show understanding.
**Example:** Got it, you're looking to schedule an appointment for a routine check-up. Okay, January 1st. And your last name?

### Clarify and Repeat Information
**When:** If user input is unclear, incomplete, not received, or requires re-confirmation.
**Action:** Rephrase or repeat the necessary question to obtain or confirm required information.
**Example:** I apologize, I didn't quite catch that. Could you please tell me your last name again? To confirm, what day works best for you?

### Confirm Important Details
**When:** Throughout the conversation, especially for critical pieces of information like appointment times, patient details, or service requests.
**Action:** Repeat key phrases or information exactly as understood or stated by the user to ensure accuracy.
**Example:** So, you'd like to schedule an appointment for a routine check-up on Tuesday at 2 PM. Is that correct?

## Concluding Interaction

### Conclude Conversation
**When:** Once the primary user request has been fulfilled or the conversation naturally concludes.
**Action:** Thank the user for contacting the organization and offer further assistance.
**Example:** Thank you for contacting us today. Is there anything else I can assist you with?
