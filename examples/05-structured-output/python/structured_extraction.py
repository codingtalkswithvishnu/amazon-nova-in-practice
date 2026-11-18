"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import os

    import boto3

    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    MODEL_ID = os.environ.get("NOVA_MODEL_ID", "us.amazon.nova-lite-v1:0")

    clinical_note = (
        "Patient is a 54-year-old with a dry cough for 5 days and mild fever. "
        "On amlodipine for hypertension. No known allergies."
    )

    # The tool's input schema IS the output shape we want back.
    tool_config = {
        "tools": [
            {
                "toolSpec": {
                    "name": "record_extracted_fields",
                    "description": "Record the structured fields extracted from a clinical note.",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "age": {"type": ["integer", "null"]},
                                "chief_complaint": {"type": ["string", "null"]},
                                "duration_days": {"type": ["integer", "null"]},
                                "fever": {"type": ["boolean", "null"]},
                                "medications": {
                                    "type": ["array", "null"],
                                    "items": {"type": "string"},
                                },
                                "allergies": {
                                    "type": ["array", "null"],
                                    "items": {"type": "string"},
                                },
                            },
                            "required": [
                                "age",
                                "chief_complaint",
                                "duration_days",
                                "fever",
                                "medications",
                                "allergies",
                            ],
                            "additionalProperties": False,
                        }
                    },
                }
            }
        ],
        # Force the model to use our tool, so we always get structured output.
        "toolChoice": {"tool": {"name": "record_extracted_fields"}},
    }

    response = client.converse(
        modelId=MODEL_ID,
        system=[
            {
                "text": "Extract only what is explicitly stated. Use null for anything absent. Never guess."
            }
        ],
        messages=[
            {"role": "user", "content": [{"text": f"Clinical note:\n{clinical_note}"}]}
        ],
        toolConfig=tool_config,
        inferenceConfig={"maxTokens": 500, "temperature": 0},
    )

    from nova_book.runtime import structured_result

    schema = tool_config["tools"][0]["toolSpec"]["inputSchema"]["json"]
    fields = structured_result(response, "record_extracted_fields", schema)
    print(fields)


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
