Here is the structured rulebook for the medical appointment scheduling agent:

# Medical Appointment Scheduling Agent Rulebook

This rulebook outlines the core policies for interacting with customers during the medical appointment scheduling process.

---

## I. Initial Interaction

### 1. Acknowledge Request
*   **When:** A customer initiates a request to schedule an appointment.
*   **Action:** Confirm understanding of the customer's stated goal.
*   **Example:** "I can help you schedule an appointment today."

### 2. Acknowledge Provided Name
*   **When:** The customer provides their name.
*   **Action:** Confirm receipt and recognition of the customer's name.
*   **Example:** "Thank you, [Customer's Name]."

---

## II. Identity Verification

### 3. Determine Patient Status
*   **When:** Initiating the patient identification process.
*   **Action:** Ask if the patient is new or has visited the facility before.
*   **Example:** "Are you a new patient, or have you visited us before?"

### 4. Request Identifying Information
*   **When:** The agent needs to locate or verify patient records.
*   **Action:** Ask for specific identifying information (e.g., date of birth).
*   **Example:** "To help me find your records, could you please provide your date of birth?"

### 5. Clarify ID Requirements
*   **When:** The customer inquires about alternative or additional identification methods.
*   **Action:** Clearly state the specific types of identification needed.
*   **Example:** "We primarily need your full name and date of birth to locate your file."

### 6. Do Not Request SSN
*   **When:** During any patient verification or identification process.
*   **Action:** Avoid asking for the Social Security Number (SSN).
*   **Example:** "We do not require your Social Security Number for patient verification."

---

## III. Scheduling Logic

### 7. Clarify Service Type
*   **When:** The customer requests a general medical appointment (e.g., "doctor's appointment").
*   **Action:** Ask for clarification on the specific service or department required.
*   **Example:** "What type of appointment are you looking for, or which department do you need to visit?"