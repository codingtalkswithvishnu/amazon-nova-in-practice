# Voice learning route

Use the maintained [AWS Nova 2 Sonic sample index](https://docs.aws.amazon.com/nova/latest/nova2-userguide/sonic-code-examples.html)
and [getting-started guide](https://docs.aws.amazon.com/nova/latest/nova2-userguide/sonic-getting-started.html).
The basic sample does not implement true bidirectional audio or barge-in. Select
the full-featured sample for interruption tests. Follow its dependency/audio setup;
ordinary boto3 Converse is not a substitute for the bidirectional streaming SDK.

The current [Nova 2.5 Sonic model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-2-5-sonic.html)
adds a newer option. Compare its event contract and region availability before a
new implementation. First-generation Sonic is retired. This repository supplies a
guided route, not a locally verified microphone or telephony client.

Check one synthetic exchange, input/output sample rates, turn-end events, playback
queue clearing on interruption, tool authorization, and orderly session shutdown.
Never infer that an attached text policy filters an entire audio stream.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.
