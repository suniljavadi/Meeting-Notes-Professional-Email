import re


def clean_transcript(transcript: str) -> str:
    """Normalize whitespace while preserving the transcript's factual wording."""
    text = transcript.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
