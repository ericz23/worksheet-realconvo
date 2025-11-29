# Conversation Tree

- Agent: Thank you for calling [ORGANIZATION]. How can I assist you today?
User: Hi, I’d like to book a medical appointment.
  - Agent: Okay. Are you an established patient or would you be a new one?
User: I'm an established patient.
    - Agent: Okay, fantastic. Could you provide your phone number so I can pull up your chart?
User: Yes.
      - Agent: Okay, give me a moment as I pull up your chart. Thank you.
User: [PHONE_NUMBER]
        - Agent: Okay. What type of medical appointment are you looking to book?
User: I need a routine check-up and I also wanted to discuss some headaches I've been having.
        - Agent: Okay. What type of medical appointment are you looking to book?
User: I'd like to schedule an appointment for my [MEDICAL_CONDITION]. It's been bothering me for a few days.
        - Agent: Okay. What type of medical appointment are you looking to book?
User: I need a follow-up appointment for my [MEDICAL_PROCESS] procedure.
      - Agent: Okay, give me a moment as I pull up your chart. Thank you.
User: Okay, thanks.
        - Agent: Okay, what would you be coming in for today?
User: I need an annual check-up.
        - Agent: Okay, what would you be coming in for today?
User: I've been having some stomach pain lately.
        - Agent: Okay, what would you be coming in for today?
User: I wanted to discuss some lab results.
      - Agent: Okay, give me a moment as I pull up your chart. Thank you.
User: I need to schedule a follow-up appointment.
        - Agent: All right. And what would you be coming in for?
User: It's for my annual check-up.
        - Agent: All right. And what would you be coming in for?
User: I need a follow-up on my recent lab results.
        - Agent: All right. And what would you be coming in for?
User: It's for a check-up regarding my medication.
    - Agent: Okay, fantastic. Could you provide your phone number so I can pull up your chart?
User: Sure, it's [PHONE_NUMBER].
      - Agent: Okay, thank you. Please give me just a moment while I pull up your chart. I'll be right back.
User: Okay.
        - Agent: Okay, thank you for holding. Now that I have your chart pulled up, you mentioned you'd like to book a medical appointment. What type of appointment were you looking to schedule today?
User: I'd like to schedule a general check-up.
        - Agent: Okay, thank you for holding. Now that I have your chart pulled up, you mentioned you'd like to book a medical appointment. What type of appointment were you looking to schedule today?
User: I need to book a follow-up appointment.
        - Agent: Okay, thank you for holding. Now that I have your chart pulled up, you mentioned you'd like to book a medical appointment. What type of appointment were you looking to schedule today?
User: I've been experiencing some new symptoms and would like to schedule a consultation.
      - Agent: Okay, thank you. Please give me just a moment while I pull up your chart. I'll be right back.
User: Alright.
        - Agent: Thank you for holding. You mentioned you want to book a medical appointment. What type of appointment are you looking to schedule today?
User: I'd like to schedule my annual physical.
        - Agent: Thank you for holding. You mentioned you want to book a medical appointment. What type of appointment are you looking to schedule today?
User: I need a follow-up appointment for my medication.
        - Agent: Thank you for holding. You mentioned you want to book a medical appointment. What type of appointment are you looking to schedule today?
User: I've been experiencing some new symptoms and wanted to get them checked out.
      - Agent: Okay, thank you. Please give me just a moment while I pull up your chart. I'll be right back.
User: No problem.
        - Agent: [PERSON_NAME], you mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: No, it's actually for a skin rash I've developed.
        - Agent: [PERSON_NAME], you mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: Yes, but I also wanted to ask about some recent [MEDICAL_CONDITION] symptoms I've been having.
        - Agent: [PERSON_NAME], you mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: No, I need to get my annual check-up done and talk about a [MEDICAL_CONDITION].
    - Agent: Okay, fantastic. Could you provide your phone number so I can pull up your chart?
User: Of course. My number is [PHONE_NUMBER].
      - Agent: Okay, thank you. Please give me a moment while I pull up your chart.
User: Okay.
        - Agent: Okay, thank you. Now that I have your chart pulled up, what type of appointment are you looking to schedule today?
User: I need to schedule an annual physical, and I also have a new rash I'd like to get checked.
        - Agent: Okay, thank you. Now that I have your chart pulled up, what type of appointment are you looking to schedule today?
User: I've been experiencing some chest pain, and I need to see a doctor about it as soon as possible.
        - Agent: Okay, thank you. Now that I have your chart pulled up, what type of appointment are you looking to schedule today?
User: I'm due for my routine check-up, and I also wanted to discuss my blood pressure.
      - Agent: Okay, thank you. Please give me a moment while I pull up your chart.
