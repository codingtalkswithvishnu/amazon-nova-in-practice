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
    with open(
        Path(__file__).resolve().parents[3] / "fixtures" / "synthetic_form_photo.jpg",
        "rb",
    ) as f:
        image_bytes = f.read()

    response = client.converse(
        modelId=os.environ.get("NOVA_MODEL_ID", "us.amazon.nova-lite-v1:0"),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": "This is a photo of a patient intake form. List which fields are filled in and which are left blank."
                    },
                    {"image": {"format": "jpeg", "source": {"bytes": image_bytes}}},
                ],
            }
        ],
        inferenceConfig={"maxTokens": 500, "temperature": 0},
    )
    print(text_reply(response))


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
