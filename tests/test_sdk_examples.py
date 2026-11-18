"""Execute complete Python entry functions with fake SDK clients and real schemas."""

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import botocore.session
from botocore.validate import validate_parameters

ROOT = Path(__file__).resolve().parents[1]


class RequestCheckingClient:
    def __init__(self, service):
        self.model = botocore.session.get_session().get_service_model(service)

    def __getattr__(self, name):
        operation = "".join(part.title() for part in name.split("_"))

        def invoke(**request):
            validate_parameters(
                request, self.model.operation_model(operation).input_shape
            )
            response = {
                "stopReason": "end_turn",
                "usage": {"inputTokens": 10, "outputTokens": 5},
                "output": {
                    "message": {
                        "role": "assistant",
                        "content": [{"text": "Fictional answer"}],
                    }
                },
            }
            if name == "converse" and "toolConfig" in request:
                tool = request["toolConfig"]["tools"][0]["toolSpec"]["name"]
                if tool == "record_extracted_fields":
                    response["stopReason"] = "tool_use"
                    response["output"]["message"]["content"] = [
                        {
                            "toolUse": {
                                "name": tool,
                                "toolUseId": "fictional-id",
                                "input": {
                                    "age": 54,
                                    "chief_complaint": "dry cough",
                                    "duration_days": 5,
                                    "fever": True,
                                    "medications": ["amlodipine"],
                                    "allergies": [],
                                },
                            }
                        }
                    ]
            if name == "invoke_model":
                body = json.loads(request["body"])
                if "taskType" in body:
                    # Local illustrative response, never a generated image claim.
                    return {
                        "body": io.BytesIO(
                            json.dumps({"images": ["aW1hZ2U="]}).encode()
                        )
                    }
                if body.get("schemaVersion") != "messages-v1":
                    raise AssertionError("Missing native Nova schema version")
                return {"body": io.BytesIO(json.dumps(response).encode())}
            if name == "converse_stream":
                return {
                    "stream": iter(
                        [
                            {
                                "contentBlockDelta": {
                                    "delta": {"text": "Fictional text"}
                                }
                            },
                            {"messageStop": {"stopReason": "end_turn"}},
                        ]
                    )
                }
            if name == "retrieve_and_generate":
                return {"output": {"text": "Fictional answer"}, "citations": []}
            if name == "start_async_invoke":
                return {
                    "invocationArn": "arn:aws:bedrock:us-east-1:123456789012:async-invoke/demo"
                }
            if name == "get_async_invoke":
                return {
                    "status": "Completed",
                    "outputDataConfig": {
                        "s3OutputDataConfig": {"s3Uri": "s3://fictional/output/"}
                    },
                }
            if name == "apply_guardrail":
                return {"action": "NONE"}
            return response

        return invoke


class CompleteExampleTests(unittest.TestCase):
    def test_guardrail_request_contract_and_blocked_outcome(self):
        path = ROOT / "examples/14-evaluation-safety/python/guardrails.py"
        spec = importlib.util.spec_from_file_location("guardrail_example", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(
            module.check_text(
                RequestCheckingClient("bedrock-runtime"),
                "Fictional question",
                "demo123456",
                "1",
            )
        )

        class BlockedClient:
            def apply_guardrail(self, **request):
                return {"action": "GUARDRAIL_INTERVENED"}

        self.assertFalse(
            module.check_text(BlockedClient(), "Fictional question", "demo123456", "1")
        )

    def test_complete_python_aws_examples_with_local_clients(self):
        paths = [
            p
            for p in ROOT.glob("examples/**/python/*.py")
            if p.stem
            not in {
                "framework",
                "evaluate",
                "estimate",
                "reasoning",
                "guardrails",
                "validate_data",
                "demo",
            }
        ]
        with tempfile.TemporaryDirectory() as directory:
            prior = Path.cwd()
            os.chdir(directory)
            try:
                Path("product_photo.png").write_bytes(b"fictional input bytes")
                with (
                    patch.dict(
                        os.environ,
                        {
                            "NOVA_KNOWLEDGE_BASE_ID": "DEMO123456",
                            "NOVA_GENERATION_MODEL_ARN": "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0",
                        },
                    ),
                    patch(
                        "boto3.client",
                        side_effect=lambda service, **kw: RequestCheckingClient(
                            service
                        ),
                    ),
                ):
                    for number, path in enumerate(paths):
                        with self.subTest(example=str(path.relative_to(ROOT))):
                            spec = importlib.util.spec_from_file_location(
                                f"example{number}", path
                            )
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            with contextlib.redirect_stdout(io.StringIO()):
                                module.main()
            finally:
                os.chdir(prior)


if __name__ == "__main__":
    unittest.main()
