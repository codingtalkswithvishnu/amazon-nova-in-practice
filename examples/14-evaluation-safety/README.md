# Chapter 14 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [python/evaluate.py](python/evaluate.py) | `python examples/14-evaluation-safety/python/evaluate.py` |

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.

Run `python examples/14-evaluation-safety/python/evaluate.py` for the local demonstration. The optional `python/guardrails.py` example requires an existing published guardrail, NOVA_GUARDRAIL_ID, NOVA_GUARDRAIL_VERSION and explicit --live. This is a metered check; it does not create policies.
