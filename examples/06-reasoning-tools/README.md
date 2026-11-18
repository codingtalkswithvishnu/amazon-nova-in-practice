# Chapter 6 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [csharp/appointments/Program.cs](csharp/appointments/Program.cs) | `dotnet run --project examples/06-reasoning-tools/csharp/appointments -- --live` |
| [python/appointments.py](python/appointments.py) | `python examples/06-reasoning-tools/python/appointments.py --live` |
| [python/reasoning.py](python/reasoning.py) | `python examples/06-reasoning-tools/python/reasoning.py --live` |

`--live` permits a metered request. Configure AWS_REGION, AWS_PROFILE and an
approved NOVA_MODEL_ID first. Do not supply real patient data. Generated wording
can vary; check stop reason, output shape and source facts rather than exact text.

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.
