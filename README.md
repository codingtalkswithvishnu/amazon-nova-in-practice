# Amazon Nova in Practice — companion examples

Companion code for **Amazon Nova: Frontier Intelligence — Powering Your
Organisation's Workflows**, by **Vishnu VG**.

Start with [Amazon Nova on AWS](https://aws.amazon.com/nova/) for the product and
current documentation. This repository contains complete teaching examples,
fictional data and local contract checks. The book, cover and EPUB are maintained
separately.

## Start here

Use Git, Python 3.12 or later and, for C# examples, the .NET 11 SDK. The checked
baseline is Python 3.12.16, .NET SDK 11.0.100 and AWS .NET SDK packages 4.1.0.2.
The lock includes the optional LangChain example and validation tools.
.NET 11 is the latest stable release for this edition (10 November 2026), with
STS support through 14 November 2028. See the [Microsoft support record](https://github.com/dotnet/core/blob/main/release-notes/11.0/README.md).
`global.json` selects the validated SDK feature band and rejects prereleases.

From the directory where you keep projects (macOS/Linux):

```bash
git clone https://github.com/codingtalkswithvishnu/amazon-nova-in-practice.git
cd amazon-nova-in-practice
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip install --no-deps -e .
python -m unittest discover -s tests -v
python tools/verify.py
```

Windows PowerShell, from the cloned repository root:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock
python -m pip install --no-deps -e .
python -m unittest discover -s tests -v
python tools/verify.py
```

Expected result: local tests and syntax/fixture checks pass. These commands do
not contact AWS. C# local checks:

```bash
dotnet run --project dotnet/ContractChecks
python tools/check_dotnet.py
```

The first command verifies response, schema and tool-result handling. The second
restores and builds every supplied C# project using committed package locks.

## Your first metered request

Install the AWS CLI and sign in using your organisation's short-lived credential
method. For IAM Identity Center, use `aws sso login --profile your-learning-profile`.
Set AWS_PROFILE to that profile, AWS_REGION to a supported Region and NOVA_MODEL_ID
to an approved model/profile ID. The default teaching route is
`us.amazon.nova-lite-v1:0` in `us-east-1`; cross-region routing may process a request
in another permitted destination Region. Verify your identity with
`aws sts get-caller-identity` and confirm the route's permissions and availability.

```bash
python examples/03-first-call/python/first_call.py --live
dotnet run --project examples/03-first-call/csharp/first_call -- --live
```

Expect generated text. Inspect the usage example for token counters. Wording
varies. AccessDenied means inspect the identity/policies/resource; it does not
mean an obsolete model-enable toggle needs switching. Missing credentials,
unsupported model/Region, throttling and incomplete output are separate failures.
Budget alerts are notifications, so also bound the number of requests you run.
Keep credentials out of the repository.

## Chapter map

| Chapter | Start here | Outcome |
| --- | --- | --- |
| 1 | [01-landscape](examples/01-landscape/README.md) | Name component responsibilities |
| 2 | [02-model-selection](examples/02-model-selection/README.md) | Choose a measured model candidate |
| 3 | [03-first-call](examples/03-first-call/README.md) | First response and usage |
| 4 | [04-converse-invoke](examples/04-converse-invoke/README.md) | History, streaming and native JSON |
| 5 | [05-structured-output](examples/05-structured-output/README.md) | Validated extracted fields |
| 6 | [06-reasoning-tools](examples/06-reasoning-tools/README.md) | Reasoning settings and bounded tools |
| 7 | [07-multimodal](examples/07-multimodal/README.md) | Synthetic PDF and image input |
| 8 | [08-canvas-historical](examples/08-canvas-historical/README.md) | Historical image contract |
| 9 | [09-reel-historical](examples/09-reel-historical/README.md) | Historical asynchronous video contract |
| 10 | [10-voice](examples/10-voice/README.md) | Official voice sample learning route |
| 11 | [11-grounding](examples/11-grounding/README.md) | Policy retrieval and citation inspection |
| 12 | [12-customisation](examples/12-customisation/README.md) | Conversation-format training preparation |
| 13 | [13-cost](examples/13-cost/README.md) | Decimal model-only cost estimate |
| 14 | [14-evaluation-safety](examples/14-evaluation-safety/README.md) | Evaluation and guardrail contracts |
| 15 | [15-assistant-design](examples/15-assistant-design/README.md) | Offline assistant state transitions |
| 16 | [16-industry-patterns](examples/16-industry-patterns/README.md) | Measurable industry pilot brief |

## Example boundaries and model status

Reviewed 18 November 2026. AWS lists Canvas, Reel 1.0/1.1 and first-generation
Sonic as retired. Their preserved request contracts must not be treated as live
endpoint instructions. The voice route uses maintained Nova 2 Sonic references
and identifies Nova 2.5 Sonic as a newer catalogue option. Check the exact model's
current lifecycle before making a paid request.

The training records, urgency labels and appointment schedules are fictional.
They are not medical guidance or evidence of a validated clinical system. Voice,
training and deployment are documented extensions; this repository does not
supply a deployed portal, validated triage service or verified telephony client.
Keep your practice modifications in a separate directory from the reference.

See [VALIDATION.md](VALIDATION.md) for executed checks and limits. Run
`python -m pip_audit -r requirements.lock` for a fresh dependency check. The
[CI workflow](.github/workflows/checks.yml) repeats local tests and compilation;
it has no AWS credentials and does not perform paid inference.
