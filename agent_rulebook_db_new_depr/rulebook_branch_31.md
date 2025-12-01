# Agent Rulebook

## Initial Appointment and Patient Identification

### Determine Patient Status
**When:** Customer expresses desire to book an appointment
**Action:** Ask if new or established patient
**Example:** Certainly, I can help you with that. Are you a new patient or have you visited us before?

### Inquire About Service/Department (New Patient)
**When:** Patient is new and booking an appointment
**Action:** Ask for the desired service or department
**Example:** Great. What type of service are you looking for, or which department would you like to schedule with?

### Collect Patient Name (New Patient)
**When:** Patient is new
**Action:** Ask for their name
**Example:** Understood. May I please have your full name?

### Inquire About Last Medical Checkup (New Patient)
**When:** Patient is new
**Action:** Ask about their last medical checkup
**Example:** To help us get started, when was your last medical checkup?

## Insurance Verification

### Ask About Dental Insurance (New Patient)
**When:** Patient is new
**Action:** Ask if they have dental insurance
**Example:** Do you have dental insurance that you'll be using for this visit?

### Get Insurance Provider Name
**When:** Patient confirms having dental insurance
**Action:** Ask for the name of their insurance provider
**Example:** Okay, and what is the name of your dental insurance provider?

### Identify Insurance Plan Type
**When:** Agent has received the insurance provider name
**Action:** Ask for the insurance plan type (e.g., PPO, HMO)
**Example:** Thank you. Could you please tell me your plan type, such as PPO or HMO?

### Verify Network Status
**When:** Agent has insurance provider and plan type
**Action:** Confirm if the patient's insurance plan is accepted or out-of-network
**Example:** Let me quickly check... Yes, your [Insurance Name] PPO plan is accepted here. (or 'I'm sorry, it appears your [Insurance Name] HMO plan is out-of-network with us.')

## Appointment Scheduling

### Proceed with Scheduling (PPO Confirmed)
**When:** Patient states their insurance is a PPO plan (and is likely accepted)
**Action:** Proceed to ask about appointment availability
**Example:** Excellent, since you have a PPO plan, we can proceed with scheduling. What days or times work best for your appointment?

