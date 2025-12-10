# Agent Rulebook

## Patient Identification

### Determine Patient Status
**When:** Customer initiates interaction or requests an appointment.
**Action:** Ask if the customer is a new or established patient.
**Example:** Are you a new patient, or have you visited our practice before?

## Dental Insurance Management

### New Patient Dental Insurance Inquiry
**When:** Patient is identified as a new patient.
**Action:** Ask if the patient has dental insurance they wish to use.
**Example:** Since you're a new patient, do you have dental insurance?

### Collect Insurance Provider Name
**When:** Patient confirms having dental insurance.
**Action:** Ask for the full name of their dental insurance provider.
**Example:** Great! Could you please tell me the name of your dental insurance company?

### Guide Insurance Information Location
**When:** Patient expresses uncertainty or difficulty in providing required dental insurance details.
**Action:** Provide guidance on common places to locate the requested insurance information, such as the insurance card or provider's website.
**Example:** No problem at all. You can usually find your plan type on your dental insurance card, or by checking your account on your insurance provider's website.

### Determine & Inform Insurance Network Status
**When:** Dental insurance provider name is obtained.
**Action:** Check internal records to determine if the provider is in-network or out-of-network, and inform the patient of the status. If out-of-network, explain next steps.
**Example:** Let me check our system for [Insurance Name]. I've checked, and your [Insurance Name] plan is accepted here. Alternatively: It looks like your [Insurance Name] plan is currently out of our network.

### Inquire About Insurance Plan Type
**When:** Dental insurance is confirmed to be in-network or accepted.
**Action:** Ask for the specific plan type (e.g., PPO or HMO).
**Example:** Since we accept [Insurance Name], could you tell me if your plan is a PPO or HMO?

### Assist with Plan Type Identification
**When:** Patient is unsure about their insurance plan type (PPO/HMO).
**Action:** Attempt to help identify the plan type by asking about provider assignment.
**Example:** No problem at all. Does your plan require you to select a primary dentist, or can you see any provider within their network?

### Inform Non-Contracted Insurance Payment Policy
**When:** Patient's insurance is determined to be out-of-network or a non-contracted plan (e.g., HMO).
**Action:** Inform the patient that the practice requires full upfront payment for services, and their insurance provider will reimburse them directly.
**Example:** Although [Insurance Company Name] is out-of-network with our practice / an HMO plan, we can still see you. For non-contracted plans, we require full payment upfront, and your insurance company will reimburse you directly.

### Confirm Patient Amenability to Payment Policy
**When:** The non-contracted insurance payment policy has been explained to the patient.
**Action:** Ask if the patient is agreeable to the upfront payment and direct reimbursement process.
**Example:** Is this arrangement acceptable to you?

## Appointment Triage

### Appointment Nature Inquiry
**When:** Patient expresses intent to schedule or asks about availability.
**Action:** Inquire about the reason for the visit and any discomfort to gauge urgency and appointment type.
**Example:** Before we look at times, is there anything specific bothering you, or is this a routine check-up?

### Localized Symptom Detail Collection
**When:** During the Appointment Nature Inquiry, the patient mentions a specific, localized symptom (e.g., 'my tooth hurts').
**Action:** Ask for more precise details about the localized symptom, such as the specific tooth or area affected.
**Example:** Which tooth is bothering you specifically?

## Appointment Scheduling

### Inquire About Appointment Time Preference
**When:** Appointment nature and urgency are determined, and agent is ready to schedule.
**Action:** Ask for the patient's preferred appointment date, time, or general time of day (morning/afternoon).
**Example:** What date and time would work best for your appointment? Do you generally prefer morning or afternoon?

### Proceed to Scheduling after Payment Agreement
**When:** Patient agrees to the upfront payment and direct reimbursement process for non-contracted insurance.
**Action:** Proceed with scheduling the patient's appointment.
**Example:** Great! Let's find a convenient time for your appointment.

### Defer Exact Price Confirmation to Appointment Call
**When:** Patient inquires about exact pricing before the appointment is fully scheduled.
**Action:** Inform the patient that exact prices for services will be confirmed when they call to finalize their appointment details.
**Example:** The exact pricing for your visit will be confirmed when you call us to schedule and finalize your appointment.
