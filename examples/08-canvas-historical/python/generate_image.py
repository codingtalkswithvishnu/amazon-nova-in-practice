"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import base64
    import json
    import os

    import boto3
    from botocore.config import Config

    # Image generation can take a little while, so allow a generous read timeout.
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        config=Config(read_timeout=300),
    )
    MODEL_ID = "amazon.nova-canvas-v1:0"

    body = json.dumps(
        {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": "A clean, friendly flat illustration of a stethoscope on a pale blue "
                "background, simple and professional, suitable for a clinic website."
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "width": 1024,
                "height": 1024,
                "quality": "standard",  # or "premium"
                "seed": 42,  # fixed seed -> repeatable image
            },
        }
    )

    response = client.invoke_model(modelId=MODEL_ID, body=body)
    result = json.loads(response["body"].read())

    # Images come back as Base64 strings; decode and save the first one.
    image_bytes = base64.b64decode(result["images"][0])
    with open("stethoscope.png", "wb") as f:
        f.write(image_bytes)
    print("Saved stethoscope.png")


if __name__ == "__main__":
    raise SystemExit("Historical endpoint: run local tests; this model is retired.")
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
