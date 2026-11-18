"""Task scoring that keeps invalid answers and failed calls visible."""


def evaluate(classify_fn, eval_set):
    rows = list(eval_set)
    if not rows:
        raise ValueError("An evaluation set must contain at least one case")
    labels = {"routine", "soon", "urgent"}
    for row in rows:
        if (
            not isinstance(row, (list, tuple))
            or len(row) != 2
            or not isinstance(row[0], str)
            or not row[0].strip()
            or not isinstance(row[1], str)
            or row[1] not in labels
        ):
            raise ValueError(
                "Each case needs non-empty text and a valid expected label"
            )
    counts = {"correct": 0, "wrong": 0, "invalid": 0, "error": 0}
    failures = []
    for index, (text, expected) in enumerate(rows):
        try:
            raw = classify_fn(text)
        except Exception:
            counts["error"] += 1
            failures.append({"case": index, "kind": "error"})
            continue
        predicted = raw.strip().lower() if isinstance(raw, str) else None
        kind = (
            "invalid"
            if predicted not in labels
            else "correct"
            if predicted == expected
            else "wrong"
        )
        counts[kind] += 1
        if kind != "correct":
            failures.append(
                {
                    "case": index,
                    "kind": kind,
                    "expected": expected,
                    "predicted": predicted,
                }
            )
    return {
        **counts,
        "total": len(rows),
        "accuracy": counts["correct"] / len(rows),
        "failures": failures,
    }
