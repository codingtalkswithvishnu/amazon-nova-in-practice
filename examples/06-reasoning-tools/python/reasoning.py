"""Nova 2 Lite request builder: high effort must omit inference controls."""

import os
import sys

import boto3
from botocore.config import Config

from nova_book.runtime import text_reply


def build_request(effort):
    if effort not in {"low", "medium", "high"}:
        raise ValueError("effort must be low, medium or high")
    request = {
        "modelId": os.environ.get(
            "NOVA_REASONING_MODEL_ID", "us.amazon.nova-2-lite-v1:0"
        ),
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "Can appointments of 20, 30 and 15 minutes all fit between 09:00 and 10:00? "
                        "Give a feasible subset and verify its total duration."
                    }
                ],
            }
        ],
        "additionalModelRequestFields": {
            "reasoningConfig": {"type": "enabled", "maxReasoningEffort": effort}
        },
    }
    if effort != "high":
        request["inferenceConfig"] = {"maxTokens": 1500, "temperature": 0}
    return request


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit(
            "Inspect build_request locally; use --live for a paid request."
        )
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        config=Config(read_timeout=3600),
    )
    print(text_reply(client.converse(**build_request("low"))))
