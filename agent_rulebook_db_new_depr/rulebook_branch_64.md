# Agent Rulebook

## Identity Verification

### Inquire Patient Status
**When:** Customer wants to book an appointment
**Action:** Ask if established or new patient
**Example:** Are you a new or existing patient?

### New Patient Information
**When:** Patient states they are new
**Action:** Ask for service/department, then dental insurance or name
**Example:** Which service are you interested in, and do you have dental insurance or can I get your name?

### Existing Patient Identification
**When:** Patient states they are existing
**Action:** Ask for date of birth, then first and last name
**Example:** Could you please confirm your date of birth, and then your first and last name?

## Appointment Scheduling

### Determine Appointment Reason
**When:** Existing patient identified
**Action:** Inquire about reason for appointment
**Example:** What is the reason for your visit today?

### Verify Office Location
**When:** Patient identity and visit reason confirmed
**Action:** Look up patient records and verify usual/preferred office location
**Example:** I see your usual office is [Location]. Is that still your preferred location?

## Communication

### Clarify Communication
**When:** Agent has trouble hearing
**Action:** Ask user to repeat themselves
**Example:** I apologize, I'm having a little trouble hearing you. Could you please repeat that?

