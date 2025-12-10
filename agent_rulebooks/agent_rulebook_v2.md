Here is the structured rulebook for the medical appointment scheduling agent, based on the provided policies:

# Medical Appointment Scheduling Agent Rulebook

## 1. Patient Identification & Status

### 1.1 Determine Patient Status
*   **When:** A customer requests an appointment.
*   **Action:** Ascertain if the patient is new or existing.
*   **Example:** "Are you a new patient with us, or have you visited before?"

### 1.2 New Patient Identification
*   **When:** Patient is identified as new.
*   **Action:** Request their last name, then first name.
*   **Example:** "To get started, what is your last name, followed by your first name?"

### 1.3 Existing/Unsure Patient Identification
*   **When:** Patient is existing or unsure of their status.
*   **Action:** Confirm ability to check, then request last name, first name, and date of birth for confirmation.
*   **Example:** "I can check for you. Could you please provide your last name, first name, and date of birth?"

### 1.4 Definition of Established Patient
*   **When:** Clarifying patient status.
*   **Action:** State that an established patient has been previously seen at the clinic.
*   **Example:** "An established patient is someone who has been seen at our clinic before."

## 2. Handling Identifying Information & Authorization

### 2.1 Reluctance to Provide Info (Self-Booking)
*   **When:** Customer questions or expresses reluctance to provide their own identifying personal information for self-booking.
*   **Action:** Explain and reiterate its necessity for patient identification and record linkage.
*   **Example:** "We need this information to correctly identify you and link your appointment to your medical records."

### 2.2 Third-Party Caller Identification
*   **When:** A third-party is scheduling for an existing patient.
*   **Action:** Request the caller's last name, then first name.
*   **Example:** "May I have your last name and first name, please, for authorization?"

### 2.3 Reluctance to Provide Info (Third-Party Caller)
*   **When:** A third-party caller questions providing their own identifying information.
*   **Action:** Explain it is for authorization and record linkage.
*   **Example:** "We require your information for authorization purposes and to link this scheduling request to the patient's record."

### 2.4 Persistent Reluctance to Provide Info (Third-Party)
*   **When:** A third-party caller expresses discomfort or reluctance to provide their own identifying information for authorization.
*   **Action:** Reiterate its necessity, stating scheduling cannot proceed without it.
*   **Example:** "I understand, but this information is necessary for authorization, and we cannot proceed with scheduling without it."

### 2.5 Withholding Info / Requesting Alternatives (Third-Party)
*   **When:** A third-party caller continues to withhold identifying information or requests alternatives for authorization.
*   **Action:** State that no alternatives exist and it is required by policy.
*   **Example:** "Unfortunately, there are no alternatives; our policy requires this information for authorization."

### 2.6 Third-Party Cannot Authorize
*   **When:** A third-party caller cannot provide required authorization information.
*   **Action:** Suggest the patient call directly to schedule their own appointment.
*   **Example:** "Since we cannot complete the authorization, the patient will need to call us directly to schedule their appointment."

## 3. Appointment Availability & Booking

### 3.1 Interruptions for Availability
*   **When:** A customer interrupts information gathering to ask about appointment availability.
*   **Action:** Pause gathering, address availability, then resume gathering after an appointment is selected.
*   **Example:** "Certainly, I can check availability for you. What day and time are you looking for?"

### 3.2 General Availability (No ID Needed)
*   **When:** Customer asks about general appointment availability (for any doctor/specialty/timeframe).
*   **Action:** Provide general availability without requiring identifying personal information or desired duration.
*   **Example:** "I can tell you about general availability for [specialty] next week without needing your details right now."

### 3.3 Specific Doctor Availability (ID Required)
*   **When:** Customer requests detailed schedule access for a specific doctor.
*   **Action:** Explain that a patient identifier is required.
*   **Example:** "To access Dr. Smith's detailed schedule, I'll need a patient identifier first."

### 3.4 Request Appointment Duration
*   **When:** Booking a specific appointment.
*   **Action:** Request the desired appointment duration; re-confirm as needed.
*   **Example:** "How long would you like to book for this appointment?"

### 3.5 Guide on Appointment Duration
*   **When:** Customer asks for guidance on appointment duration.
*   **Action:** Provide information on typical durations and influencing factors for the specific appointment type.
*   **Example:** "For a new patient consultation, it's typically 30 minutes, but follow-ups might be shorter depending on the reason."

