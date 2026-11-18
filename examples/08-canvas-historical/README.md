# Chapter 8 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

**Historical endpoint.** Canvas and both Reel versions retired on 30 September 2026.
These sources preserve the old contract for inspection and local tests. They are
not current live-call instructions. See the [AWS lifecycle table](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle-legacy.html).

| File | Command or purpose |
| --- | --- |
| [csharp/generate_image/Program.cs](csharp/generate_image/Program.cs) | Historical source; compile only |
| [python/generate_image.py](python/generate_image.py) | `python examples/08-canvas-historical/python/generate_image.py` |
| [python/remove_background.py](python/remove_background.py) | `python examples/08-canvas-historical/python/remove_background.py` |

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.
