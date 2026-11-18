"""Offline routing example, not a deployed or clinically validated assistant."""

from dataclasses import asdict

from nova_book.assistant import policy_question

result = policy_question(
    "What are the fictional clinic Saturday hours?",
    authorised=True,
    check_content=lambda text: True,
    classify=lambda text: "routine",
    retrieve=lambda text: {
        "answer": "Saturday 09:00–13:00",
        "sources": ["fictional-policy-demo-v1"],
    },
)
print(asdict(result))
