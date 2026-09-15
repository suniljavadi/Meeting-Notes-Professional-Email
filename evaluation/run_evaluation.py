import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.extraction.rules import extract_meeting_facts


def main():
    records = json.loads((Path(__file__).parent / "dataset.json").read_text())
    outputs = []
    for record in records:
        result = extract_meeting_facts(record["text"])
        outputs.append({"id": record["id"], "actions": len(result.action_items), "owners": result.owners, "deadlines": result.deadlines, "risks": len(result.risks)})
    print(json.dumps({"count": len(outputs), "results": outputs}, indent=2))


if __name__ == "__main__":
    main()
