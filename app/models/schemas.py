from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ActionStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    UNKNOWN = "UNKNOWN"


class EmailType(str, Enum):
    MEETING_FOLLOW_UP = "meeting follow-up"
    ACTION_ITEM_SUMMARY = "action item summary"
    MANAGEMENT_UPDATE = "management update"
    PROJECT_STATUS = "project status"
    CUSTOMER_FOLLOW_UP = "customer follow-up"
    TECHNICAL_DISCUSSION = "technical discussion summary"


class Tone(str, Enum):
    PROFESSIONAL = "professional"
    CONCISE = "concise"
    FORMAL = "formal"
    FRIENDLY = "friendly"


class ActionItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: str = Field(min_length=1, max_length=500)
    owner: str = Field(default="unknown", min_length=1, max_length=100)
    deadline: str = Field(default="unknown", min_length=1, max_length=100)
    status: ActionStatus = ActionStatus.OPEN


class MeetingAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str = Field(min_length=1, max_length=2_000)
    decisions: list[str] = Field(default_factory=list, max_length=20)
    action_items: list[ActionItem] = Field(default_factory=list, max_length=50)
    owners: list[str] = Field(default_factory=list, max_length=50)
    deadlines: list[str] = Field(default_factory=list, max_length=50)
    risks: list[str] = Field(default_factory=list, max_length=20)
    dependencies: list[str] = Field(default_factory=list, max_length=20)
    open_questions: list[str] = Field(default_factory=list, max_length=20)


class AnalyzeRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=30_000)

    @field_validator("transcript")
    @classmethod
    def transcript_must_contain_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("transcript must contain non-whitespace text")
        return value.strip()


class EmailRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=30_000)
    email_type: EmailType = EmailType.MEETING_FOLLOW_UP
    tone: Tone = Tone.PROFESSIONAL
    analysis: MeetingAnalysis | None = None

    @field_validator("transcript")
    @classmethod
    def transcript_must_contain_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("transcript must contain non-whitespace text")
        return value.strip()


class GeneratedEmail(BaseModel):
    subject: str
    body: str
    validation_passed: bool
    validation_warnings: list[str] = Field(default_factory=list)


class AnalyzeResponse(BaseModel):
    request_id: str
    processing_time_ms: float
    llm_latency_ms: float
    analysis: MeetingAnalysis
    email: GeneratedEmail
