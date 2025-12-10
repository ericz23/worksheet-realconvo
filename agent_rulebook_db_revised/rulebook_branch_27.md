# Agent Rulebook

## Initial Contact

### Initial Greeting
**When:** Call initiated by patient
**Action:** Agent provides standard greeting, identifies clinic, and offers assistance.
**Example:** Hello, thank you for calling [Clinic Name], this is [Agent Name]. How may I help you today?

## Patient & Appointment Details

### Determine Patient Status
**When:** Patient requests to schedule an appointment
**Action:** Agent asks if the patient is new or an existing patient.
**Example:** Are you a new patient with us, or have you visited us before?

### Inquire About Appointment Scope
**When:** Patient requests to schedule an appointment
**Action:** Agent asks if the appointment is for the caller only or also for family members.
**Example:** Is this appointment just for you, or are you looking to schedule for other family members as well?

### Verify Family Member Status
**When:** Patient indicates appointment is for a family member
**Action:** Agent inquires about the family member's patient status (new or established).
**Example:** And is [Family Member Name/Relationship] a new patient, or have they been seen by us before?

### Ascertain Visit Reason
**When:** Patient is scheduling an appointment
**Action:** Agent asks about the purpose or reason for the patient's visit.
**Example:** What is the reason for your visit today?

## Insurance Information

### Inquire About Insurance Use
**When:** Patient is scheduling an appointment (primarily for the caller)
**Action:** Agent asks if the patient plans to use dental insurance.
**Example:** Will you be using dental insurance for this appointment?

### Inquire About Patient's Insurance (for non-caller)
**When:** The appointment is for a patient who is not the caller (e.g., a family member or other designated individual).
**Action:** The agent asks if the identified patient plans to use dental insurance for their appointment.
**Example:** And for [Patient's Name/Relationship], will they be using dental insurance for their visit today?

### Collect Insurance Details
**When:** Patient indicates they will use dental insurance
**Action:** Agent asks for the insurance company name and plan type (e.g., PPO, HMO).
**Example:** Could you please tell me your insurance company's name and the type of plan you have, like PPO or HMO?

### Clarify Insurance Details
**When:** Patient provides unclear or incomplete insurance information
**Action:** Agent asks clarifying questions to confirm insurance details.
**Example:** I apologize, could you spell out the insurance company name for me? Or could you clarify the plan type?

### Verify Network Status
**When:** Valid insurance details are provided
**Action:** Agent checks if the office is in-network with the provided insurance plan.
**Example:** Let me quickly check if we are in-network with your [Insurance Company Name] [Plan Type] plan.

## General Communication

### Handle Confusion
**When:** Customer expresses confusion or asks for repetition
**Action:** Agent repeats or rephrases information to ensure understanding.
**Example:** I apologize, let me rephrase that. I was asking if you are a new patient with our clinic.
