"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import os
    from pathlib import Path

    import boto3

    from nova_book.runtime import text_reply

    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    MODEL_ID = os.environ.get(
        "NOVA_MODEL_ID", "us.amazon.nova-lite-v1:0"
    )  # multimodal; Micro would not work here

    # A synthetic referral PDF you have on disk. Never use real patient documents.
    with open(
        Path(__file__).resolve().parents[3] / "fixtures" / "synthetic_referral.pdf",
        "rb",
    ) as f:
        document_bytes = f.read()

    response = client.converse(
        modelId=MODEL_ID,
        system=[
            {
                "text": "You summarise clinical referrals for a busy GP. "
                "Be factual, concise, and never add clinical judgement."
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": "Summarise this referral in three short bullet points: reason, relevant history, requested action."
                    },
                    {
                        "document": {
                            "format": "pdf",  # confirm supported formats for the chosen model
                            "name": "Synthetic Referral",
                            "source": {"bytes": document_bytes},
                        }
                    },
                ],
            }
        ],
        inferenceConfig={"maxTokens": 500, "temperature": 0.2},
    )

    print(text_reply(response))


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
