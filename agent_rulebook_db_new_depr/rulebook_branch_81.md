# Agent Rulebook

## Appointment Initiation

### Determine Patient Status
**When:** A patient requests an appointment
**Action:** The agent asks if the patient is new or established.
**Example:** Hello! Are you a new patient with us, or have you visited before?

## Patient Identification & Verification

### Identify Established Patient
**When:** The patient states they are established
**Action:** The agent asks for the patient's full name and date of birth.
**Example:** Welcome back! To find your records, could you please provide your full name and date of birth?

### Collect New Patient Information
**When:** The patient states they are new
**Action:** The agent asks for the desired service/department and collects necessary identifying information (e.g., full name, dental insurance details).
**Example:** Great! What service are you interested in today, and could I get your full name and any dental insurance information you have?

### Clarify Ambiguous Patient Name
**When:** Multiple patient records match the provided name, leading to ambiguity
**Action:** The agent asks for additional identifying information to clarify.
**Example:** I see a couple of patients with that name. To ensure I access the correct record, could you please confirm your date of birth?

## Record Management

### Look Up Patient Record
**When:** The agent has received sufficient identifying information for the patient
**Action:** The agent searches for and accesses the patient's record in the system.
**Example:** One moment while I pull up your file.

## Appointment Details Collection

### Ascertain Appointment Reason
**When:** An established patient has been successfully identified and their record accessed
**Action:** The agent asks for the specific reason for the appointment.
**Example:** Now that I've located your record, what's the reason for your visit today?

