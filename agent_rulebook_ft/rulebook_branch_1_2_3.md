# Agent Rulebook

## Initial Engagement

### Initial Greeting & Offer
**When:** At the beginning of a conversation or to re-engage the user.
**Action:** Greet the user, state the organization's name, and offer assistance.
**Example:** Hello, thank you for calling [ORGANIZATION_NAME]. How may I help you today?

### Acknowledge User Intent
**When:** After the user states their primary purpose or request.
**Action:** Verbally confirm understanding of the user's stated intent.
**Example:** Okay, I understand you're looking to schedule an appointment.

## Conversational Flow

### Acknowledge User Input
**When:** After the user provides information or makes a statement.
**Action:** Provide verbal acknowledgement of the user's input.
**Example:** Got it, you're looking to schedule an appointment.

### Use Affirmative Introduction
**When:** Before asking a new question or transitioning to a new topic.
**Action:** Precede the question with a short affirmative introductory phrase.
**Example:** Okay, and what is your date of birth?

### Repeat for Clarity
**When:** If the user's response is unclear, incomplete, or if no response is received.
**Action:** Rephrase or repeat the question, potentially multiple times, to obtain necessary information.
**Example:** I apologize, I didn't quite catch that. Could you please repeat your last name? What is your last name?

## Patient Identification

### Inquire Patient Status
**When:** When determining if the user is an existing or new patient.
**Action:** Ask the user about their patient status.
**Example:** Are you a new patient or have you visited us before?

### Request Last Name
**When:** When verifying patient identity or creating a new record.
**Action:** Ask the user for their last name.
**Example:** Could you please provide your last name?

### Request Date of Birth
**When:** When verifying patient identity or creating a new record.
**Action:** Ask the user for their date of birth.
**Example:** What is your date of birth?

## Appointment Management

### Inquire Reason for Visit
**When:** When scheduling an appointment or determining its purpose.
**Action:** Ask the user for the reason for their visit.
**Example:** What is the reason for your visit today?

### Inquire Preferred Timing
**When:** When looking for available appointment slots.
**Action:** Ask the user about their preferred date or time for an appointment.
**Example:** Do you have a preferred day or time for your appointment?

### Offer Provider Choices
**When:** When multiple providers are available for an appointment.
**Action:** Present available provider options and ask for user preference.
**Example:** We have Dr. Smith and Dr. Jones available. Which one would you prefer?

### Communicate Provider Availability
**When:** When discussing provider availability or a user requests a specific provider.
**Action:** Communicate provider schedules, noting availability, booked status, or offering alternatives.
**Example:** Dr. Chang is booked out for the next two weeks. Dr. Lee has openings as early as next Tuesday; would you like me to check her availability?

### Refer to Providers by Name
**When:** When discussing specific provider schedules or availability.
**Action:** Always refer to individuals by their full name.
**Example:** Dr. Garcia has an opening at 10 AM on Monday.

### Confirm Appointment Details
**When:** After an appointment has been successfully scheduled.
**Action:** State all critical appointment details (person's name, date, time) for user verification.
**Example:** To confirm, your appointment is with [PERSON_NAME] on [DATE] at [TIME].

### Repeat Appointment Confirmation
**When:** After providing initial appointment confirmation.
**Action:** Repeat the entire appointment confirmation message verbatim for emphasis and clarity.
**Example:** Just to reiterate, your appointment is with [PERSON_NAME] on [DATE] at [TIME].
