import copy
import importlib.util
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from jsonschema import ValidationError

from nova_book.assistant import policy_question
from nova_book.cost import estimate
from nova_book.evaluation import evaluate
from nova_book.runtime import (
    ResponseError,
    run_tools,
    stream_text,
    structured_result,
    text_reply,
    wait_for_video,
)
from nova_book.training import read_records

ROOT = Path(__file__).resolve().parents[1]


def answer(text="Done", stop="end_turn"):
    return {
        "stopReason": stop,
        "output": {"message": {"role": "assistant", "content": [{"text": text}]}},
    }


def tools(*calls):
    return {
        "stopReason": "tool_use",
        "output": {
            "message": {"role": "assistant", "content": [{"toolUse": c} for c in calls]}
        },
    }


def call(name="get_next_appointment", key="id1", arguments=None):
    return {
        "name": name,
        "toolUseId": key,
        "input": {"specialty": "cardiology"} if arguments is None else arguments,
    }


class FakeClient:
    def __init__(self, *responses):
        self.responses = iter(responses)
        self.requests = []

    def converse(self, **request):
        self.requests.append(copy.deepcopy(request))
        return next(self.responses)


class ToolTests(unittest.TestCase):
    def test_direct_answer_does_not_make_an_extra_call(self):
        client = FakeClient(answer())
        messages = [{"role": "user", "content": [{"text": "Hello"}]}]
        self.assertEqual(run_tools(client, "model", messages, {}), "Done")
        self.assertEqual(len(client.requests), 1)
        self.assertEqual(len(messages), 1)

    def test_multiple_calls_are_returned_in_one_matching_turn(self):
        client = FakeClient(tools(call(key="a"), call(key="b")), answer())
        run_tools(client, "model", [], {})
        history = client.requests[1]["messages"]
        self.assertEqual([m["role"] for m in history], ["assistant", "user"])
        self.assertEqual(
            [b["toolResult"]["toolUseId"] for b in history[-1]["content"]], ["a", "b"]
        )

    def test_unknown_tool_and_bad_arguments_never_execute(self):
        for request in [
            call(name="delete_records"),
            call(arguments={"specialty": 7}),
            call(arguments={"specialty": "cardiology", "extra": True}),
        ]:
            client = FakeClient(tools(request), answer())
            executed = []
            run_tools(client, "model", [], {}, lookup=lambda **kw: executed.append(kw))
            self.assertEqual(executed, [])
            self.assertEqual(
                client.requests[1]["messages"][-1]["content"][0]["toolResult"][
                    "status"
                ],
                "error",
            )

    def test_empty_search_is_success_but_failed_lookup_is_error(self):
        empty = FakeClient(tools(call(arguments={"specialty": "unknown"})), answer())
        run_tools(empty, "model", [], {})
        result = empty.requests[1]["messages"][-1]["content"][0]["toolResult"]
        self.assertEqual(result["status"], "success")
        self.assertIsNone(result["content"][0]["json"]["next_slot"])

        def failed(**kwargs):
            raise OSError("private detail must not reach the prompt")

        client = FakeClient(tools(call()), answer())
        run_tools(client, "model", [], {}, lookup=failed)
        result = client.requests[1]["messages"][-1]["content"][0]["toolResult"]
        self.assertEqual(result["status"], "error")
        self.assertNotIn("private detail", str(result))

    def test_loop_is_bounded_and_duplicate_ids_are_rejected(self):
        client = FakeClient(tools(call()), tools(call()))
        with self.assertRaises(ResponseError):
            run_tools(client, "model", [], {}, max_calls=2)
        self.assertEqual(len(client.requests), 2)
        with self.assertRaises(ResponseError):
            run_tools(FakeClient(tools(call(), call())), "model", [], {})


class ResponseTests(unittest.TestCase):
    def test_stream_ignores_non_text_and_rejects_missing_stop_and_errors(self):
        events = [
            {"contentBlockDelta": {"delta": {"toolUse": {"input": "{}"}}}},
            {"contentBlockDelta": {"delta": {"text": "Hello"}}},
            {"messageStop": {"stopReason": "end_turn"}},
        ]
        self.assertEqual("".join(stream_text(events)), "Hello")
        for bad in [
            events[:-1],
            [{"modelStreamErrorException": {}}],
            [{"messageStop": {"stopReason": "max_tokens"}}],
        ]:
            with self.assertRaises(ResponseError):
                list(stream_text(bad))

    def test_final_text_ignores_reasoning_and_combines_text(self):
        response = answer()
        response["output"]["message"]["content"] = [
            {"reasoningContent": {"reasoningText": {"text": "private"}}},
            {"text": "Hello "},
            {"text": "reader"},
        ]
        self.assertEqual(text_reply(response), "Hello reader")

    def test_truncation_blocked_empty_and_tool_answers_are_rejected(self):
        for response in [
            answer(stop="max_tokens"),
            answer(stop="guardrail_intervened"),
            answer(""),
            tools(call()),
            {"stopReason": "end_turn"},
        ]:
            with self.assertRaises(ResponseError):
                text_reply(response)

    def test_structured_contract_rejects_wrong_tool_type_and_missing_field(self):
        schema = {
            "type": "object",
            "properties": {"age": {"type": ["integer", "null"]}},
            "required": ["age"],
            "additionalProperties": False,
        }
        self.assertEqual(
            structured_result(
                tools(call(name="extract", arguments={"age": None})), "extract", schema
            ),
            {"age": None},
        )
        for data in [{}, {"age": "54"}, {"age": 54, "extra": 1}]:
            with self.assertRaises(ValidationError):
                structured_result(
                    tools(call(name="extract", arguments=data)), "extract", schema
                )
        with self.assertRaises(ResponseError):
            structured_result(tools(call()), "extract", schema)


