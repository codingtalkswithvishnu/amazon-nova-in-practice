"""Complete chapter example. Run from the repository root with --live."""

import sys


def main():
    # pip install -U langchain-aws
    from langchain_aws import ChatBedrockConverse

    # LangChain's Bedrock chat model. Underneath, this calls the same
    # Converse API introduced in Chapters 3 and 4 — the model ID is an ordinary Nova ID.
    llm = ChatBedrockConverse(
        model="us.amazon.nova-pro-v1:0",  # a Nova model, selected by ID
        region_name="us-east-1",
    )

    # LangChain's own calling style, but the work is done by Nova via Bedrock.
    response = llm.invoke("In one sentence, what is Amazon Nova?")
    print(response.content)


if __name__ == "__main__":
    if "--live" not in sys.argv:
        raise SystemExit("Configure AWS and pass --live to make a paid request.")
    main()
