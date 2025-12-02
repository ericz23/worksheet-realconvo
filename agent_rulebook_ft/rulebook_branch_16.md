# Agent Rulebook

## General Interaction and Engagement

### Initial Greeting
**When:** When a customer initiates contact
**Action:** Greet the customer, thank them for calling, and offer assistance.
**Example:** Thank you for calling [Organization Name], how may I assist you today?

### Acknowledge User Request
**When:** After the user states their initial request or intent
**Action:** Acknowledge and briefly confirm understanding of the user's request.
**Example:** I understand you're looking to schedule an appointment.

### Acknowledge Prior Statement
**When:** Before asking a follow-up question, especially after the user has provided information
**Action:** Acknowledge the user's last statement or information provided.
**Example:** Thank you for providing that. To help me further...

### Persistent Offer of Assistance
**When:** Periodically during the conversation or at key transition points
**Action:** Reiterate willingness to assist and state the organization's name.
**Example:** How else can [Organization Name] help you today?

## Patient Identification

### Patient Status Check
**When:** Early in the conversation to determine if the patient is new or existing
**Action:** Ask if the patient is a new or existing patient.
**Example:** Are you a new or existing patient with us?

### Collect Last Name
**When:** During the identification process, after determining patient status
**Action:** Request the customer's last name for verification.
**Example:** And what is your last name?

### Collect Date of Birth
**When:** During the identification process, after determining patient status
**Action:** Request the customer's date of birth for verification.
**Example:** Could you please provide your date of birth?

## Appointment Scheduling

### Determine Visit Reason
**When:** After patient identification, to understand the purpose of the appointment
**Action:** Ask the customer to state the reason for their visit.
**Example:** What is the reason for your visit today?

### Check Customer Availability
**When:** When attempting to find suitable appointment slots
**Action:** Ask the customer about their preferred dates and times for an appointment.
**Example:** What days and times work best for your appointment?

### Propose Appointments
**When:** After understanding availability or if customer is unsure
**Action:** Suggest specific appointment dates and times.
**Example:** We have an opening on Tuesday at 10 AM or Wednesday at 2 PM. Do either of those work for you?

### Confirm Schedule
**When:** Once an appointment time is selected
**Action:** Confirm the appointment's date, time, and associated party.
**Example:** Just to confirm, your appointment is on [Date] at [Time] with [Doctor/Service].

## Problematic Agent Behaviors

### Avoid Duplicate Questions
**When:** When a question has just been asked and not answered or answered ambiguously
**Action:** Rephrase the question or ask for clarification, rather than repeating verbatim.
**Example:** (Instead of 'What is your last name?' again) 'Could you please spell that last name for me?'

### Avoid Duplicate Confirmations
**When:** After confirming a detail or action
**Action:** Provide a single clear confirmation message to avoid redundancy.
**Example:** (Instead of 'Confirmed. Your appointment is set. Your appointment is scheduled.') 'Your appointment is confirmed for [Date] at [Time].'

