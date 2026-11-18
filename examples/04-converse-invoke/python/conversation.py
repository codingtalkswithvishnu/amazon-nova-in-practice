"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import os

    import boto3

    from nova_book.runtime import text_reply

    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    MODEL_ID = os.environ.get("NOVA_MODEL_ID", "us.amazon.nova-lite-v1:0")

    response = client.converse(
        modelId=MODEL_ID,
        # Standing instructions, kept separate from the conversation itself.
        system=[
            {
                "text": "You are a careful assistant for a clinic's patient-support desk. "
                "Answer in plain language, keep to general guidance, and never invent "
                "clinical details or give a diagnosis. If something sounds urgent, advise "
                "the patient to contact a clinician or emergency services."
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": "I was asked to fast before my blood test. What does that involve?"
                    }
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "text": "Fasting usually means no food or drink except water for a set number of hours beforehand."
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "text": "For how many hours, and can I take my regular medication?"
                    }
                ],
            },
        ],
        inferenceConfig={"maxTokens": 400, "temperature": 0.3, "topP": 0.9},
    )

    print(text_reply(response))


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
