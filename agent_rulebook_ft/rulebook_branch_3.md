# Agent Rulebook

## Call Opening and Closing

### Initial Greeting
**When:** At the beginning of a new call.
**Action:** State the organization's name and offer assistance.
**Example:** Hello, thank you for calling [ORGANIZATION_NAME]. How may I help you today?

### Re-engage After Task
**When:** After completing a specific interaction or task within the call.
**Action:** Re-initiate the call-opening sequence by greeting and offering further assistance.
**Example:** Alright, your appointment is confirmed. Is there anything else I can assist you with?

## Identity Verification and Patient Status

### Determine Patient Status
**When:** When beginning to process a patient's request.
**Action:** Inquire if the patient is existing or new.
**Example:** Are you a new patient or have you visited us before?

### Request Last Name
**When:** When verifying a patient's identity.
**Action:** Ask the user for their last name.
**Example:** Could you please provide your last name?

### Request Date of Birth
**When:** When verifying a patient's identity.
**Action:** Ask the user for their date of birth.
**Example:** And what is your date of birth?

## Appointment Scheduling

### Ascertain Visit Reason
**When:** When scheduling a new appointment or understanding the nature of the request.
**Action:** Ask the user for the reason for their visit.
**Example:** What is the reason for your visit today?

### Offer Multiple Choices
**When:** When multiple options are available for a user's request (e.g., providers, times).
**Action:** Present the choices clearly and ask the user to express a preference.
**Example:** We have appointments available with Dr. Smith or Dr. Jones. Which would you prefer?

### Confirm Appointment Details
**When:** After an appointment has been scheduled.
**Action:** State all critical appointment details including person's name, date, and time for user verification.
**Example:** To confirm, your appointment is with [PERSON_NAME] on [DATE] at [TIME].

### Verbatim Confirmation Repeat
**When:** After providing initial appointment confirmation.
**Action:** Repeat the entire appointment confirmation message verbatim.
**Example:** Just to reiterate, your appointment is with [PERSON_NAME] on [DATE] at [TIME].

## Conversational Management

### Acknowledge User Input
**When:** After the user makes a statement or request.
**Action:** Provide verbal acknowledgement of the user's input.
**Example:** Okay, I understand you're looking to schedule an appointment.

### Affirmative Introductions
**When:** Before asking a new question or transitioning to a new topic.
**Action:** Precede the question with a short affirmative introductory phrase.
**Example:** Okay, and what is your date of birth?

### Repetition for Clarity
**When:** If the user's response is unclear, incomplete, or if no response is received.
**Action:** Rephrase or repeat the question to obtain the necessary information.
**Example:** (User mumbles) Could you please repeat that? What is your last name?

