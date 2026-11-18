"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import os

    import boto3

    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    MODEL_ID = os.environ.get(
        "NOVA_MODEL_ID", "us.amazon.nova-pro-v1:0"
    )  # a capable model for multi-step tool use

    # Step 0: the real function behind the tool (synthetic data here).
    def get_next_appointment(specialty: str) -> dict:
        fake_schedule = {
            "cardiology": "2030-11-03T10:30:00+05:30",
            "general": "2030-10-30T09:00:00+05:30",
        }
        return {
            "specialty": specialty,
            "next_slot": fake_schedule.get(specialty, "no slots found"),
        }

    # Step 1: describe the tool to the model.
    tool_config = {
        "tools": [
            {
                "toolSpec": {
                    "name": "get_next_appointment",
                    "description": "Get the next available appointment slot for a medical specialty.",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "specialty": {
                                    "type": "string",
                                    "description": "e.g. cardiology, general",
                                }
                            },
                            "required": ["specialty"],
                        }
                    },
                }
            }
        ]
    }

    messages = [
        {
            "role": "user",
            "content": [{"text": "When is the next cardiology appointment available?"}],
        }
    ]

    from nova_book.runtime import run_tools

    print(run_tools(client, MODEL_ID, messages, tool_config))


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
