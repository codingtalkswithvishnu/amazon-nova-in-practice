# Chapter 5 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [csharp/prompt_extraction/Program.cs](csharp/prompt_extraction/Program.cs) | `dotnet run --project examples/05-structured-output/csharp/prompt_extraction -- --live` |
| [csharp/structured_extraction/Program.cs](csharp/structured_extraction/Program.cs) | `dotnet run --project examples/05-structured-output/csharp/structured_extraction -- --live` |
| [few_shot_prompt.txt](few_shot_prompt.txt) | Fictional fixture / reference input |
| [python/prompt_extraction.py](python/prompt_extraction.py) | `python examples/05-structured-output/python/prompt_extraction.py --live` |
| [python/structured_extraction.py](python/structured_extraction.py) | `python examples/05-structured-output/python/structured_extraction.py --live` |

`--live` permits a metered request. Configure AWS_REGION, AWS_PROFILE and an
approved NOVA_MODEL_ID first. Do not supply real patient data. Generated wording
can vary; check stop reason, output shape and source facts rather than exact text.

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.
