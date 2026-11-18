"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import os

    import boto3

    from nova_book.runtime import text_reply

    # The Bedrock *runtime* client is the one that actually calls models.
    # Set region_name to the region where you enabled Nova access.
    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    # The model ID selects which Nova model answers. Confirm the exact ID
    # for your account/region in the Bedrock console if this is rejected.
    MODEL_ID = os.environ.get("NOVA_MODEL_ID", "us.amazon.nova-lite-v1:0")

    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": "In two sentences, explain what Amazon Bedrock is to a new engineer."
                    }
                ],
            }
        ],
        inferenceConfig={"maxTokens": 300, "temperature": 0.3},
    )

    # The model's text sits inside the returned structure. We dig it out here;
    # Chapter 4 explains this response shape in full.
    reply = text_reply(response)
    print(reply)


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
