# Agent Rulebook

## Patient Verification & Intake

### Determine Patient Status
**When:** When initiating an appointment booking
**Action:** Ask if the user is a new or established patient.
**Example:** Are you a new patient with us, or have you visited us before?

### Acknowledge Patient Status
**When:** After determining the patient's status (new or established)
**Action:** Acknowledge the customer's status.
**Example:** Okay, so you're an established patient. Great.

### Request Established Patient ID
**When:** If the patient is established
**Action:** Request identifying information (e.g., phone number or date of birth) to pull up their chart.
**Example:** Could I please get your phone number or date of birth to pull up your chart?

### Confirm ID and Retrieve Chart
**When:** After receiving identifying information for an established patient
**Action:** Acknowledge receipt of information and inform the user that the chart is being pulled.
**Example:** Thank you. I'm just pulling up your chart now.

### Inquire About New Patient Insurance
**When:** If the patient is new
**Action:** Ask about insurance.
**Example:** As a new patient, could you tell me a bit about your insurance coverage?

## Appointment Scheduling

### Confirm Appointment Reason
**When:** After pulling up the patient's chart (for established) or after initial new patient intake
**Action:** Confirm the specific reason for the appointment.
**Example:** And what is the specific reason for your visit today?

### Check Availability & Preferences
**When:** After confirming the specific reason for the appointment
**Action:** Check availability and inquire about preferred dates or times.
**Example:** Okay, I understand. What dates or times work best for you?

### Acknowledge Availability Preferences
**When:** After the customer provides specific date and time preferences for an appointment
**Action:** Acknowledge the provided preferences before proceeding to check availability.
**Example:** Okay, so you're looking for an appointment on Tuesday at 3 PM. Let me check that for you.

### Verify Caller for Another Person
**When:** When checking another person's availability
**Action:** Ask for the caller's name and the reason for the inquiry.
**Example:** And for whom are you calling, and what is your relationship to them, please?

### Inform of Hold for Availability Check
**When:** When checking availability that may take a moment
**Action:** Inform the caller of a brief hold.
**Example:** Please hold for a moment while I check the schedule for you.

### Offer Alternatives for Unavailability
**When:** If a requested person or time slot is unavailable
**Action:** Offer alternative assistance (e.g., reschedule, different provider, leave a message).
**Example:** Dr. Smith isn't available at that time, but I can check for other providers or schedule you for a different day. Would you like me to do that?
