# Chapter 9 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

**Historical endpoint.** Canvas and both Reel versions retired on 30 September 2026.
These sources preserve the old contract for inspection and local tests. They are
not current live-call instructions. See the [AWS lifecycle table](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle-legacy.html).

| File | Command or purpose |
| --- | --- |
| [csharp/video_job/Program.cs](csharp/video_job/Program.cs) | Historical source; compile only |
| [python/video_job.py](python/video_job.py) | `python examples/09-reel-historical/python/video_job.py` |

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.
