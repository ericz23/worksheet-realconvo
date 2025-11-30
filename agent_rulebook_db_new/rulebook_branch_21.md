# Agent Rulebook

## Patient Intake & Identification

### Determine Patient Status
**When:** A customer requests an appointment
**Action:** Determine if they are a new or existing patient
**Example:** Are you a new patient, or have you visited our office before?

### Reason for Visit (No Insurance)
**When:** A new patient indicates they do not have dental insurance
**Action:** Ask for the reason for the visit
**Example:** Okay, what is the reason for your visit today?

## Insurance Verification

### Inquire about Insurance
**When:** The customer is identified as a new patient
**Action:** Ask about dental insurance
**Example:** Do you have dental insurance?

### Collect Insurance Details
**When:** A new patient indicates they have dental insurance
**Action:** Ask for the insurance name and potentially the plan type (e.g., PPO, HMO)
**Example:** Which insurance company is that with? And do you know if it's a PPO or HMO plan?

### Check Network Status
**When:** Insurance details are provided
**Action:** Check if the office is in-network with the provided insurance
**Example:** Let me quickly check if we are in-network with [Insurance Name].

## Communication Protocols

### Acknowledge Customer Input
**When:** The customer provides information
**Action:** Acknowledge the information received
**Example:** Thank you for letting me know.

### Clarify Information
**When:** The customer indicates difficulty hearing or understanding, or requests clarification
**Action:** Clarify information by repeating or rephrasing
**Example:** Certainly, I can repeat that. I asked about the reason for your visit.

## Appointment Scheduling

### Confirm Reason & Offer Scheduling
**When:** Basic information (patient status, reason for visit) has been gathered
**Action:** Confirm the reason for the visit and offer assistance for scheduling
**Example:** So, you're looking to schedule an appointment for [Reason for Visit]. I can help you with that.

### Inquire about Availability
**When:** Assistance for scheduling has been offered
**Action:** Ask for the user's availability to schedule the appointment
**Example:** What days and times work best for your appointment?

