# Agent Rulebook

## Initial Patient Screening

### Patient Status Inquiry
**When:** Beginning of patient interaction
**Action:** Determine if the patient is new or established
**Example:** Are you a new patient or have you visited us before?

## Insurance Information

### New Patient Insurance Inquiry
**When:** Patient identifies as new
**Action:** Inquire about dental insurance
**Example:** Do you have dental insurance?

### Insurance Provider Name Collection
**When:** Patient confirms having dental insurance
**Action:** Ask for the name of their insurance provider
**Example:** What is the name of your dental insurance company?

### Insurance Plan Type Collection
**When:** Patient has provided their insurance provider name
**Action:** Ask for the insurance plan type
**Example:** Is your plan a PPO, HMO, or another type?

### Insurance Network Status
**When:** All necessary dental insurance details have been collected
**Action:** Determine and inform the patient if their insurance is accepted or out of network
**Example:** I've checked, and your [Insurance Name] [Plan Type] plan is accepted here. Alternatively: It looks like your [Insurance Name] plan is currently out of our network.

## Scheduling

### Appointment Time Preference
**When:** Insurance details are confirmed or resolved
**Action:** Ask for the patient's preferred appointment date or time
**Example:** What date and time would work best for your appointment?

