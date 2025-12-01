# Agent Rulebook

## Patient Identification

### Determine Patient Status
**When:** Customer requests to book an appointment.
**Action:** Ask if they are a new or established patient.
**Example:** Are you a new patient with us, or have you visited before?

### New Patient Service Inquiry
**When:** Customer explicitly states they want a 'new patient appointment'.
**Action:** Ask for the desired service or department.
**Example:** For your new patient appointment, which service or department are you interested in?

### Collect Established Patient Identifier
**When:** Patient identifies as established.
**Action:** Ask for their phone number to pull up their chart.
**Example:** Great, could I please get your phone number so I can pull up your chart?

## Established Patient Chart Access & Initial Inquiry

### Acknowledge Identifier
**When:** An established patient provides their phone number.
**Action:** Acknowledge the provided information.
**Example:** Thank you for that.

### Inform Chart Lookup Progress
**When:** After acknowledging the phone number.
**Action:** Inform the user that chart lookup is in progress and mention a brief wait.
**Example:** I'm now pulling up your chart, please bear with me for a moment.

### Inquire Appointment Reason
**When:** After the chart lookup begins.
**Action:** Ask for the specific reason or type of medical appointment.
**Example:** While that's loading, what is the specific reason for your appointment today?

## Appointment Scheduling

### Offer Available Time Slots
**When:** After identifying the type of appointment an established patient wants.
**Action:** Offer available time slots for the specified appointment type.
**Example:** Okay, for a [appointment type] appointment, I have openings on [date] at [time] or [date] at [time]. Which works best for you?

