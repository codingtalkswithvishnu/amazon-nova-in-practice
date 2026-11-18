"""Check synthetic text with an existing published Bedrock guardrail."""

import os
import sys

import boto3


def check_text(client, text, guardrail_id, guardrail_version):
    response = client.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion=guardrail_version,
        source="INPUT",
        content=[{"text": {"text": text}}],
    )
    # An exception is a failed check, never implicit permission to continue.
    return response["action"] == "NONE"


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit(
            "Set a published guardrail ID/version and use --live for a metered check."
        )
    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    print(
        check_text(
            client,
            "What are the fictional clinic opening hours?",
            os.environ["NOVA_GUARDRAIL_ID"],
            os.environ["NOVA_GUARDRAIL_VERSION"],
        )
    )
