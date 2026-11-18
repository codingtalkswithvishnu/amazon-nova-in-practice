"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import os

    import boto3

    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    response = client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[{"role": "user", "content": [{"text": "Explain Bedrock briefly."}]}],
        inferenceConfig={"maxTokens": 100},
    )
    usage = response["usage"]
    print(
        f"Input tokens: {usage['inputTokens']}, Output tokens: {usage['outputTokens']}"
    )


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
