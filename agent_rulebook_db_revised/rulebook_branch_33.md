# Agent Rulebook

## Patient Status & Acknowledgment

### Determine Patient Status
**When:** User wants to book an appointment
**Action:** Agent asks if they are a new or established patient
**Example:** Hello! Are you a new patient with us or an established one?

### Acknowledge Patient Status
**When:** After determining patient status
**Action:** Agent acknowledges the customer's status before requesting information
**Example:** Okay, an established patient. Thank you for letting me know.

## Identity Verification & Chart Preparation

### Identify Established Patient
**When:** Patient is established
**Action:** Agent asks for their phone number or date of birth to pull up their chart
**Example:** To access your chart, could you please provide your phone number or your date of birth?

### Inform of Chart Retrieval
**When:** After receiving patient identification
**Action:** Agent informs the customer they will pull up the chart and may take a moment or place them on hold
**Example:** Thank you. I'm pulling up your chart now, which may take a moment. Please bear with me.

## Appointment Details & Scheduling

### Inquire Appointment Reason
**When:** After retrieving an established patient's chart
**Action:** Agent asks for the specific reason or type of appointment
**Example:** Now that I have your chart open, what brings you in today? What type of appointment are you looking to schedule?

### Gather Scheduling Preferences
**When:** After the patient specifies the reason for the appointment
**Action:** Agent asks for preferred location (if not established) and preferred days and times
**Example:** For this appointment, do you have a preferred location, and what days and times are most convenient for you?

### Confirm Scheduling Preferences
**When:** After gathering initial scheduling preferences (location, days, times) from the user.
**Action:** The agent explicitly confirms the gathered preferences with the user to ensure accuracy before proceeding with the search.
**Example:** Just to confirm, you're looking for an appointment at our Downtown location, on a weekday, sometime in the late afternoon. Is that correct?

### Inform of Availability Check
**When:** After confirming the user's scheduling preferences.
**Action:** The agent informs the user that they are checking for availability and may ask them to hold briefly.
**Example:** Okay, I'll check our schedule for those preferences. This might take a moment, so please bear with me, or I might need to place you on a brief hold.

### Present Appointment Options
**When:** After checking for availability based on the confirmed preferences.
**Action:** The agent presents multiple specific appointment times and dates that match the user's preferences, allowing the user to choose.
**Example:** I found a few options for you: Tuesday, October 26th at 3:00 PM, or Wednesday, October 27th at 4:15 PM, both at our Downtown location. Do either of those work for you?
