# Chapter 11 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [csharp/knowledge_base/Program.cs](csharp/knowledge_base/Program.cs) | `dotnet run --project examples/11-grounding/csharp/knowledge_base -- --live` |
| [python/knowledge_base.py](python/knowledge_base.py) | `python examples/11-grounding/python/knowledge_base.py --live` |

`--live` permits a metered request. Configure AWS_REGION, AWS_PROFILE and an
approved NOVA_MODEL_ID first. Do not supply real patient data. Generated wording
can vary; inspect the answer, citations and source facts rather than exact text.
RetrieveAndGenerate does not expose the Converse response envelope or stop reason.

First create and ingest a Knowledge Base using fixtures/clinic_policy.md. Set
NOVA_KNOWLEDGE_BASE_ID and NOVA_GENERATION_MODEL_ARN to real supported resources.
The examples do not create them. Inspect retrieval and citation support; no-answer
and a failed retrieval are different outcomes. Delete any practice vector store,
source objects and other resources you created after finishing the exercise.

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.

## Manual preparation and expected observations

The chapter's S3 practice route uses a **customer-managed Knowledge Base** with a
selected vector store. AWS also offers and recommends
[Bedrock Managed Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-build-managed.html)
for managed storage and retrieval. Choose the route before creating resources;
this repository does not provision either one.

1. Read [the fictional policy](../../fixtures/clinic_policy.md) and upload it to a
   dedicated S3 prefix in the approved Region.
2. Follow the official [creation guide](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-create.html)
   with an authorised IAM identity, S3 source, supported embedding model, compatible
   vector store and required service role.
3. Sync the source and inspect the ingestion result. Re-sync after source changes.
4. In the console test panel, disable response generation and ask for Saturday
   opening hours. Inspect the actual retrieved passage and source. The policy
   states 09:00–13:00.
5. Enable generation with a supported Nova model/profile and compare the answer
   and citation with that passage. Configure NOVA_KNOWLEDGE_BASE_ID and
   NOVA_GENERATION_MODEL_ARN, then run the supplied Python or C# query example.
6. Ask about Sunday. The fixture does not provide that answer; a plausible invented
   schedule fails the check. A failed ingestion or denied request is an operational
   failure, not evidence that the policy lacks an answer.
7. Record outcomes and remove all exercise resources, including separately billed
   storage that deleting the Knowledge Base may leave behind.

Use AWS's [retrieval test guide](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve.html)
for current console controls. These instructions were documentation-reviewed;
provisioning, live retrieval, tenancy controls and answer quality were not exercised
in this repository's credential-free checks. In a product, enforce document access
before generation and keep source versions with the result. A citation is a route
to evidence, not proof that every generated statement is supported.
