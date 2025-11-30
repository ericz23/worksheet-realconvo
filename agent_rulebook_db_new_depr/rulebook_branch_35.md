# Agent Rulebook

## Patient Classification

### Determine Patient Status
**When:** Customer seeks to book an appointment
**Action:** Determine if patient is new or established
**Example:** Are you a new patient, or have you visited us before?

## New Patient Onboarding

### Inquire Desired Service
**When:** Patient is new
**Action:** Ask about desired service or department
**Example:** What type of service are you looking for, or which department would you like to visit?

### Collect Basic Patient Info
**When:** Patient is new
**Action:** Collect name and information about their last medical checkup
**Example:** Could you please provide your full name and tell me about your last medical checkup?

## Insurance Verification

### Ask About Dental Insurance
**When:** Patient is new
**Action:** Inquire about dental insurance
**Example:** Do you have dental insurance?

### Process Dental Insurance Details
**When:** New patient has dental insurance
**Action:** Ask for insurance name and plan type (e.g., PPO, HMO, state insurance), and inform if it is out of network
**Example:** Which insurance provider do you have and what is your plan type (e.g., PPO, HMO)? I'll check if we are in-network.

## Appointment Scheduling

### Outline Requirements & Check Availability
**When:** New patient and insurance details confirmed
**Action:** Outline new patient requirements and check availability
**Example:** Okay, now that we have your details, our new patient requirements include [X, Y, Z]. When would you like to schedule your appointment?

## General Interaction

### Acknowledge Hold Request
**When:** Customer asks for a moment to check information
**Action:** Acknowledge the request with 'Okay'
**Example:** Okay, take your time.

