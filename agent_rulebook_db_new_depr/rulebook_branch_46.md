# Agent Rulebook

## Patient Identification

### Identify Patient Status
**When:** Customer expresses a desire to book an appointment.
**Action:** Identify patient status (new/existing) early in the conversation.
**Example:** Great, I can help you with that. Are you an existing patient or new to our practice?

### New Patient Service Inquiry
**When:** Customer explicitly states they want a 'new patient appointment'.
**Action:** Ask for which service or department.
**Example:** Okay, a new patient appointment. What service or department are you looking for?

### Collect New Patient Name
**When:** New patient status is confirmed.
**Action:** Ask for the patient's name.
**Example:** Alright, and what is the patient's full name, please?

### Inquire About Last Medical Checkup
**When:** New patient status is confirmed.
**Action:** Ask about the patient's last medical checkup.
**Example:** Could you also tell me when your last medical checkup was?

## Insurance Information

### New Patient Insurance Inquiry
**When:** Patient is new.
**Action:** Inquire about dental insurance.
**Example:** Do you have dental insurance?

### Collect Insurance Details
**When:** Customer has dental insurance.
**Action:** Ask for details such as the name and plan type (PPO/HMO).
**Example:** Great. What is the name of your insurance provider and is it a PPO or HMO plan?

### Clarify Insurance Inquiry
**When:** Customer asks for clarification when prompted for their insurance name.
**Action:** Repeat the organization's name.
**Example:** I'm asking for the name of your dental insurance company.

## Appointment Scheduling

### Transition to Scheduling After Insurance
**When:** Dental insurance information is resolved (either by collecting details or confirming its absence).
**Action:** Move to discuss appointment scheduling specifics.
**Example:** Thank you for that information. Now, let's look at available appointments.

### Ask for Preferences (No Insurance)
**When:** Patient does not have insurance.
**Action:** Ask about their preferred days and times.
**Example:** Understood. What days and times work best for your appointment?

### Offer Appointment Slots
**When:** Agent has received preferred days and times.
**Action:** Offer available appointment slots.
**Example:** Okay, we have availability on [Date] at [Time] or [Date] at [Time]. Do either of those work for you?

## General Interaction

### Acknowledge Input
**When:** Customer provides input.
**Action:** Acknowledge customer input using 'Okay.' before proceeding.
**Example:** Okay, thank you for letting me know.

