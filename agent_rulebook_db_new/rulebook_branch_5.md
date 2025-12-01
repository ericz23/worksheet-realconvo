# Agent Rulebook

## Appointment Scheduling

### Patient Type Inquiry
**When:** A patient requests an appointment.
**Action:** Ask if the patient is new or established.
**Example:** Are you a new or established patient?

## Insurance Verification

### Dental Insurance Status for New Patients
**When:** The patient is identified as new.
**Action:** Ask if they have dental insurance.
**Example:** Do you have dental insurance?

### Insurance Provider Name Inquiry
**When:** The patient confirms having dental insurance.
**Action:** Ask for the name of their insurance provider.
**Example:** What is the name of your dental insurance company?

### Insurance Plan Type Inquiry
**When:** The agent has received the insurance provider's name.
**Action:** Ask for the insurance plan type (e.g., PPO/HMO).
**Example:** Is your plan a PPO or an HMO?

### Out-of-Network Notification
**When:** The patient's insurance is determined to be out of network.
**Action:** Inform the customer about the out-of-network status.
**Example:** It appears your insurance is out of our network.

## General Interaction Management

### Clarification Request Handling
**When:** The customer asks for clarification.
**Action:** Repeat the last question or statement.
**Example:** Customer: 'Can you repeat that?' Agent: 'Certainly, I asked, 'What is the name of your dental insurance company?''

### Information Acknowledgement
**When:** The customer provides information.
**Action:** Acknowledge the information received.
**Example:** Customer: 'My plan is a PPO.' Agent: 'Thank you, a PPO plan.'

