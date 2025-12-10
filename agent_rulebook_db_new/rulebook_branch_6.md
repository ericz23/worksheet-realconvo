# Agent Rulebook

## Patient Status Determination

### Determine Patient Status
**When:** Customer requests an appointment
**Action:** Agent asks if the patient is new or existing
**Example:** Are you a new or existing patient with our office?

## Dental Insurance Information

### Inquire About Dental Insurance (New Patient)
**When:** Customer identified as a new patient
**Action:** Agent asks if they have dental insurance
**Example:** Since you're a new patient, do you have dental insurance?

### Collect Insurance Name
**When:** Patient confirms having dental insurance
**Action:** Agent asks for the name of their insurance provider
**Example:** Great! What is the name of your dental insurance provider?

### Confirm Insurance Name Receipt
**When:** Patient provides insurance name
**Action:** Agent confirms receipt of the insurance name
**Example:** Thank you, so that's [Insurance Name].

### Collect Insurance Plan Type
**When:** Agent has received the insurance name
**Action:** Agent asks for the type of insurance plan (e.g., PPO/HMO, state insurance)
**Example:** And what type of plan do you have, such as PPO, HMO, or state insurance?

## Insurance Acceptance

### Inform Insurance Acceptance
**When:** Agent has verified insurance acceptance
**Action:** Agent informs the patient if their insurance is accepted or if the office is out of network
**Example:** Good news, we accept [Insurance Name],

## Customer Clarification

### Repeat Last Question
**When:** Customer asks for clarification on the last question
**Action:** Agent repeats the last question
**Example:** Certainly, I was asking [repeat last question].

