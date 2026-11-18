# Validation boundaries

Reviewed: 18 November 2026.

Executed locally with Python 3.12.16 and .NET SDK 11.0.100 / runtime 11.0.0:
21 Python tests passed, 14 net11.0 C# projects built without warnings/errors,
and 11 C# contract checks passed. NuGet checks reported no deprecated, known
vulnerable or outdated direct/transitive packages in the two complete dependency
sets shared by the 14 projects. Python's locked dependency audit reported no known
vulnerabilities. These statements describe that check date, not future releases.

- Python: parse every source, Ruff lint/format, contract tests for complete answers,
  extraction, streaming, tool dispatch, job states, evaluation, decimal costs,
  conversation-format training records and assistant handoffs.
- C#: compile every project; execute the shared response/schema/tool-result checks.
- SDK contracts: request shapes are checked using the installed botocore service model.
- Dependencies: requirements.lock fixes the validated Python environment;
  packages.lock.json fixes every C# project's transitive packages. Dependency
  audit results are saved with the book's private review evidence.
- Publication: code is separate from the manuscript. The book links to the
  published source revision; link and EPUB checks are recorded with the book.

These are local and simulated checks. No live Bedrock, Knowledge Base, training,
S3 media generation, microphone, telephony or deployed application run is claimed.
The tiny synthetic fixtures establish teaching contracts, not production accuracy.
