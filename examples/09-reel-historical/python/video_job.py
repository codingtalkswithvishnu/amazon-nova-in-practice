"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import os

    import boto3

    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    MODEL_ID = "amazon.nova-reel-v1:1"  # confirm the current version ID
    S3_OUTPUT = "s3://your-output-bucket/reel/"  # must exist and be writable by Bedrock

    # Step 1: submit the asynchronous job.
    start = client.start_async_invoke(
        modelId=MODEL_ID,
        modelInput={
            "taskType": "TEXT_VIDEO",
            "textToVideoParams": {
                "text": "A calm, slow pan across a bright, tidy clinic waiting room, "
                "warm natural light, reassuring and professional."
            },
            "videoGenerationConfig": {
                "durationSeconds": 6,
                "fps": 24,
                "dimension": "1280x720",
                "seed": 7,
            },
        },
        outputDataConfig={"s3OutputDataConfig": {"s3Uri": S3_OUTPUT}},
    )
    invocation_arn = start["invocationArn"]
    print("Job submitted:", invocation_arn)

    from nova_book.runtime import wait_for_video

    print("Video written to:", wait_for_video(client, invocation_arn))


if __name__ == "__main__":
    raise SystemExit("Historical endpoint: run local tests; this model is retired.")
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
