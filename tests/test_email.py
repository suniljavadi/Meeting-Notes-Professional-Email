from app.models.schemas import EmailType, Tone
from app.services.email import generate_email
from app.validation.email import validate_email
from app.extraction.rules import extract_meeting_facts


def test_email_contains_all_actions_and_unknowns():
    analysis = extract_meeting_facts("Sunil will prepare the checklist by Friday. Database team needs to validate indexes.")
    email = validate_email(generate_email(analysis, EmailType.MEETING_FOLLOW_UP, Tone.PROFESSIONAL), analysis, "Sunil will prepare the checklist by Friday. Database team needs to validate indexes.")
    assert "Sunil will prepare the checklist" in email.body
    assert "Owner: unknown" in email.body
    assert "Deadline: Friday" in email.body
    assert email.validation_passed


def test_generation_supports_types_and_tones():
    analysis = extract_meeting_facts("The team agreed to ship on Monday.")
    email = generate_email(analysis, EmailType.MANAGEMENT_UPDATE, Tone.FORMAL)
    assert email.subject == "Management update"
    assert "Regards" in email.body
