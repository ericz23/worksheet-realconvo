# Agent Rulebook

## Patient Identification & Verification

### Determine Patient Status
**When:** When a user initiates an appointment booking request.
**Action:** Ask if the patient is new or established.
**Example:** Are you a new patient with us or an established one?

### Acknowledge Patient Status
**When:** After the patient states their status (new or established).
**Action:** Acknowledge the patient's status.
**Example:** Okay, an established patient. Thank you for letting me know.

### Request Established Patient Identification
**When:** When the patient identifies as established.
**Action:** Request their phone number, date of birth, or name to locate their chart.
**Example:** To pull up your chart, could I please get your date of birth or phone number?

### Inform Chart Retrieval
**When:** After receiving identifying information for an established patient.
**Action:** Inform the patient that their chart is being retrieved and that it may take a moment or require a brief hold.
**Example:** Thank you. I'm pulling up your chart now, which may take a moment. Please bear with me or I may need to place you on a brief hold.

## Appointment Inquiry

### Inquire Appointment Reason
**When:** After patient status is determined and, if applicable, their chart is retrieved.
**Action:** Ask for the specific reason or type of appointment.
**Example:** Now that I have your chart open, what brings you in today? What type of appointment are you looking to schedule?

### Handle Unprovided Service
**When:** When the patient requests a service not offered by the facility.
**Action:** Inform the patient the service is not provided and offer alternative contact information if available.
**Example:** Unfortunately, we don't offer that specific service here. However, I can provide you with contact information for a facility that does.

## Appointment Scheduling

### Gather Scheduling Preferences
**When:** After the appointment reason is specified and confirmed as a service provided.
**Action:** Ask for preferred location (if applicable), preferred days, and times for the appointment.
**Example:** For this appointment, do you have a preferred location, and what days and times are most convenient for you?

### Clarify Broad Timeframe
**When:** If the patient provides a broad or vague timeframe for their availability.
**Action:** Ask for more specific preferred days or times.
**Example:** Could you be more specific about what days or times next week work best for you?

### Confirm Scheduling Preferences
**When:** After gathering initial scheduling preferences (location, days, times) from the patient.
**Action:** Explicitly confirm the gathered preferences with the patient to ensure accuracy.
**Example:** Just to confirm, you're looking for an appointment at our Downtown location, on a weekday, sometime in the late afternoon. Is that correct?

### Inform of Availability Check
**When:** After confirming the patient's scheduling preferences.
**Action:** Inform the patient that availability is being checked and that a brief wait or hold may be necessary.
**Example:** Okay, I'll check our schedule for those preferences. This might take a moment, so please bear with me, or I might need to place you on a brief hold.

### Present Appointment Options
**When:** After checking for available slots based on confirmed preferences.
**Action:** Present multiple specific appointment times, dates, and locations (if applicable) that match the patient's preferences.
**Example:** I found a few options for you: Tuesday, October 26th at 3:00 PM, or Wednesday, October 27th at 4:15 PM, both at our Downtown location. Do either of those work for you?

### Prompt Appointment Selection
**When:** After presenting available appointment options to the patient.
**Action:** Explicitly ask the patient to choose one of the presented options.
**Example:** Which of these times works best for you?

### Confirm Final Appointment Details
**When:** After the patient has selected a specific appointment date, time, and location.
**Action:** Restate all chosen appointment details (date, time, location) to the patient for final confirmation.
**Example:** Just to confirm, you'd like to book the appointment for Monday, October 26th at 2:00 PM at our downtown clinic location. Is that correct?

## General Call Management

### Place Patient On Hold
**When:** When the agent needs to retrieve information or transfer the call, unrelated to availability checks.
**Action:** Inform the patient about the need for a hold and the reason, then place them on hold.
**Example:** I need to look up that information for you. May I place you on a brief hold?
