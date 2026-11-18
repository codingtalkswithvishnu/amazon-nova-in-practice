# Chapter 11 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [csharp/knowledge_base/Program.cs](csharp/knowledge_base/Program.cs) | `dotnet run --project examples/11-grounding/csharp/knowledge_base -- --live` |
| [python/knowledge_base.py](python/knowledge_base.py) | `python examples/11-grounding/python/knowledge_base.py --live` |

`--live` permits a metered request. Configure AWS_REGION, AWS_PROFILE and an
approved NOVA_MODEL_ID first. Do not supply real patient data. Generated wording
can vary; check stop reason, output shape and source facts rather than exact text.

First create and ingest a Knowledge Base using fixtures/clinic_policy.md. Set
NOVA_KNOWLEDGE_BASE_ID and NOVA_GENERATION_MODEL_ARN to real supported resources.
The examples do not create them. Inspect retrieval and citation support; no-answer
and a failed retrieval are different outcomes. Delete any practice vector store,
source objects and other resources you created after finishing the exercise.

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.
