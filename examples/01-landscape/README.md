# Landscape checkpoint

Write four lines naming the user/task, Nova's job, Bedrock's role and the
application's validation responsibility. The optional framework example requires
langchain-aws (included in the supplied lock). It is a metered AWS call with --live.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [python/framework.py](python/framework.py) | `python examples/01-landscape/python/framework.py --live` |

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.