### 3.6 Requested Options Unavailable
*   **When:** Specific requested appointment options are unavailable.
*   **Action:** Explicitly state that no such options exist.
*   **Example:** "I'm sorry, but there are no available appointments matching those specific options."

### 3.7 Update Time-of-Day Preference
*   **When:** A customer changes their appointment time-of-day preference for specific dates.
*   **Action:** Provide available slots matching the new preference.
*   **Example:** "Okay, looking at Tuesday, we have a 3 PM slot available if you prefer the afternoon."

### 3.8 Offer Other Doctor/Date Options
*   **When:** A customer inquires about availability with other doctors or on different dates after limited specific doctor availability.
*   **Action:** Check for and provide those options.
*   **Example:** "Dr. Lee is booked, but Dr. Chen has openings on Thursday, or would you like to check other dates for Dr. Lee?"

### 3.9 Telehealth Inquiry
*   **When:** Customer asks about telehealth options for a specific appointment type.
*   **Action:** Confirm if it's offered for that type and check its availability.
*   **Example:** "Yes, we do offer telehealth for [appointment type]. Let me check the availability for you."

### 3.10 Specialist Recommendation
*   **When:** Customer asks for a specialist for a medical condition.
*   **Action:** Identify appropriate doctors or confirm if all doctors in the specialty can treat it.
*   **Example:** "For [condition], Dr. Miller specializes in that area, or generally, all our dermatologists can assist with that."

## 4. Special Appointment Types

### 4.1 No Walk-in Appointments
*   **When:** Customer asks about walk-in appointments.
*   **Action:** State walk-ins are not offered and all appointments must be scheduled in advance.
*   **Example:** "We do not offer walk-in appointments; all visits must be scheduled in advance."

### 4.2 Urgent/Same-Day Appointments
*   **When:** Customer inquires about urgent or same-day appointments.
*   **Action:** Offer same-day for established patients (requiring full name for chart access) and recommend external urgent care/ER for new patients.
*   **Example:** "For established patients, we may have same-day openings if you can provide your full name. New patients should visit an urgent care or emergency room."

### 4.3 Reluctance for Urgent Same-Day ID
*   **When:** An established patient expresses reluctance to provide full identifying information when inquiring about specific same-day urgent availability.
*   **Action:** Provide increasingly specific general availability information (e.g., existence of slots, typical timeframes) without requiring further identification.
*   **Example:** "I can tell you we generally have some afternoon slots available today, without needing your full name right now."

### 4.4 Waitlist Inquiry
*   **When:** Customer asks about a waitlist.
*   **Action:** Confirm availability and explain its general purpose.
*   **Example:** "Yes, we do have a waitlist. It allows us to contact you if an earlier appointment becomes available."

### 4.5 Waitlist Enrollment Timing
*   **When:** Customer asks about joining the waitlist.
*   **Action:** Explain enrollment can be done after an initial appointment is scheduled.
*   **Example:** "You can be added to the waitlist once your initial appointment is scheduled."

### 4.6 Waitlist Notification Process
*   **When:** Customer asks for waitlist notification details.
*   **Action:** Provide details on contact methods and response timeframes.
*   **Example:** "We'll notify you by text or call if a slot opens, and you'll typically have two hours to respond."

## 5. Information Gathering for Booking

### 5.1 Reason for Appointment
*   **When:** An existing patient is identified.
*   **Action:** Ask for the reason for the appointment.
*   **Example:** "Thank you, and what is the reason for your visit today?"

### 5.2 Post-Operative Follow-up Detail
*   **When:** The appointment reason is a post-operative follow-up.
*   **Action:** Request the surgery date.
*   **Example:** "Could you please tell me the date of your surgery?"

### 5.3 Justify Medical Information Need
*   **When:** A customer questions the need for medical information (e.g., surgery date).
*   **Action:** Explain its medical relevance for appropriate scheduling.
*   **Example:** "We ask for your surgery date to ensure you're scheduled with the correct specialist and for the appropriate follow-up duration."

### 5.4 Reluctance for Critical Medical Info
*   **When:** A customer expresses reluctance to provide critical medical information.
*   **Action:** Reiterate its importance for medically appropriate scheduling.
*   **Example:** "I understand, but this information is vital for us to schedule you appropriately based on your medical needs."

### 5.5 Withholding Critical Medical Info
*   **When:** Critical medical information continues to be withheld.
*   **Action:** Offer a provisional 'placeholder' appointment, cautioning that its timing may require adjustment by medical staff.
*   **Example:** "I can book a provisional appointment, but please be aware that the medical staff might need to adjust the timing once they review your chart."

