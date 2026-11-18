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

    # Synthetic note — never use real patient data while developing.
    clinical_note = (
        "Patient is a 54-year-old presenting with a dry cough for 5 days and mild fever. "
        "No shortness of breath. History of hypertension, on amlodipine. No known allergies."
    )

    response = client.converse(
        modelId=MODEL_ID,
        system=[
            {
                "text":
                # Role + constraints live here, as durable rules.
                "You are a careful clinical-documentation assistant. "
                "Extract only what is explicitly stated. If a field is not mentioned, use null. "
                "Never infer, guess, or add a diagnosis. Return valid JSON only, with no extra text."
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text":
                        # Task + data + format live here.
                        "Extract these fields from the clinical note as JSON with keys "
                        "age, chief_complaint, duration_days, fever (true/false/null), "
                        "medications (list), allergies (list).\n\n"
                        f"Clinical note:\n{clinical_note}"
                    }
                ],
            }
        ],
        inferenceConfig={"maxTokens": 400, "temperature": 0},
    )

    print(text_reply(response))


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
