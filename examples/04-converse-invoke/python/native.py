"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import json
    import os

    import boto3

    from nova_book.runtime import text_reply

    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    MODEL_ID = os.environ.get("NOVA_MODEL_ID", "us.amazon.nova-lite-v1:0")

    # Nova's native request format, passed as a JSON body.
    body = {
        "schemaVersion": "messages-v1",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": "Name three benefits of a managed model service."}
                ],
            }
        ],
        "inferenceConfig": {"maxTokens": 300, "temperature": 0.3},
    }

    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
    )

    # The native response is a JSON body you parse yourself.
    result = json.loads(response["body"].read())
    print(text_reply(result))


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
