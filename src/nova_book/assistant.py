"""Offline Chapter 15 design exercise; injected services stand in for cloud calls.

This teaches routing states, not clinical triage or a deployable patient service.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Draft:
    state: str
    reason: str
    answer: str | None = None
    sources: tuple[str, ...] = ()


def policy_question(question, *, authorised, check_content, classify, retrieve):
    if not authorised:
        return Draft("rejected", "access_denied")
    if not isinstance(question, str) or not question.strip():
        return Draft("rejected", "invalid_input")
    try:
        allowed = check_content(question)
    except Exception:
        return Draft("needs_staff", "content_check_failed")
    if allowed is not True:
        return Draft("needs_staff", "content_blocked")
    try:
        label = classify(question)
    except Exception:
        return Draft("needs_staff", "classification_failed")
    if label != "routine":
        return Draft("needs_staff", "urgency_or_uncertainty")
    try:
        result = retrieve(question)
    except Exception:
        return Draft("needs_staff", "retrieval_failed")
    if not isinstance(result, dict):
        return Draft("needs_staff", "invalid_retrieval")
    answer, sources = result.get("answer"), result.get("sources")
    if (
        not isinstance(answer, str)
        or not answer.strip()
        or not isinstance(sources, list)
        or not sources
        or not all(isinstance(s, str) and s.strip() for s in sources)
    ):
        return Draft("needs_staff", "missing_evidence")
    try:
        allowed = check_content(answer)
    except Exception:
        return Draft("needs_staff", "output_check_failed")
    if allowed is not True:
        return Draft("needs_staff", "output_blocked")
    # Sources are inspectable references, not a proof that the answer is true.
    return Draft("draft_ready", "staff_review_required", answer, tuple(sources))
