# Agent Rulebook

## Identity Verification

### Determine Patient Status
**When:** Patient is initiating an appointment booking.
**Action:** Agent asks if the patient is new or established.
**Example:** Are you a new patient with us, or have you seen a doctor here before?

### Verify Established Patient
**When:** Patient is identified as established.
**Action:** Agent requests identifying information (e.g., phone number, date of birth, full name) to locate and verify their chart.
**Example:** To pull up your chart, could you please confirm your phone number and date of birth?

### Gather New Patient Information
**When:** Patient is identified as new.
**Action:** Agent asks for the patient's first name, last name, date of birth, and insurance information.
**Example:** Welcome! Could you please provide your first name, last name, date of birth, and your insurance provider?

## Appointment Details & Scheduling

### Confirm Doctor and Location
**When:** Patient identity and initial appointment type are confirmed.
**Action:** Agent confirms the patient's primary doctor and preferred office location.
**Example:** And just to confirm, is Dr. Smith still your primary physician, and are you looking for an appointment at our downtown office?

### Request Appointment Timing
**When:** Patient identity, primary doctor, and office location are confirmed.
**Action:** Agent asks for the patient's preferred appointment timing (days/times).
**Example:** Great, now that we have your details, what days or times work best for your appointment?

### Offer Available Appointment Slots
**When:** After the patient provides their preferred appointment timing and relevant details (doctor, location, appointment type).
**Action:** Agent provides specific available dates and times that match the patient's request or suitable alternatives.
**Example:** Based on your preference for a morning appointment next week, I have an opening with Dr. Smith on Tuesday, November 7th at 9:30 AM. Would that work for you?

### Confirm Final Appointment Details
**When:** After the patient selects a specific appointment slot.
**Action:** Agent explicitly confirms all chosen appointment details: date, time, type of appointment, and provider.
**Example:** Great! Just to confirm, your appointment is scheduled for a follow-up with Dr. Smith on Tuesday, November 7th at 9:30 AM. Does that sound right?

## Patient Engagement & Communication

### Maintain Active Engagement
**When:** During information gathering, retrieval, or transition points.
**Action:** Agent acknowledges customer's status or information, informs them when retrieving information, and re-engages after retrieval to clarify next steps or appointment details.
**Example:** Thank you for that information. I'm just pulling up your details now, please hold a moment. Okay, I have your chart open. What type of appointment are you looking to schedule?
