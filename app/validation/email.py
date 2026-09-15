import re
from app.models.schemas import GeneratedEmail, MeetingAnalysis


def validate_email(email: GeneratedEmail, analysis: MeetingAnalysis, transcript: str) -> GeneratedEmail:
    warnings: list[str] = []
    body_lower = email.body.lower()
    for item in analysis.action_items:
        if item.action.lower() not in body_lower:
            warnings.append(f"Missing action item in email: {item.action}")
    transcript_lower = transcript.lower()
    for item in analysis.action_items:
        if item.action.lower() not in transcript_lower and item.action.lower() not in body_lower:
            warnings.append(f"Unsupported action item: {item.action}")
    for owner in analysis.owners:
        if owner.lower() not in body_lower:
            warnings.append(f"Missing owner in email: {owner}")
    for deadline in analysis.deadlines:
        if deadline.lower() not in body_lower:
            warnings.append(f"Missing deadline in email: {deadline}")
    return email.model_copy(update={"validation_passed": not warnings, "validation_warnings": warnings})
