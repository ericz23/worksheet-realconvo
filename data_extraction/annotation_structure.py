import enum
from typing import List, Optional
from pydantic import BaseModel, Field


class SpeakerType(str, enum.Enum):
    AGENT = "agent"
    CUSTOMER = "customer"


class DialogueAct(str, enum.Enum):
    provide_information = "provide_information"
    request_information = "request_information"
    question_open = "question_open"
    question_closed = "question_closed"
    confirm = "confirm"
    confirm_yes = "confirm_yes"
    confirm_no = "confirm_no"
    request_action = "request_action"
    propose_action = "propose_action"
    commit_action = "commit_action"
    greeting_opening = "greeting_opening"
    closing = "closing"
    apologize = "apologize"
    thanks = "thanks"
    acknowledge_backchannel = "acknowledge_backchannel"
    hold_or_transfer = "hold_or_transfer"


class SubTopicCategory(str, enum.Enum):
    PET_APPOINTMENT_SCHEDULING = "Pet Appointment Scheduling"
    DENTAL_APPOINTMENT_REQUESTS = "Dental Appointment Requests"
    OTHER_MEDICAL_APPOINTMENT_MANAGEMENT = "Other Medical Appointment Management"
    MEDICAL_PROCEDURE_INQUIRIES = "Medical Procedure Inquiries"
    BILLING_AND_PAYMENT_INQUIRIES = "Billing and Payment Inquiries"
    PET_INQUIRIES = "Pet Inquiries"
    OTHER = "Other"


class TranscriptSegment(BaseModel):
    turn_index: int = Field(..., ge=0)
    text: str
    speaker: SpeakerType
    confidence: float = Field(..., ge=0.0, le=1.0)
    dialogue_act: DialogueAct
    dialogue_act_confidence: float = Field(..., ge=0.0, le=1.0)


class ConversationLevel(BaseModel):
    summary: str
    actions_taken: str
    outcome: str
    sub_topic: SubTopicCategory


class LabeledConversation(BaseModel):
    id: Optional[int] = None
    source_zip: Optional[str] = None
    conversation: ConversationLevel
    segments: List[TranscriptSegment]