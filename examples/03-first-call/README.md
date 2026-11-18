# Chapter 3 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [csharp/first_call/Program.cs](csharp/first_call/Program.cs) | `dotnet run --project examples/03-first-call/csharp/first_call -- --live` |
| [csharp/usage/Program.cs](csharp/usage/Program.cs) | `dotnet run --project examples/03-first-call/csharp/usage -- --live` |
| [python/first_call.py](python/first_call.py) | `python examples/03-first-call/python/first_call.py --live` |
| [python/usage.py](python/usage.py) | `python examples/03-first-call/python/usage.py --live` |

`--live` permits a metered request. Configure AWS_REGION, AWS_PROFILE and an
approved NOVA_MODEL_ID first. Do not supply real patient data. Generated wording
can vary; check stop reason, output shape and source facts rather than exact text.

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.
