# Chapter 7 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [csharp/document/Program.cs](csharp/document/Program.cs) | `dotnet run --project examples/07-multimodal/csharp/document -- --live` |
| [csharp/image/Program.cs](csharp/image/Program.cs) | `dotnet run --project examples/07-multimodal/csharp/image -- --live` |
| [python/document.py](python/document.py) | `python examples/07-multimodal/python/document.py --live` |
| [python/image.py](python/image.py) | `python examples/07-multimodal/python/image.py --live` |

`--live` permits a metered request. Configure AWS_REGION, AWS_PROFILE and an
approved NOVA_MODEL_ID first. Do not supply real patient data. Generated wording
can vary; check stop reason, output shape and source facts rather than exact text.

Open fixtures/synthetic_referral.pdf and fixtures/synthetic_form_photo.jpg before
the model call. The form has a deliberately blank appointment reference. Check
each generated value against the source. No cloud resources are created here.

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.
