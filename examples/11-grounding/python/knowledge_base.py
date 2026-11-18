"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    import os

    import boto3

    # Knowledge Base operations use the bedrock-agent-runtime client.
    client = boto3.client(
        "bedrock-agent-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    KNOWLEDGE_BASE_ID = os.environ[
        "NOVA_KNOWLEDGE_BASE_ID"
    ]  # created once in the Bedrock console
    MODEL_ARN = os.environ["NOVA_GENERATION_MODEL_ARN"]

    response = client.retrieve_and_generate(
        input={"text": "What are the fictional clinic Saturday opening hours?"},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": MODEL_ARN,
            },
        },
    )

    # A grounded answer, plus citations back to your source documents.
    print(response["output"]["text"])
    for citation in response.get("citations", []):
        for ref in citation.get("retrievedReferences", []):
            print("Source:", ref.get("location"))


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
