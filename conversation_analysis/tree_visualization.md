# Conversation Tree

- Agent: Thank you for calling [ORGANIZATION]. How can I assist you today?
User: Hi, I’d like to book a medical appointment.
  - Agent: Okay. Are you a new patient or an established patient?
User: I'm a new patient.
    - Agent: Okay, do you have any dental insurance?
User: Yes, I do have dental insurance.
      - Agent: What is the name of your insurance?
User: I have [ORGANIZATION] dental insurance.
        - Agent: Okay, we take that insurance. Is it a PPO or HMO plan?
User: It's a PPO plan.
        - Agent: Okay, we take that insurance. Is it a PPO or HMO plan?
User: I have an HMO plan.
        - Agent: Okay, we take that insurance. Is it a PPO or HMO plan?
User: I'm not sure if it's PPO or HMO.
      - Agent: What is the name of your insurance?
User: I'm sorry, could you repeat that?
        - Agent: What is the name of your insurance?
User: It's Delta Dental.
        - Agent: What is the name of your insurance?
User: My insurance is Aetna.
        - Agent: What is the name of your insurance?
User: I have Cigna Dental.
      - Agent: What is the name of your insurance?
User: I think it's [ORGANIZATION] but I'll have to double check.
        - Agent: Okay, [ORGANIZATION]. Is that a PPO or an HMO plan?
User: I believe it's a PPO plan.
        - Agent: Okay, [ORGANIZATION]. Is that a PPO or an HMO plan?
User: It's an HMO plan.
        - Agent: Okay, [ORGANIZATION]. Is that a PPO or an HMO plan?
User: I'm not sure, I'd have to check my card.
    - Agent: Okay, do you have any dental insurance?
User: Yes, I have [ORGANIZATION] dental.
      - Agent: Okay, perfect. Do you know if it is PPO or hmo?
User: I believe it's a PPO plan.
        - Agent: Okay. All right, great. When were you thinking of coming in if you have an appointment?
User: I'm not sure, what do you have available?
        - Agent: Okay. All right, great. When were you thinking of coming in if you have an appointment?
User: I'm hoping to come in sometime next week.
        - Agent: Okay. All right, great. When were you thinking of coming in if you have an appointment?
User: I'm pretty flexible, whenever you have an opening.
      - Agent: Okay, perfect. Do you know if it is PPO or hmo?
User: I think it's an HMO plan.
        - Agent: Okay. At the moment we're not contracted with any HMO plans.
User: Oh, I see. I might be mistaken then, I'll need to double check if it's PPO.
        - Agent: Okay. At the moment we're not contracted with any HMO plans.
User: Okay, so you don't accept HMO plans. Do you only accept PPO?
        - Agent: Okay. At the moment we're not contracted with any HMO plans.
User: Oh, that's unfortunate. I'm pretty sure it's an HMO.
      - Agent: Okay, perfect. Do you know if it is PPO or hmo?
User: I'm not sure if it's PPO or HMO. How can I find that out?
        - Agent: Okay. That information is typically on your insurance card, or you can check the [ORGANIZATION] website for your plan. Do you know if you're assigned to this office?
User: I don't know if I'm assigned to this office.
        - Agent: Okay. That information is typically on your insurance card, or you can check the [ORGANIZATION] website for your plan. Do you know if you're assigned to this office?
User: I'm not sure about that either. I'll need to check my card for the assignment as well.
        - Agent: Okay. That information is typically on your insurance card, or you can check the [ORGANIZATION] website for your plan. Do you know if you're assigned to this office?
User: Assigned? I'm not sure. How would I find that out?
    - Agent: Okay, do you have any dental insurance?
User: No, I don't have dental insurance.
      - Agent: Okay. What is the reason for your visit today?
User: I'd like to schedule a general physical check-up.
        - Agent: Okay, a general physical check-up. I can help you with that.
User: Great, what are your next available appointments?
        - Agent: Okay, a general physical check-up. I can help you with that.
User: Okay, do you have any openings next week?
        - Agent: Okay, a general physical check-up. I can help you with that.
User: Perfect, just let me know what works for you.
      - Agent: Okay. What is the reason for your visit today?
User: I've been experiencing some chest pain and wanted to get it looked at.
        - Agent: Okay. We'll definitely want to get that looked at for you. What day and time works best for your appointment?
User: I'm available on Tuesday mornings, or Friday afternoons work for me too.
        - Agent: Okay. We'll definitely want to get that looked at for you. What day and time works best for your appointment?
User: I'm pretty flexible, do you have anything available next week?
        - Agent: Okay. We'll definitely want to get that looked at for you. What day and time works best for your appointment?
User: What's the earliest you have an opening?
      - Agent: Okay. What is the reason for your visit today?
User: I'm looking to establish care with a new primary care doctor.
        - Agent: Okay. And this appointment is going to be just for you or also for family members?
User: Just for me.
        - Agent: Okay. And this appointment is going to be just for you or also for family members?
User: It's for me and my child.
        - Agent: Okay. And this appointment is going to be just for you or also for family members?
User: It's for my spouse, not for me.
  - Agent: Okay. Are you a new patient or an established patient?
User: I'm an established patient.
    - Agent: Okay, fantastic. Could you provide your phone number so I can pull up your chart?
User: [PHONE_NUMBER]
      - Agent: Okay, give me moment as I pull up your chart. Give me one moment please. I'll be right back on the line with you. Thank you.
User: Okay.
        - Agent: You mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: Yes, that's what I called about.
        - Agent: You mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: No, it's actually for an annual physical.
        - Agent: You mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: No, I wanted to discuss a new [SYMPTOM] I've been experiencing.
      - Agent: Okay, give me moment as I pull up your chart. Give me one moment please. I'll be right back on the line with you. Thank you.
