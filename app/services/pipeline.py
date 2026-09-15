import time
import uuid
from app.config.settings import Settings
from app.llm.provider import get_provider
from app.models.schemas import AnalyzeResponse, EmailRequest
from app.services.cleaning import clean_transcript
from app.services.email import generate_email
from app.validation.email import validate_email


def analyze_and_generate(transcript: str, settings: Settings, email_type, tone) -> AnalyzeResponse:
    request_id = str(uuid.uuid4())
    started = time.perf_counter()
    cleaned = clean_transcript(transcript)
    analysis, llm_latency = get_provider(settings).extract(cleaned)
    email = generate_email(analysis, email_type, tone)
    email = validate_email(email, analysis, cleaned)
    return AnalyzeResponse(request_id=request_id, processing_time_ms=(time.perf_counter() - started) * 1000,
                           llm_latency_ms=llm_latency, analysis=analysis, email=email)


def generate_only(request: EmailRequest, settings: Settings):
    cleaned = clean_transcript(request.transcript)
    analysis = request.analysis or get_provider(settings).extract(cleaned)[0]
    email = validate_email(generate_email(analysis, request.email_type, request.tone), analysis, cleaned)
    return email
