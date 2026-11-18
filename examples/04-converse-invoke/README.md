# Chapter 4 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [csharp/conversation/Program.cs](csharp/conversation/Program.cs) | `dotnet run --project examples/04-converse-invoke/csharp/conversation -- --live` |
| [csharp/native/Program.cs](csharp/native/Program.cs) | `dotnet run --project examples/04-converse-invoke/csharp/native -- --live` |
| [csharp/streaming/Program.cs](csharp/streaming/Program.cs) | `dotnet run --project examples/04-converse-invoke/csharp/streaming -- --live` |
| [python/conversation.py](python/conversation.py) | `python examples/04-converse-invoke/python/conversation.py --live` |
| [python/native.py](python/native.py) | `python examples/04-converse-invoke/python/native.py --live` |
| [python/streaming.py](python/streaming.py) | `python examples/04-converse-invoke/python/streaming.py --live` |

`--live` permits a metered request. Configure AWS_REGION, AWS_PROFILE and an
approved NOVA_MODEL_ID first. Do not supply real patient data. Generated wording
can vary; check stop reason, output shape and source facts rather than exact text.

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.