User: Sure.
        - Agent: Okay, you mentioned you'd like to book a medical appointment. Was it for a specific medical process?
User: Yes, I need to schedule my annual physical check-up.
        - Agent: Okay, you mentioned you'd like to book a medical appointment. Was it for a specific medical process?
User: I'd like to make an appointment for a flu shot.
        - Agent: Okay, you mentioned you'd like to book a medical appointment. Was it for a specific medical process?
User: Well, I'm not sure about a specific process, but I've been having some [SYMPTOM] and I'd like to get it checked out.
      - Agent: Okay, thank you. Please give me a moment while I pull up your chart.
User: No problem.
        - Agent: [PERSON_NAME], you mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: Yes, that's right.
        - Agent: [PERSON_NAME], you mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: No, it's actually for something else. I need to get my [MEDICAL_PROCESS] checked.
        - Agent: [PERSON_NAME], you mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: Yes, for that, and I also wanted to talk about a persistent [MEDICAL_CONDITION].
  - Agent: Okay. Are you an established patient or would you be a new one?
User: I'm a new patient.
    - Agent: Okay, so this is the first time patient. Do you have dental insurance?
User: I do, yes.
      - Agent: What is the name of your insurance?
User: It's [ORGANIZATION] Health.
        - Agent: Okay, and is that a PPO or an HMO plan?
User: I'm not sure. I think it's a PPO.
        - Agent: Okay, and is that a PPO or an HMO plan?
User: I'm not sure about that. I'd have to check my card.
        - Agent: Okay, and is that a PPO or an HMO plan?
User: Can you repeat that, please?
      - Agent: What is the name of your insurance?
User: I have [ORGANIZATION] Medical Benefits.
        - Agent: Okay. Is that a PPO or an HMO plan?
User: I believe it's a PPO plan.
        - Agent: Okay. Is that a PPO or an HMO plan?
User: I'm not sure. I'd have to check my insurance card.
        - Agent: Okay. Is that a PPO or an HMO plan?
User: I'm not certain, I'll need to look that up.
      - Agent: What is the name of your insurance?
User: Oh, let me just check my insurance card. One moment please.
        - Agent: Okay.
User: Okay, it's [ORGANIZATION] [ORGANIZATION].
        - Agent: Okay.
User: My insurance is [ORGANIZATION].
        - Agent: Okay.
User: I have [ORGANIZATION] [ORGANIZATION] insurance.
    - Agent: Okay, so this is the first time patient. Do you have dental insurance?
User: Yes, it's [ORGANIZATION] [ORGANIZATION].
      - Agent: Okay, perfect. Do you know if it is PPO or hmo?
User: I believe it's a PPO plan.
        - Agent: Okay. All right, great. When were you thinking of coming in if you have an appointment?
User: I'm not sure, what's your earliest availability?
        - Agent: Okay. All right, great. When were you thinking of coming in if you have an appointment?
User: I don't know how soon you have openings.
        - Agent: Okay. All right, great. When were you thinking of coming in if you have an appointment?
User: As soon as possible.
      - Agent: Okay, perfect. Do you know if it is PPO or hmo?
User: I'm not sure, I'd have to check my insurance card.
        - Agent: Okay, no problem. I can hold while you check your card. Do you know if you're assigned to this office?
User: I'm not sure about that either, I'll check my card.
        - Agent: Okay, no problem. I can hold while you check your card. Do you know if you're assigned to this office?
User: I'll have to check my insurance card for both of those details.
        - Agent: Okay, no problem. I can hold while you check your card. Do you know if you're assigned to this office?
User: What do you mean by 'assigned to this office'?
      - Agent: Okay, perfect. Do you know if it is PPO or hmo?
User: Yes, it's PPO.
        - Agent: Okay. All right, great. When were you thinking of coming in if you have an appointment?
User: I'm not sure, what do you have available?
        - Agent: Okay. All right, great. When were you thinking of coming in if you have an appointment?
User: As soon as possible.
        - Agent: Okay. All right, great. When were you thinking of coming in if you have an appointment?
User: Sometime next week would be great.
    - Agent: Okay, so this is the first time patient. Do you have dental insurance?
User: No, I don't.
      - Agent: Okay.
User: Okay.
        - Agent: Okay. And what days and times are you looking for?
User: I'm looking for something in the afternoon, maybe next week.
        - Agent: Okay. And what days and times are you looking for?
User: What days and times do you have available?
        - Agent: Okay. And what days and times are you looking for?
User: I'm pretty flexible, do you have anything open next week?
      - Agent: Okay.
User: So, what's the next step?
        - Agent: Okay. No problem. This appointment is going to be just for you or also for family members?
