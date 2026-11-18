"""Local structural checks for a small Nova conversation-format SFT example."""

import json


def read_records(path):
    records = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        try:
            record = json.loads(line)
            if not isinstance(record, dict) or not isinstance(
                record.get("schemaVersion"), str
            ):
                raise ValueError("Missing conversation schemaVersion")
            messages = record.get("messages")
            if not isinstance(messages, list) or len(messages) < 2:
                raise ValueError("Need user and assistant turns")
            for index, message in enumerate(messages):
                expected = "user" if index % 2 == 0 else "assistant"
                if message.get("role") != expected:
                    raise ValueError("Turns must alternate user and assistant")
                content = message.get("content")
                if (
                    not isinstance(content, list)
                    or not content
                    or not all(
                        isinstance(b, dict)
                        and isinstance(b.get("text"), str)
                        and b["text"].strip()
                        for b in content
                    )
                ):
                    raise ValueError("Text example needs non-empty content")
            if messages[-1]["role"] != "assistant":
                raise ValueError("Last turn must be an assistant target")
        except (ValueError, TypeError, AttributeError) as exc:
            raise ValueError(f"Invalid training record at line {number}") from exc
        records.append(record)
    if not records:
        raise ValueError("Dataset is empty")
    return records
