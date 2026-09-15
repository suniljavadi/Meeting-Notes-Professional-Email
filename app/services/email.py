from app.models.schemas import EmailType, GeneratedEmail, MeetingAnalysis, Tone


def generate_email(analysis: MeetingAnalysis, email_type: EmailType, tone: Tone) -> GeneratedEmail:
    greeting = "Hello team," if tone != Tone.FRIENDLY else "Hi team,"
    closing = "Regards," if tone in (Tone.FORMAL, Tone.PROFESSIONAL) else "Thanks,"
    subject_prefix = {
        EmailType.MEETING_FOLLOW_UP: "Meeting follow-up",
        EmailType.ACTION_ITEM_SUMMARY: "Action items",
        EmailType.MANAGEMENT_UPDATE: "Management update",
        EmailType.PROJECT_STATUS: "Project status update",
        EmailType.CUSTOMER_FOLLOW_UP: "Customer follow-up",
        EmailType.TECHNICAL_DISCUSSION: "Technical discussion summary",
    }[email_type]
    lines = [greeting, "", f"Thank you for the discussion. {analysis.summary}"]
    if analysis.decisions:
        lines += ["", "Decisions:"] + [f"- {item}" for item in analysis.decisions]
    if analysis.action_items:
        lines += ["", "Action items:"]
        for item in analysis.action_items:
            lines.append(f"- {item.action} | Owner: {item.owner} | Deadline: {item.deadline} | Status: {item.status.value}")
    if analysis.risks:
        lines += ["", "Risks and open points:"] + [f"- {item}" for item in analysis.risks]
    if analysis.dependencies:
        lines += ["", "Dependencies:"] + [f"- {item}" for item in analysis.dependencies]
    if analysis.open_questions:
        lines += ["", "Open questions:"] + [f"- {item}" for item in analysis.open_questions]
    lines += ["", "Please let me know if anything needs correction.", "", closing, "[Your name]"]
    return GeneratedEmail(subject=subject_prefix, body="\n".join(lines), validation_passed=False)
