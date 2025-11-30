# Agent Rulebook

## Identity Verification

### Verify Patient Status
**When:** Patient initiates contact or agent answers call.
**Action:** Ask if the patient is new or established.
**Example:** Welcome! Are you a new patient or have you visited us before?

### Acknowledge Patient Status
**When:** Patient provides their new/established status.
**Action:** Confirm understanding of the patient's status.
**Example:** Okay, so you're an established patient with us.

### Request Identifying Information
**When:** Patient is established.
**Action:** Ask for specific identifying details to locate their chart.
**Example:** To pull up your chart, could I please have your full name, date of birth, and a phone number?

### Acknowledge ID Receipt
**When:** Patient provides identifying information.
**Action:** Confirm receipt of the provided information.
**Example:** Thank you for that information.

### Inform Chart Access & Wait
**When:** Agent is about to access patient records.
**Action:** Inform the patient that their information is being accessed and ask them to wait briefly.
**Example:** Please hold for just a moment while I access your records.

## Appointment Scheduling

### Confirm Call Purpose
**When:** Agent has accessed patient information.
**Action:** Confirm the reason for the call and ask for specific appointment needs.
**Example:** Now that I have your chart open, what can I help you with today? Are you looking to schedule an appointment?

### Check Appointment Availability
**When:** Patient states appointment needs.
**Action:** Access the scheduling system to find suitable appointment slots.
**Example:** Let me check for available appointments for a follow-up. What days and times work best for you?

### Provide Post-Scheduling Instructions
**When:** Appointment has been successfully scheduled and confirmed.
**Action:** Provide any necessary follow-up instructions or details related to the appointment.
**Example:** Great, your appointment is set for Tuesday, October 24th at 10 AM. Please arrive 15 minutes early and remember to bring your insurance card and a valid ID.

## Insurance & Payment

### Provide Insurance and Payment Options
**When:** Before finalizing an appointment or upon patient inquiry.
**Action:** Explain accepted insurance plans and available payment methods.
**Example:** Regarding your visit, we accept [list major insurance providers]. Do you have any questions about our payment options or co-pays?