class EvaluationAndCostTests(unittest.TestCase):
    def test_outcomes_include_errors_and_invalid_answers_in_denominator(self):
        def classify(text):
            if text == "error":
                raise RuntimeError("service failed")
            return {"ok": " Routine ", "wrong": "urgent", "bad": "perhaps"}[text]

        score = evaluate(
            classify, [(s, "routine") for s in ["ok", "wrong", "bad", "error"]]
        )
        self.assertEqual(
            [score[k] for k in ["correct", "wrong", "invalid", "error"]], [1] * 4
        )
        self.assertEqual(score["accuracy"], 0.25)

    def test_empty_and_malformed_eval_sets_fail_before_calling(self):
        for cases in [[], [("text", "rountine")], [("", "routine")], [("only one",)]]:
            with self.assertRaises(ValueError):
                evaluate(lambda _: self.fail("Must validate first"), cases)

    def test_decimal_cost_and_units(self):
        cost = estimate(1000, 200, 50_000, "0.035", "0.14")
        self.assertEqual(cost["daily"], Decimal("3.15"))
        self.assertEqual(cost["monthly"], Decimal("94.50"))
        self.assertEqual(estimate(1000, 0, 0, 1, 1)["daily"], 0)

    def test_invalid_cost_inputs(self):
        for values in [
            (-1, 1, 1, 1, 1),
            (1, 1, 1, "NaN", 1),
            (True, 1, 1, 1, 1),
            (1, 1, 1, -1, 1),
        ]:
            with self.assertRaises(ValueError):
                estimate(*values)


class JobTests(unittest.TestCase):
    def test_completion_failure_and_timeout_are_distinct(self):
        class Jobs:
            def __init__(self, responses):
                self.responses = iter(responses)

            def get_async_invoke(self, **kwargs):
                return next(self.responses)

        done = {
            "status": "Completed",
            "outputDataConfig": {
                "s3OutputDataConfig": {"s3Uri": "s3://fictional/output/"}
            },
        }
        self.assertEqual(
            wait_for_video(Jobs([done]), "arn", clock=lambda: 0),
            "s3://fictional/output/",
        )
        for state in ["Failed", "Unknown"]:
            with self.assertRaises(ResponseError):
                wait_for_video(Jobs([{"status": state}]), "arn", clock=lambda: 0)
        now = [0]

        def pause(seconds):
            now[0] += seconds

        with self.assertRaisesRegex(TimeoutError, "may still run"):
            wait_for_video(
                Jobs([{"status": "InProgress"}] * 3),
                "saved-arn",
                timeout=2,
                interval=1,
                clock=lambda: now[0],
                pause=pause,
            )


class DesignTests(unittest.TestCase):
    def run_question(self, **overrides):
        options = {
            "authorised": True,
            "check_content": lambda _: True,
            "classify": lambda _: "routine",
            "retrieve": lambda _: {
                "answer": "Saturday 09:00–13:00",
                "sources": ["fictional-policy-v1"],
            },
        }
        options.update(overrides)
        return policy_question("Saturday hours?", **options)

    def test_answer_remains_a_draft_and_requires_sources(self):
        self.assertEqual(self.run_question().state, "draft_ready")
        self.assertEqual(
            self.run_question(retrieve=lambda _: {}).reason, "missing_evidence"
        )

    def test_access_and_urgency_prevent_retrieval(self):
        def forbidden(_):
            self.fail("Should not retrieve")

        self.assertEqual(
            self.run_question(authorised=False, retrieve=forbidden).state, "rejected"
        )
        for label in ["urgent", "soon", "uncertain", None]:
            self.assertEqual(
                self.run_question(classify=lambda _: label, retrieve=forbidden).state,
                "needs_staff",
            )

    def test_blocked_input_and_dependency_failure_have_distinct_reasons(self):
        def failed(_):
            raise RuntimeError("dependency")

        self.assertEqual(
            self.run_question(check_content=lambda _: False).reason, "content_blocked"
        )
        self.assertEqual(self.run_question(retrieve=failed).reason, "retrieval_failed")
        self.assertEqual(
            self.run_question(classify=failed).reason, "classification_failed"
        )


class DataAndReasoningTests(unittest.TestCase):
    def test_training_fixture_and_invalid_records(self):
        self.assertEqual(
            len(
                read_records(ROOT / "examples/12-customisation/training_example.jsonl")
            ),
            3,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.jsonl"
            for content in [
                "",
                "\n",
                '{"prompt":"not a Nova conversation"}\n',
                "null\n",
            ]:
                path.write_text(content)
                with self.assertRaises(ValueError):
                    read_records(path)

    def test_high_effort_request_omits_incompatible_inference_controls(self):
        spec = importlib.util.spec_from_file_location(
            "reasoning", ROOT / "examples/06-reasoning-tools/python/reasoning.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertNotIn("inferenceConfig", module.build_request("high"))
        self.assertIn("inferenceConfig", module.build_request("low"))
        with self.assertRaises(ValueError):
            module.build_request("extreme")


if __name__ == "__main__":
    unittest.main()
