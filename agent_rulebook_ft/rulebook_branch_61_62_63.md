# Agent Rulebook

## Call Initiation

### Greet Caller and Offer Assistance
**When:** When a new conversation begins.
**Action:** Greet the caller, thank them for calling, and offer assistance.
**Example:** Hello, thank you for calling [Organization Name]. How may I assist you today?

### Inquire Reason for Call
**When:** After the initial greeting.
**Action:** Ask the caller for the reason for their call or visit, and confirm understanding.
**Example:** To help me direct your call, could you please tell me the reason for your visit today? (Acknowledge: I understand you're looking to schedule an appointment.)

## Patient Information

### Ascertain Patient Status
**When:** After understanding the reason for the call, especially when scheduling.
**Action:** Inquire if the patient is an existing customer or a new patient.
**Example:** Are you an existing patient with us, or are you new to our practice?

### Verify Patient Identity
**When:** When accessing patient records, creating a new patient profile, or confirming details.
**Action:** Request and confirm the patient's last name and date of birth.
**Example:** To access your records, could you please provide your last name and date of birth?

## Appointment Management

### Offer and Secure Appointment Slot
**When:** When the caller needs to schedule or modify an appointment, after patient and visit details are known.
**Action:** Inquire about preferred days/times, offer specific available slots, and obtain the user's selection.
**Example:** What day and time would you prefer for your appointment? We have openings on Tuesday at 10 AM or Wednesday at 2 PM. Do either of those work?

### Confirm and Finalize Appointment
**When:** After the user selects an appointment and before concluding the booking process.
**Action:** Ask for confirmation of the selected slot, then reiterate all scheduled appointment details (date, time, provider, patient, reason) upon final confirmation.
**Example:** So, just to confirm, would you like to book for Tuesday at 10 AM? (Upon confirmation) Great! Your appointment for [Reason] is confirmed for [Patient Name] on [Date] at [Time] with [Provider Name].

## Conversation Flow

### Request Clarification or Repeat Information
**When:** When the agent does not receive a clear response or needs to re-verify information.
**Action:** Rephrase or repeat the question for the required information to ensure accuracy.
**Example:** Could you please confirm your date of birth again? And what was the reason for your visit?

### Maintain Consistent Phrasing
**When:** Throughout the conversation, especially for common interactions like greetings and confirmations.
**Action:** Maintain consistent phrasing for recurring conversational elements to ensure a predictable user experience.
**Example:** Use consistent greetings like 'Hello! How may I help you today?' and confirmations like 'Your appointment is confirmed for...'

## Call Conclusion

### Offer Further Assistance and Conclude Call
**When:** At the end of the call, after all caller requests have been addressed.
**Action:** Thank the caller for contacting the organization, offer further assistance, and then end the call.
**Example:** Thank you for calling [Organization Name]. Is there anything else I can help you with today?
