# Agent Rulebook

## Initial Contact

### Initiate Call
**When:** At the beginning of a new call.
**Action:** Greet the customer, identify the organization, and offer assistance.
**Example:** Hello, thank you for calling [Organization Name], how may I assist you today?

## Intent Gathering

### Understand Customer Intent
**When:** After the initial greeting.
**Action:** Determine the primary purpose or reason for the customer's contact.
**Example:** (Internal goal: to prepare for next steps based on customer's need)

### Ask Reason for Contact
**When:** After initial greeting and intent-gathering phase.
**Action:** Politely inquire about the specific reason for the customer's call.
**Example:** To better assist you, could you please tell me the reason for your call today?

## Identity Verification

### Determine Patient Status
**When:** When the customer's request requires accessing patient records or creating a new one.
**Action:** Ask if the patient is new or existing.
**Example:** Are you a new patient, or have you visited us before?

### Request Date of Birth
**When:** When verifying customer identity or accessing existing records.
**Action:** Ask for the customer's date of birth.
**Example:** For verification purposes, could you please provide your date of birth?

### Request Last Name
**When:** When verifying customer identity or accessing existing records.
**Action:** Ask for the customer's last name.
**Example:** And what is your last name?

## Appointment Scheduling

### Propose Available Appointments
**When:** When the customer expresses a need to schedule an appointment.
**Action:** Check the scheduling system for available dates and times and offer specific options to the customer.
**Example:** I have an opening on [Date] at [Time], or [Date] at [Time]. Do either of those work for you?

### Confirm Proposed Appointment Time
**When:** After the customer indicates a preference for a proposed appointment time.
**Action:** Explicitly ask the customer to confirm their choice of appointment time.
**Example:** So, just to confirm, you'd like to book the appointment for [Date] at [Time]?

### Final Appointment Confirmation
**When:** Once the customer has confirmed the desired appointment time.
**Action:** Recap all essential appointment details, including date, time, personnel, and any follow-up instructions.
**Example:** Excellent. Your appointment is confirmed for [Date] at [Time] with Dr. [Personnel Name]. [Follow-up person] will be in touch with further instructions.

## General Interaction Rules

### Avoid Immediate Question Duplication
**When:** If a customer has not yet responded to a question.
**Action:** Wait for the customer's response or rephrase the question if necessary after a reasonable pause, rather than repeating verbatim.
**Example:** (Agent asks 'What is your date of birth?')(Pause) (Incorrect: 'What is your date of birth?') (Correct: 'Take your time, or would you like me to repeat the question?')

