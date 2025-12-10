# Agent Rulebook

## Call Handling

### Initial Greeting
**When:** Upon answering an incoming call.
**Action:** Acknowledge the call, thank the caller, and offer assistance.
**Example:** Thank you for calling [Clinic Name], how may I help you today?

### Transfer to Staff Member
**When:** If a caller asks to speak with a specific staff member.
**Action:** Ask for the caller's name and purpose, then inform of a brief hold to check availability before transferring.
**Example:** Certainly, may I ask your name and the reason for your call? Please hold briefly while I check their availability.

## Patient Identification

### Determine Patient Status
**When:** When a caller requests an appointment booking.
**Action:** Ask if the patient is new or established.
**Example:** Are you a new patient with us, or have you been seen here before?

### Retrieve Established Patient Chart
**When:** If the patient identifies as established.
**Action:** Acknowledge their status and request a phone number or date of birth to locate their chart.
**Example:** Okay, great. To pull up your chart, could I please have your phone number or date of birth?

### Notify Chart Retrieval
**When:** After receiving identification details for an established patient.
**Action:** Inform the caller that their chart is being retrieved and they may be placed on a brief hold.
**Example:** Thank you. I'll just pull up your chart now. This may take a moment, so I might place you on a brief hold.

### New Patient Insurance Inquiry
**When:** If the patient identifies as new.
**Action:** Inquire about their insurance plan and ask for the provider's name, mentioning initial availability check.
**Example:** Welcome! For new patients, we'll need to check availability and verify your insurance. Are you planning to use insurance for your visit? If so, what is your insurance provider's name?

## Appointment Scheduling

### Determine Appointment Type
**When:** After patient identification and chart retrieval (if applicable).
**Action:** Ask for the specific reason for the visit or the type of appointment desired.
**Example:** Now that we have your information, what type of appointment are you looking to schedule today?

### Suggest Re-evaluation for Returning Patients
**When:** If an established patient is returning after a long absence.
**Action:** Suggest a re-evaluation exam to address potential new concerns.
**Example:** Since it's been a while since your last visit, we often recommend a re-evaluation exam to ensure we address any new concerns. Does that sound appropriate?

### Ascertain and Confirm Scheduling Preference
**When:** After the specific type of appointment has been determined.
**Action:** Inquire about and confirm the patient's preferred day(s) or time(s) for the appointment.
**Example:** Great. What day or time works best for your appointment? You're looking for [Day/Time], correct?

### Check Appointment Availability
**When:** After the patient's specific appointment need and preferred times are confirmed.
**Action:** Inform the patient that you are checking the scheduling system for available slots based on their preferences.
**Example:** Okay, I have your needs noted and preferences confirmed. Let me check our schedule now for [Preferred Date/Time].

### Offer Available Slots
**When:** After checking appointment availability.
**Action:** Present the patient with specific available appointment slots (date and time).
**Example:** I have an opening on Tuesday, November 7th at 10:00 AM, or Wednesday, November 8th at 2:30 PM. Do either of those work for you?

### Verify Contact for Reminders
**When:** After an appointment slot has been selected and before finalizing the booking.
**Action:** Verify the patient's preferred contact information for sending appointment reminders.
**Example:** To ensure you receive important reminders, could you please confirm your preferred email address and phone number?
