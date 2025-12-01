# Agent Rulebook

## Patient Identification

### Determine Patient Status
**When:** User wants to book an appointment
**Action:** Ask if new or established patient
**Example:** Are you a new or established patient?

### Acknowledge Patient Status
**When:** After patient states their status (new/established)
**Action:** Acknowledge their status
**Example:** Okay, you're an established patient.

### Request Established Patient ID
**When:** Patient is established
**Action:** Ask for phone number or date of birth
**Example:** To pull up your chart, could I get your phone number or date of birth?

### Inform Chart Retrieval
**When:** After receiving established patient ID info
**Action:** Inform user about chart retrieval and possible brief hold
**Example:** Thank you. I'm pulling up your chart now, this may take a moment. I might place you on a brief hold.

## Appointment Scheduling

### Ask for Appointment Reason
**When:** After an established patient's chart has been retrieved or after determining a new patient
**Action:** Ask for specific reason or type of appointment
**Example:** Now that I have your chart, what is the reason for your visit today?

### Request Desired Time/Date
**When:** After clarifying the reason/type of appointment
**Action:** Ask for desired time/date
**Example:** What day and time works best for your appointment?

