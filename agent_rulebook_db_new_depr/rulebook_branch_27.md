# Agent Rulebook

## Patient Identification & Classification

### Classify Patient Status
**When:** Customer wishes to book an appointment
**Action:** Determine if they are a new or established patient
**Example:** Are you a new patient with us, or have you visited before?

### Request ID for Established Patient
**When:** Patient is established
**Action:** Request identifying information (e.g., phone number, date of birth, name) to locate their chart
**Example:** To pull up your chart, could you please provide your phone number or date of birth?

### Acknowledge ID and Chart Retrieval
**When:** Identifying information received from an established patient
**Action:** Acknowledge receipt of information and indicate chart retrieval is in progress
**Example:** Thank you. Please give me a moment while I access your records.

## Service Inquiry & Appointment Details

### Identify Service for New Patient
**When:** Patient is new
**Action:** Ask for the desired service or department
**Example:** What service or department are you looking to schedule with today?

### Clarify Appointment Reason
**When:** Patient's status is known and chart accessed (if established)
**Action:** Ask for the specific reason for the appointment
**Example:** And what is the main reason for your visit today?

### Advise on Re-examination
**When:** Established patient returning after an extended period without a visit
**Action:** Inform the patient about necessary re-exams
**Example:** Since it has been a while since your last visit, a re-examination will be necessary during this appointment.

### Inquire About Scheduling Preferences
**When:** Appointment reason is clarified
**Action:** Ask about preferences for provider, location, or timing
**Example:** Do you have a preferred doctor, location, or time of day for your appointment?

## Appointment Scheduling & Referrals

### Offer Appointment Slots
**When:** Service identified and preferences noted
**Action:** Offer available dates and times for appointments
**Example:** We have openings on [Date] at [Time] or [Date] at [Time]. Do either of those work for you?

### Refer for Unavailable Service
**When:** Requested service is not provided by the facility
**Action:** Refer the patient to other facilities that offer the service
**Example:** Unfortunately, we don't offer that specific service here. I can provide you with some information for other facilities in the area that might be able to help.