User: Just for me.
        - Agent: Okay. No problem. This appointment is going to be just for you or also for family members?
User: Just for me, please.
        - Agent: Okay. No problem. This appointment is going to be just for you or also for family members?
User: It's just for me.
      - Agent: Okay.
User: Can I still make an appointment?
        - Agent: Yes, of course.
User: Great, how can I book one?
        - Agent: Yes, of course.
User: Okay, when are you available?
        - Agent: Yes, of course.
User: Perfect, I'd like to schedule an appointment then.
  - Agent: Okay. Are you an established patient or would you be a new one?
User: I'm an existing patient.
    - Agent: What's your date of birth?
User: [DATE_OF_BIRTH]
      - Agent: Okay, and what would you be coming in for?
User: I'd like to schedule an annual physical.
        - Agent: Okay. And you usually come to our [ORGANIZATION] office?
User: Yes, that's correct.
        - Agent: Okay. And you usually come to our [ORGANIZATION] office?
User: Yes, that's my usual office. Do you have any appointments available there?
        - Agent: Okay. And you usually come to our [ORGANIZATION] office?
User: I think so, but I'm not entirely sure. When was my last visit?
      - Agent: Okay, and what would you be coming in for?
User: I have been experiencing a cough and sore throat.
        - Agent: Okay. And do you usually come to our [ORGANIZATION] office?
User: Yes, I usually come to this office.
        - Agent: Okay. And do you usually come to our [ORGANIZATION] office?
User: Yes, I do.
        - Agent: Okay. And do you usually come to our [ORGANIZATION] office?
User: No, I usually go to your [OTHER_LOCATION] office.
      - Agent: Okay, and what would you be coming in for?
User: I need a follow-up for my recent blood work.
        - Agent: Okay. And which office do you usually come to?
User: I usually go to the [OFFICE_LOCATION] office.
        - Agent: Okay. And which office do you usually come to?
User: I'm not entirely sure, could you please check my records?
        - Agent: Okay. And which office do you usually come to?
User: I don't remember, can you tell me which office I visited last time?
    - Agent: What's your date of birth?
User: It's [DATE_OF_BIRTH]
      - Agent: Okay, and your first and last name please?
User: [PERSON_NAME] [PERSON_NAME].
        - Agent: Okay, one moment while I pull up your file.
User: I'd like to schedule an annual check-up.
        - Agent: Okay, one moment while I pull up your file.
User: I'm looking to book a follow-up appointment.
        - Agent: Okay, one moment while I pull up your file.
User: Okay, thank you.
      - Agent: Okay, and your first and last name please?
User: My name is [PERSON_NAME] [PERSON_NAME].
        - Agent: Okay, thank you. One moment while I pull up your information.
User: Okay, thanks.
        - Agent: Okay, thank you. One moment while I pull up your information.
User: I'm calling about my annual check-up.
        - Agent: Okay, thank you. One moment while I pull up your information.
User: Sure. I'm hoping to schedule a check-up, and I was wondering if [PERSON_NAME] is still practicing there?
      - Agent: Okay, and your first and last name please?
User: Sure, it's [PERSON_NAME] [PERSON_NAME].
        - Agent: Okay, one moment while I pull up your record.
User: Okay. I'd like to schedule an annual check-up.
        - Agent: Okay, one moment while I pull up your record.
User: Alright. I'm hoping to see if [PERSON_NAME] has any availability next week.
        - Agent: Okay, one moment while I pull up your record.
User: Thank you. I need to schedule a follow-up for my [MEDICAL_CONDITION].
    - Agent: What's your date of birth?
User: My date of birth is [DATE_OF_BIRTH]
      - Agent: And your first and last name?
User: [PERSON_NAME] [PERSON_NAME]
        - Agent: Okay, one moment while I pull up your information.
User: I'd like to schedule my annual check-up.
        - Agent: Okay, one moment while I pull up your information.
User: Okay, do you see any appointments available for a follow-up?
        - Agent: Okay, one moment while I pull up your information.
User: I need to book an appointment for a new prescription.
      - Agent: And your first and last name?
User: Sure, it's [PERSON_NAME] [PERSON_NAME].
        - Agent: Okay, one moment while I look up your information.
User: Okay.
        - Agent: Okay, one moment while I look up your information.
User: I'm looking to book a general check-up.
        - Agent: Okay, one moment while I look up your information.
User: Sure, take your time.
      - Agent: And your first and last name?
User: My name is [PERSON_NAME] [PERSON_NAME].
        - Agent: Okay, one second.
User: Okay.
        - Agent: Okay, one second.
User: Sure, I'll wait.
        - Agent: Okay, one second.
User: No problem, take your time.
