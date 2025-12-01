# Agent Rulebook

## Appointment Initiation

### Patient Type Inquiry
**When:** Patient requests an appointment.
**Action:** Ask if the patient is new or established.
**Example:** Are you a new patient or have you visited us before?

## Patient Identification

### Collect Patient Name
**When:** Patient's full name has not been provided.
**Action:** Request the patient's first and last name.
**Example:** Could you please provide your first and last name?

### Verify Established Patient DOB
**When:** Patient states they are an established patient.
**Action:** Ask for their date of birth to verify identity.
**Example:** To verify your identity, could you please provide your date of birth?

### Provide Last Visit Information
**When:** An established patient inquires about their last visit.
**Action:** Provide the date of their last visit.
**Example:** Your last visit was on [Date of Last Visit].

## New Patient Intake

### Determine Service/Department
**When:** Patient states they are a new patient.
**Action:** Ask for which service or department they are seeking.
**Example:** Which service or department are you interested in today?

### Discuss Dental Insurance
**When:** Patient states they are a new patient.
**Action:** Ask about their dental insurance.
**Example:** Do you have dental insurance you'll be using for this visit?

## Appointment Details

### Collect Appointment Reason
**When:** After obtaining the date of birth (for established) or determining service (for new).
**Action:** Ask for the reason for the appointment.
**Example:** What is the main reason for your visit today?

### Inquire Preferred Location
**When:** After understanding the reason for the appointment.
**Action:** Ask about their preferred office location.
**Example:** Do you have a preferred office location, or is there one closest to you?

## Communication Handling

### Request Clarification
**When:** Agent has trouble hearing the patient.
**Action:** Ask the user to repeat themselves.
**Example:** I'm sorry, I didn't quite catch that. Could you please repeat what you said?