User: Sounds good.
        - Agent: You mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: Yes, that's correct.
        - Agent: You mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: No, it's actually for a follow-up on my [MEDICAL_CONDITION].
        - Agent: You mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: It's not for that specific reason. I need to schedule an appointment for my yearly check-up and I also have a [MEDICAL_PROCESS] concern.
      - Agent: Okay, give me moment as I pull up your chart. Give me one moment please. I'll be right back on the line with you. Thank you.
User: Alright, I'll wait.
        - Agent: Okay, I have your chart here. You mentioned you'd like to book a medical appointment. What kind of appointment are you looking to schedule today?
User: I'd like to schedule a routine check-up, please.
        - Agent: Okay, I have your chart here. You mentioned you'd like to book a medical appointment. What kind of appointment are you looking to schedule today?
User: I'm experiencing some [MEDICAL_CONDITION] symptoms and would like to get it checked out.
        - Agent: Okay, I have your chart here. You mentioned you'd like to book a medical appointment. What kind of appointment are you looking to schedule today?
User: I need to schedule a follow-up appointment for my [MEDICAL_PROCESS].
    - Agent: Okay, fantastic. Could you provide your phone number so I can pull up your chart?
User: Yes, it's [PHONE_NUMBER].
      - Agent: Okay, give me a moment as I pull up your chart. I'll be right back on the line with you. Thank you.
User: Okay.
        - Agent: Okay, you mentioned you'd like to book a medical appointment. What type of appointment are you looking to schedule?
User: I'd like to schedule my annual check-up.
        - Agent: Okay, you mentioned you'd like to book a medical appointment. What type of appointment are you looking to schedule?
User: I've been having some [SYMPTOM] and would like to get it checked.
        - Agent: Okay, you mentioned you'd like to book a medical appointment. What type of appointment are you looking to schedule?
User: I need a follow-up appointment for my [MEDICAL_CONDITION].
      - Agent: Okay, give me a moment as I pull up your chart. I'll be right back on the line with you. Thank you.
User: Sure, I'll wait.
        - Agent: [PERSON_NAME], you mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: Yes, that's correct. It's for [MEDICAL_PROCESS].
        - Agent: [PERSON_NAME], you mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: No, it's not for [MEDICAL_PROCESS]. I actually need to come in for a general check-up and discuss a [MEDICAL_CONDITION].
        - Agent: [PERSON_NAME], you mentioned you want to make an appointment. Was it for [MEDICAL_PROCESS]?
User: It's not for [MEDICAL_PROCESS]. I'd like to schedule an annual physical and I also have a [MEDICAL_CONDITION] I wanted to ask about.
      - Agent: Okay, give me a moment as I pull up your chart. I'll be right back on the line with you. Thank you.
User: Thanks.
        - Agent: Thank you for holding. You mentioned you want to make an appointment. Was it for a specific type of medical process or a general check-up?
User: I'd like to schedule an annual check-up, please.
        - Agent: Thank you for holding. You mentioned you want to make an appointment. Was it for a specific type of medical process or a general check-up?
User: I need to come in for a follow-up on my [MEDICAL_PROCESS].
        - Agent: Thank you for holding. You mentioned you want to make an appointment. Was it for a specific type of medical process or a general check-up?
User: It's for a general check-up, but I also wanted to ask about a persistent headache.
    - Agent: Okay, fantastic. Could you provide your phone number so I can pull up your chart?
User: Sure, my number is [PHONE_NUMBER].
      - Agent: Okay, give me a moment as I pull up your chart. Give me one moment please. I'll be right back on the line with you. Thank you.
User: Okay.
        - Agent: Okay, thank you for waiting. You mentioned you want to book a medical appointment. Was it for a specific type of visit or department?
User: Yes, I need to schedule my annual physical.
        - Agent: Okay, thank you for waiting. You mentioned you want to book a medical appointment. Was it for a specific type of visit or department?
User: I'd like to get a recurring [MEDICAL_CONDITION] checked out.
        - Agent: Okay, thank you for waiting. You mentioned you want to book a medical appointment. Was it for a specific type of visit or department?
User: I'm having some pain in my [BODY_PART] and I need to see a [OCCUPATION].
      - Agent: Okay, give me a moment as I pull up your chart. Give me one moment please. I'll be right back on the line with you. Thank you.
User: Sure, I'll hold.
        - Agent: Okay, you mentioned you want to book a medical appointment. What kind of appointment are you looking for?
User: I'd like to schedule an annual physical exam, please.
        - Agent: Okay, you mentioned you want to book a medical appointment. What kind of appointment are you looking for?
User: I'm having some [SYMPTOM] and I'd like to get it checked out.
        - Agent: Okay, you mentioned you want to book a medical appointment. What kind of appointment are you looking for?
User: I need a refill for my [DRUG] prescription.
      - Agent: Okay, give me a moment as I pull up your chart. Give me one moment please. I'll be right back on the line with you. Thank you.
User: No problem, I can wait.
        - Agent: Thank you for holding. You mentioned you want to make an appointment. What kind of appointment are you looking to schedule?
User: I need to schedule an annual physical.
        - Agent: Thank you for holding. You mentioned you want to make an appointment. What kind of appointment are you looking to schedule?
User: I'd like to book an appointment for a specific medical concern, like a persistent cough.
        - Agent: Thank you for holding. You mentioned you want to make an appointment. What kind of appointment are you looking to schedule?
User: I need to schedule a follow-up appointment with Dr. [PERSON_NAME].
