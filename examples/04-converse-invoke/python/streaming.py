"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import os

    import boto3

    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    MODEL_ID = os.environ.get("NOVA_MODEL_ID", "us.amazon.nova-lite-v1:0")
    response = client.converse_stream(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": "Write a short, reassuring welcome message for a patient using our clinic's appointment portal for the first time."
                    }
                ],
            }
        ],
        inferenceConfig={"maxTokens": 300, "temperature": 0.5},
    )

    from nova_book.runtime import stream_text

    for text in stream_text(response["stream"]):
        print(text, end="", flush=True)
    print()


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
