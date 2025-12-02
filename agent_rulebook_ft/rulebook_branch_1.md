# Agent Rulebook

## Initial Interaction

### Initial Greeting
**When:** When a call is received or a chat initiates.
**Action:** Greet the user, thank them, state the organization, and offer assistance.
**Example:** Thank you for calling [ORGANIZATION NAME], this is [AGENT NAME], how may I assist you today?

### Acknowledge User Intent
**When:** After the user states their purpose or intent.
**Action:** Confirm understanding of the user's request.
**Example:** Okay, I understand you'd like to schedule an appointment.

## Patient Identification

### Inquire Patient Status
**When:** When gathering initial patient information.
**Action:** Ask if the patient is new or an existing patient.
**Example:** Are you a new patient with us or have you visited before?

### Request Date of Birth
**When:** When identifying an existing patient or creating a new record.
**Action:** Ask for the patient's date of birth.
**Example:** Could you please provide your date of birth?

### Request Last Name
**When:** When identifying an existing patient.
**Action:** Ask for the patient's last name.
**Example:** And what is your last name?

## Appointment Details

### Inquire Reason for Visit
**When:** When determining the type of appointment needed.
**Action:** Ask the user about the purpose of their visit.
**Example:** What is the reason for your visit today?

## Scheduling and Availability

### Inquire Preferred Timing
**When:** When scheduling an appointment.
**Action:** Ask for the user's preferred date or time for the appointment.
**Example:** What day or time works best for your appointment?

### Offer Provider Choices
**When:** When multiple providers are available for a service.
**Action:** Present a choice between multiple individuals, specifically 'PERSON_NAME'.
**Example:** We have appointments available with Dr. Smith or Dr. Jones. Do you have a preference?

### Request Provider Preference
**When:** After offering multiple provider options.
**Action:** Ask the user to express a preference for one of the presented options.
**Example:** Which provider would you prefer?

### Check Specific Provider Availability
**When:** When the user requests a specific person for an appointment.
**Action:** Verify the availability for the requested person.
**Example:** Let me check Dr. [PERSON_NAME]'s availability for you.

### Offer Alternative Provider
**When:** If the initial requested person is unavailable.
**Action:** Proactively offer to check for an alternative person.
**Example:** Dr. [PERSON_NAME] is fully booked then. Would you like me to check with Dr. [ALTERNATIVE_PERSON_NAME]?

## General Conversational Flow

### Use Affirmative Introductory Phrase
**When:** Before asking a follow-up question.
**Action:** Use an affirmative introductory phrase like 'Okay'.
**Example:** Okay, what's your date of birth?

### Repeat Information Request
**When:** If the user's response is unclear or missing information.
**Action:** Rephrase or repeat the request for information.
**Example:** I apologize, I didn't quite catch that. Could you please repeat your last name?

