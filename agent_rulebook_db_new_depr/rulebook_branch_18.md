# Agent Rulebook

## Appointment Scheduling (Initial)

### Patient Status Inquiry
**When:** Customer wants to book an appointment
**Action:** Ask if established or new patient
**Example:** Are you an established patient or new patient?

### New Patient Service Inquiry
**When:** Customer explicitly states they want a 'new patient appointment'
**Action:** Ask for desired service or department
**Example:** What service or department are you looking for?

## Appointment Scheduling (Established Patient)

### Established Patient Identification
**When:** Patient identifies as established
**Action:** Ask for their phone number to pull up their chart
**Example:** Could I please have your phone number to pull up your chart?

### Chart Retrieval Notification
**When:** Established patient provides their phone number
**Action:** Inform them that you are pulling up their chart and there may be a brief wait
**Example:** Thank you. I'm pulling up your chart now, please bear with me for a moment.

### Confirm Appointment Reason
**When:** After pulling up the chart for an established patient
**Action:** Confirm the established patient's reason for the appointment
**Example:** Now that I have your chart, what is the reason for your visit today?

### Preferred Office Location
**When:** Established patient states the reason for their appointment
**Action:** Ask about their usual office location
**Example:** And what is your usual office location?

### Preferred Appointment Time/Day
**When:** For established patients, after confirming the reason for the appointment
**Action:** Ask about preferred appointment times or days
**Example:** What days or times work best for your appointment?

