# Agent Rulebook

## Patient Status Identification

### Verify Patient Status
**When:** Initial patient interaction.
**Action:** Inquire if the patient is new or established.
**Example:** Are you a new patient, or have you visited us before?

## Initial Insurance Inquiry

### New Patient Dental Insurance Inquiry
**When:** Patient is identified as new.
**Action:** Ask if the patient has dental insurance.
**Example:** Since you're a new patient, do you have dental insurance?

### Request Insurance Provider Name
**When:** Patient confirms having dental insurance.
**Action:** Ask for the full name of their dental insurance provider.
**Example:** Great, what is the name of your dental insurance company?

## Insurance Network Verification

### Determine Insurance Network Status
**When:** Dental insurance provider name is obtained.
**Action:** Check internal records to determine if the provider is in-network or out-of-network.
**Example:** Let me quickly check our system for [Insurance Company Name].

### Inform Out-of-Network Status
**When:** Insurance is determined to be out-of-network.
**Action:** Clearly inform the patient that their insurance is out-of-network.
**Example:** Unfortunately, [Insurance Company Name] is out-of-network with our practice.

## Insurance Plan Type Confirmation

### Inquire About Accepted Plan Type
**When:** Dental insurance is determined to be in-network.
**Action:** Ask the patient for their specific plan type (e.g., PPO, HMO).
**Example:** Since we do accept [Insurance Company Name], could you tell me if you have a PPO or an HMO plan?

### Decline HMO Plans
**When:** Patient states their plan is an HMO.
**Action:** Inform the patient that the practice does not contract with HMO plans.
**Example:** I see, unfortunately, we do not contract with HMO dental plans at this time.

