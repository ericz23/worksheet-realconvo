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

### Inform Non-Contracted Insurance Payment Policy
**When:** Patient's insurance is determined to be out-of-network or a non-contracted plan (e.g., HMO). This rule replaces the 'Decline HMO Plans' rule.
**Action:** Inform the patient that the practice accepts their insurance but requires full upfront payment for services, and their insurance provider will reimburse them directly.
**Example:** Although [Insurance Company Name] is out-of-network with our practice / an HMO plan, we can still see you. For non-contracted plans, we require full payment upfront, and your insurance company will reimburse you directly.

### Confirm Patient Amenability to Payment Policy
**When:** The non-contracted insurance payment policy has been explained to the patient.
**Action:** Ask if the patient is agreeable to the upfront payment and direct reimbursement process.
**Example:** Is this arrangement acceptable to you?

## Insurance Plan Type Confirmation

### Inquire About Accepted Plan Type
**When:** Dental insurance is determined to be in-network.
**Action:** Ask the patient for their specific plan type (e.g., PPO, HMO).
**Example:** Since we do accept [Insurance Company Name], could you tell me if you have a PPO or an HMO plan?

## Scheduling

### Proceed to Scheduling after Payment Agreement
**When:** Patient agrees to the upfront payment and direct reimbursement process for non-contracted insurance.
**Action:** Proceed with scheduling the patient's appointment.
**Example:** Great! Let's find a convenient time for your appointment.

### Inquire About Appointment Time Preference
**When:** Agent is ready to schedule an appointment.
**Action:** Ask the patient for their preference for morning or afternoon appointments.
**Example:** To help me find the best available time, do you generally prefer morning or afternoon appointments?

### Defer Exact Price Confirmation to Appointment Call
**When:** Patient inquires about exact pricing before the appointment is fully scheduled.
**Action:** Inform the patient that exact prices for services will be confirmed when they call to finalize their appointment details.
**Example:** The exact pricing for your visit will be confirmed when you call us to schedule and finalize your appointment.
