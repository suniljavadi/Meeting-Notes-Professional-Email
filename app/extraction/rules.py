import re
from app.models.schemas import ActionItem, ActionStatus, MeetingAnalysis

_PERSON = r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?"
_DATE_VALUE = r"(?:today|tomorrow|next\s+(?:week|month)|(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)(?:\s+\d{1,2}(?:,\s*\d{4})?)?|\d{1,2}(?:st|nd|rd|th)?(?:,\s*\d{4})?)"
_DEADLINE = rf"\b(?:by|before|on|due(?:\s+by)?)\b\s+({_DATE_VALUE})"


def _sentences(text: str) -> list[str]:
    return [part.strip(" -\t") for part in re.split(r"(?:\n+|(?<=[.!?])\s+)", text) if part.strip()]


def _deadline(sentence: str) -> str:
    match = re.search(_DEADLINE, sentence, re.IGNORECASE)
    return match.group(1).strip(" .") if match else "unknown"


def _owner(sentence: str) -> str:
    match = re.search(rf"\b(?:by|owner\s*:\s*)({_PERSON})\b", sentence)
    if match:
        return match.group(1)
    match = re.search(rf"^({_PERSON})\s+(?:will|needs to|should|must)\b", sentence)
    return match.group(1) if match else "unknown"


def extract_meeting_facts(transcript: str) -> MeetingAnalysis:
    sentences = _sentences(transcript)
    actions: list[ActionItem] = []
    decisions: list[str] = []
    risks: list[str] = []
    dependencies: list[str] = []
    questions: list[str] = []
    owners: list[str] = []
    deadlines: list[str] = []

    for sentence in sentences:
        lower = sentence.lower()
        if re.search(r"\b(will|needs to|should|must|assigned|prepare|send|review|validate|confirm|test|complete|update)\b", lower):
            action_text = re.sub(r"^[\-•\s]+", "", sentence).rstrip(".")
            action_text = re.sub(r"\bby\s+[A-Za-z]+(?:\s+\d{1,2}(?:,\s*\d{4})?)?\b", "", action_text, flags=re.I).strip()
            action_text = re.sub(r"\s+", " ", action_text).rstrip(" .")
            if action_text and not any(item.action.lower() == action_text.lower() for item in actions):
                item = ActionItem(action=action_text, owner=_owner(sentence), deadline=_deadline(sentence))
                actions.append(item)
                if item.owner != "unknown": owners.append(item.owner)
                if item.deadline != "unknown": deadlines.append(item.deadline)
        if re.search(r"\b(decided|agreed|approved|will proceed|selected|confirmed)\b", lower):
            decisions.append(sentence.rstrip("."))
        if re.search(r"\b(risk|risks|may move|delay|blocked|blocker|concern|uncertain|could fail)\b", lower):
            risks.append(sentence.rstrip("."))
        if re.search(r"\b(depends on|dependency|needs .* to|waiting for|requires)\b", lower):
            dependencies.append(sentence.rstrip("."))
        if "?" in sentence or re.search(r"\b(need confirmation|open question|clarify|confirm whether)\b", lower):
            questions.append(sentence.rstrip("."))

    unique = lambda values: list(dict.fromkeys(values))
    summary = " ".join(sentences[:3]) if sentences else "No meeting content was provided."
    return MeetingAnalysis(
        summary=summary,
        decisions=unique(decisions), action_items=actions, owners=unique(owners),
        deadlines=unique(deadlines), risks=unique(risks), dependencies=unique(dependencies),
        open_questions=unique(questions),
    )
