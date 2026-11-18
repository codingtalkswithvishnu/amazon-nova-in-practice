"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import base64
    import json

    import boto3
    from botocore.config import Config

    client = boto3.client(
        "bedrock-runtime", region_name="us-east-1", config=Config(read_timeout=300)
    )

    with open("product_photo.png", "rb") as f:
        source_image = base64.b64encode(f.read()).decode("utf-8")

    # Same model, same InvokeModel call — only the taskType and its params change.
    body = json.dumps(
        {
            "taskType": "BACKGROUND_REMOVAL",
            "backgroundRemovalParams": {"image": source_image},
        }
    )

    response = client.invoke_model(modelId="amazon.nova-canvas-v1:0", body=body)
    result = json.loads(response["body"].read())
    with open("product_no_bg.png", "wb") as f:
        f.write(base64.b64decode(result["images"][0]))
    print("Saved product_no_bg.png")


if __name__ == "__main__":
    raise SystemExit("Historical endpoint: run local tests; this model is retired.")
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
