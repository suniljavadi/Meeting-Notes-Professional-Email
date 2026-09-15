from fastapi import APIRouter, HTTPException
from app.config.settings import get_settings
from app.models.schemas import AnalyzeRequest, EmailRequest
from app.services.pipeline import analyze_and_generate, generate_only

router = APIRouter()


@router.post("/analyze")
def analyze(request: AnalyzeRequest):
    settings = get_settings()
    if len(request.transcript) > settings.max_transcript_chars:
        raise HTTPException(status_code=413, detail="transcript is too long")
    return analyze_and_generate(request.transcript, settings, "meeting follow-up", "professional")


@router.post("/generate-email")
def generate_email_endpoint(request: EmailRequest):
    settings = get_settings()
    if len(request.transcript) > settings.max_transcript_chars:
        raise HTTPException(status_code=413, detail="transcript is too long")
    return generate_only(request, settings)
