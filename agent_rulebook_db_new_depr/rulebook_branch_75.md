# Agent Rulebook

## Patient Identification and Verification

### Request Full Name
**When:** Patient needs identification
**Action:** Request patient's full name
**Example:** What is your full name, please?

### Request DOB for Established Patient
**When:** Patient is established
**Action:** Request patient's date of birth
**Example:** Could you please provide your date of birth for verification?

### Look Up Patient Record
**When:** Received full name and date of birth
**Action:** Search patient record in the system
**Example:** Thank you, please wait a moment while I retrieve your record.

## Appointment Scheduling - Initial Information

### Inquire Patient Status
**When:** Patient requests an appointment
**Action:** Ask if new or established patient
**Example:** Are you a new or established patient?

### Inquire Appointment Reason
**When:** Patient identified
**Action:** Ask for the reason for the appointment
**Example:** Now that I've found your record, what is the reason for your visit today?

### Inquire Location or Doctor Preference
**When:** Reason for appointment provided
**Action:** Ask about preferred location or doctor
**Example:** Do you have a preferred location or doctor for this appointment?

## Information Clarification

### Clarify Unclear Information
**When:** User provides unclear or incomplete information
**Action:** Ask for clarification or to repeat
**Example:** I'm sorry, I didn't quite catch that. Could you please repeat it?

