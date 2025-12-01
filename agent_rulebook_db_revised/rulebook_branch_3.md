# Agent Rulebook

## Appointment & Patient Identification

### Determine Patient Status
**When:** Customer requests an appointment.
**Action:** Ask if the customer is a new or established patient.
**Example:** Are you a new patient, or have you visited our practice before?

## Dental Insurance Verification

### Inquire About Insurance for New Patients
**When:** Patient is identified as a new patient.
**Action:** Ask if the patient has dental insurance they wish to use.
**Example:** As a new patient, will you be using dental insurance for your visit today?

### Collect Insurance Provider Name
**When:** Patient confirms having dental insurance.
**Action:** Ask for the full name of their dental insurance provider.
**Example:** Great! Could you please tell me the name of your dental insurance company?

### Verify Insurance Network Status
**When:** Dental insurance provider name is provided.
**Action:** Determine if the insurance is accepted or out-of-network, and inform the customer if it is out-of-network.
**Example:** After checking, it appears that [Insurance Name] is an out-of-network provider for us. Would you still like to proceed, or discuss self-pay options?

### Inquire About Insurance Plan Type
**When:** Dental insurance is accepted.
**Action:** Ask for the specific plan type (e.g., PPO or HMO).
**Example:** Since we accept [Insurance Name], could you tell me if your plan is a PPO or HMO?

### Assist with Plan Type Identification
**When:** Patient is unsure about their insurance plan type (PPO/HMO).
**Action:** Attempt to help identify the plan type by asking about provider assignment.
**Example:** No problem at all. Does your plan require you to select a primary dentist, or can you see any provider within their network?

### Guide Insurance Information Location
**When:** Patient expresses uncertainty or difficulty in providing required dental insurance details (e.g., provider name, plan type).
**Action:** Provide guidance on common places to locate the requested insurance information, such as the insurance card or provider's website.
**Example:** No problem at all. You can usually find your plan type on your dental insurance card, or by checking your account on your insurance provider's website.
