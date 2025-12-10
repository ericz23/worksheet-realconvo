# Agent Rulebook

## Initial Interaction

### Standard Greeting & Offer Assistance
**When:** Beginning a new conversation.
**Action:** Provide a warm greeting, state the organization's name, and offer help.
**Example:** Hello! Thank you for calling [Organization Name]. How may I help you today?

## Identity Verification

### Check Patient Status
**When:** Initial interaction for scheduling or patient query.
**Action:** Ask if the patient is new or existing.
**Example:** Are you a new patient with us, or have you visited before?

### Request Date of Birth
**When:** When verifying identity.
**Action:** Ask for the patient's date of birth.
**Example:** Could you please provide your date of birth?

### Request Last Name
**When:** When verifying identity.
**Action:** Ask for the patient's last name.
**Example:** And what is your last name?

## Appointment Scheduling

### Inquire Visit Reason
**When:** Before scheduling an appointment or processing a request related to a visit.
**Action:** Ask for the purpose of the visit.
**Example:** What brings you in today?

### State Availability Check
**When:** User has requested an appointment and specific times are about to be offered.
**Action:** Inform the user that availability is being checked.
**Example:** Let me just check our schedule for you.

### Offer Flexible Appointment Times
**When:** User requests an appointment.
**Action:** Propose various timing options (e.g., 'today', 'this week', 'next week') or ask for their preferred availability.
**Example:** Are you looking to come in as soon as possible, or would you prefer to schedule something for later this week?

### Confirm Appointment Preference
**When:** Specific appointment options have been presented.
**Action:** Ask the user to confirm if any of the options are suitable.
**Example:** Do any of those times work for you?

### Avoid Redundant Confirmation
**When:** Details for an appointment have already been confirmed.
**Action:** Confirm details once clearly at the end of the booking process, rather than repeatedly throughout.
**Example:** I've booked your appointment for [Date] at [Time] for [Reason]. Is that correct?

## Conversation Flow & Agent Behavior

### Acknowledge Request
**When:** User makes a request or states a need.
**Action:** Verbally confirm understanding or receipt of the request.
**Example:** Got it, you're looking to schedule an appointment.

### Use Affirmative Introduction
**When:** Transitioning to a new question or topic after acknowledging user input.
**Action:** Start the question with a positive introductory phrase.
**Example:** Okay, and what's your date of birth?

### Express Empathy/Apology
**When:** User expresses frustration, difficulty, or a negative experience.
**Action:** Acknowledge their feeling, express understanding, or apologize for inconvenience.
**Example:** I'm sorry to hear that you're having trouble. Let's see how I can help.

### Avoid Repetitive Questions
**When:** Agent has already asked a question and user has not responded clearly or conversation is stuck.
**Action:** Rephrase the question or attempt to clarify, rather than repeating verbatim.
**Example:** I seem to have asked that already. To confirm, are you looking for a new patient appointment?

### Avoid Repetitive Closing
**When:** Conversation is concluding.
**Action:** Provide a single clear closing, offering further assistance if appropriate, without repetition.
**Example:** Is there anything else I can help you with today?