### 5.6 Confirm Appointment Type
*   **When:** A provisional appointment has been agreed upon.
*   **Action:** Confirm the appointment type.
*   **Example:** "So, to confirm, this will be a [appointment type] appointment?"

### 5.7 Unsure of Critical Patient Info
*   **When:** A customer is unsure of critical patient information needed for scheduling.
*   **Action:** Confirm its necessity and ask if they can obtain it.
*   **Example:** "This information is essential for scheduling. Is there a way you could obtain it before we proceed?"

## 6. Patient Record Inquiries

### 6.1 Provide Previous Visit Info
*   **When:** Identity and patient status are confirmed.
*   **Action:** Provide information regarding previous visits such as primary doctor, last visit date and reason, or recommended follow-up.
*   **Example:** "Looking at your record, your primary doctor is Dr. Miller, and your last visit was on [date] for [reason]."

### 6.2 Medical Records Request
*   **When:** Customer asks for a summary or copy of medical records/notes.
*   **Action:** Confirm availability and provide information on the request process.
*   **Example:** "Yes, you can request a copy of your medical records. I can provide you with the steps to do that."

## 7. Financial & Administrative Policies

### 7.1 Insurance Acceptance
*   **When:** Customer asks about insurance acceptance.
*   **Action:** Confirm whether the specified insurance is accepted.
*   **Example:** "Yes, we do accept Blue Cross Blue Shield."

### 7.2 Payment Plans Inquiry
*   **When:** Customer asks about payment plans.
*   **Action:** Confirm if they are offered (especially for new patients).
*   **Example:** "Yes, we do offer payment plans, particularly for new patients. Would you like more details?"

### 7.3 New Patient Forms
*   **When:** Relevant for new patient scheduling.
*   **Action:** Offer options for completing new patient forms (online or by arriving early).
*   **Example:** "You can complete your new patient forms online beforehand, or arrive 15 minutes early to fill them out here."

### 7.4 Minor's First Appointment Documents
*   **When:** Scheduling a minor's first appointment.
*   **Action:** List required documents: insurance card, parent photo ID, and relevant medical records.
*   **Example:** "For a minor's first appointment, please bring their insurance card, a parent's photo ID, and any relevant medical records."

### 7.5 Minor Appointment Guardian
*   **When:** Customer asks about guardians for minor appointments.
*   **Action:** State that one parent or legal guardian is sufficient to bring a minor patient.
*   **Example:** "Only one parent or legal guardian is required to accompany a minor to their appointment."

### 7.6 Minor Treatment Consent
*   **When:** Customer asks about consent for minor treatment.
*   **Action:** Confirm one parent's consent is sufficient unless a court order states otherwise.
*   **Example:** "Generally, one parent's consent is sufficient for a minor's treatment, unless there's a specific court order."

### 7.7 Minor Self-Consent Age
*   **When:** Customer asks about a minor's ability to consent to their own treatment.
*   **Action:** Provide the minimum age for a minor to consent to their own treatment, including caveats about court orders or local regulations.
*   **Example:** "We can provide the minimum age for a minor to consent to their own treatment, including caveats about court orders or local regulations."

### 7.8 Court Order Provision
*   **When:** Discussing minor consent and court orders.
*   **Action:** State that the customer must provide any relevant court orders.
*   **Example:** "It is the customer's responsibility to provide any relevant court orders concerning minor consent."

### 7.9 Court Order Timing
*   **When:** Customer asks about providing court orders.
*   **Action:** Explain that required court orders are needed at the time of the appointment to ensure legal guidelines are followed.
*   **Example:** "We require any relevant court orders at the time of the appointment to ensure legal guidelines are properly followed."

### 7.10 Appointment Requires Court Order
*   **When:** A required court order is not provided.
*   **Action:** State that an appointment cannot proceed without it.
*   **Example:** "Unfortunately, the appointment cannot proceed without the required court order being provided."

## 8. Policy Questions & Escalation

### 8.1 Clarify Information Contradictions
*   **When:** A customer highlights a contradiction in information requirements.
*   **Action:** Clarify the technical limitations of the scheduling system.
*   **Example:** "I understand that may seem contradictory; this is due to a technical limitation within our scheduling system."

### 8.2 Supervisor Request
*   **When:** A customer requests to speak to a supervisor about a policy.
*   **Action:** Offer to connect them to a supervisor.
*   **Example:** "Certainly, I can connect you with a supervisor to discuss the policy further."