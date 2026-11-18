# Assistant states

The offline example demonstrates received -> draft_ready or needs_staff outcomes.
It is a design exercise with injected dependencies; it does not deploy an API,
store patient records, book appointments or perform validated clinical triage.

A draft with sources still requires staff to check whether the sources support it.
Authorization runs before retrieval. Blocked/urgent/uncertain/failed checks cannot
fall through to an automatic routine answer.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.

Run `python examples/15-assistant-design/python/demo.py` for the offline state example. Expected state: draft_ready; staff review remains required.
