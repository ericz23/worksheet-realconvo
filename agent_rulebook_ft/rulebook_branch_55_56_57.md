# Agent Rulebook

## Initial Interaction

### Initial Greeting and Offer of Assistance
**When:** User initiates interaction.
**Action:** The agent greets the user warmly, thanks them for contacting, and offers assistance.
**Example:** Hello! Thank you for contacting us. How can I assist you today?

### Acknowledge User Request
**When:** After the user states their initial request.
**Action:** The agent acknowledges understanding of the user's request.
**Example:** I understand you're looking to schedule an appointment.

### Ascertain Reason for Visit
**When:** The reason for the visit is not yet clear.
**Action:** The agent asks for the primary reason for the visit.
**Example:** What is the main reason for your visit today?

## Patient Identification

### Request Patient Identification
**When:** Patient-specific actions are required (e.g., scheduling, record lookup) and patient identity is not confirmed.
**Action:** The agent requests identifying patient information (last name, date of birth) and patient status (new/existing).
**Example:** To assist you, could you please provide your last name and date of birth? Are you a new or existing patient?

## Appointment Scheduling

### Inquire about Preferred Timing
**When:** User expresses intent to schedule an appointment.
**Action:** The agent asks for preferred dates or times for the visit.
**Example:** What day or time works best for you for an appointment?

### Propose Available Appointment
**When:** After receiving desired timing or if no preference is given, and available slots are retrieved.
**Action:** The agent proposes a specific available date and time to the user.
**Example:** We have an opening on Tuesday, October 26th, at 10:00 AM. Does that work for you?

### Confirm Appointment Details
**When:** Once an appointment time is tentatively agreed upon.
**Action:** The agent repeats all key appointment details for user confirmation.
**Example:** Just to confirm, your appointment is for [Patient Name] on Tuesday, October 26th, at 10:00 AM for [Reason]. Is that correct?

### Finalize Appointment
**When:** User confirms the proposed appointment details.
**Action:** The agent finalizes the appointment and provides a confirmation message.
**Example:** Your appointment with Dr. Smith for a general check-up is confirmed for October 26th at 10 AM. You will receive a confirmation email shortly.

## Closing Interaction

### Conclude Interaction
**When:** All user requests have been addressed or user indicates end of interaction.
**Action:** The agent thanks the user, offers additional help, and gracefully ends the conversation.
**Example:** Thank you for contacting us today! Is there anything else I can assist you with?
