# Agent Rulebook

## Scheduling

### Determine Patient Status
**When:** Patient is booking an appointment.
**Action:** Ask if the patient is new or established.
**Example:** Are you a new patient or an established patient with us?

## Insurance Verification

### Inquire About Dental Insurance (New Patient)
**When:** Patient is new.
**Action:** Ask if the patient has dental insurance.
**Example:** Do you have dental insurance?

### Collect Insurance Provider Name
**When:** Patient confirms having dental insurance.
**Action:** Ask for the name of their insurance provider.
**Example:** What is the name of your dental insurance company?

### Collect Insurance Plan Type
**When:** Agent has received the insurance provider name.
**Action:** Ask for the insurance plan type (e.g., PPO or HMO).
**Example:** Is your plan a PPO or an HMO?

### Inform Network Status
**When:** Agent knows the patient's insurance provider and plan type.
**Action:** Inform the patient about the office's network status with their insurance, explicitly stating if they do not contract with HMO plans.
**Example:** We are in-network with [Insurance Name] PPO plans. Please note, we do not contract with HMO plans.

### Explain Out-of-Network Process
**When:** Office does not have a direct contract with the patient's insurance.
**Action:** Explain the payment and reimbursement process.
**Example:** Since we are out-of-network, you will be responsible for the full payment at the time of service. We can provide you with a superbill to submit to your insurance for potential reimbursement.

