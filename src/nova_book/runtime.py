"""Response handling, bounded tools and asynchronous job monitoring.

Clients are supplied by callers so tests never need AWS credentials.
"""

from copy import deepcopy
from time import monotonic, sleep

from jsonschema import Draft202012Validator


class ResponseError(ValueError):
    """The service response cannot be accepted as an application result."""


def stream_text(events):
    """Yield text deltas and reject errors or an incomplete final stream."""
    stopped = False
    saw_text = False
    for event in events:
        if any(key.endswith("Exception") for key in event):
            raise ResponseError("Stream failed; the displayed answer is incomplete")
        delta = event.get("contentBlockDelta", {}).get("delta", {})
        if isinstance(delta.get("text"), str):
            saw_text = saw_text or bool(delta["text"].strip())
            yield delta["text"]
        if "messageStop" in event:
            stopped = event["messageStop"].get("stopReason") in {
                "end_turn",
                "stop_sequence",
            }
            if not stopped:
                raise ResponseError("Stream did not produce a complete final answer")
    if not stopped or not saw_text:
        raise ResponseError("Stream ended without a complete text answer")


def text_reply(response):
    """Return only final text blocks; reject truncation, tools and blocked output."""
    if response.get("stopReason") not in {"end_turn", "stop_sequence"}:
        raise ResponseError(f"No complete answer: {response.get('stopReason')}")
    try:
        blocks = response["output"]["message"]["content"]
        if not isinstance(blocks, list) or any("toolUse" in b for b in blocks):
            raise ResponseError("Expected final text, received a tool request")
        text = "".join(b["text"] for b in blocks if isinstance(b.get("text"), str))
    except (KeyError, TypeError, AttributeError) as exc:
        raise ResponseError("Malformed response content") from exc
    if not text.strip():
        raise ResponseError("No final text in response")
    return text


def structured_result(response, tool_name, schema):
    """Validate the selected tool and all fields before returning extracted data."""
    if response.get("stopReason") != "tool_use":
        raise ResponseError("Expected a complete tool-use response")
    try:
        calls = [
            b["toolUse"]
            for b in response["output"]["message"]["content"]
            if "toolUse" in b
        ]
        if len(calls) != 1 or calls[0]["name"] != tool_name:
            raise ResponseError("Expected exactly one call to the extraction tool")
        result = calls[0]["input"]
    except (KeyError, TypeError) as exc:
        raise ResponseError("Malformed extraction response") from exc
    Draft202012Validator(schema).validate(result)
    return result


APPOINTMENT_SCHEMA = {
    "type": "object",
    "properties": {"specialty": {"type": "string", "minLength": 1}},
    "required": ["specialty"],
    "additionalProperties": False,
}


def get_next_appointment(specialty):
    """Read-only fictional schedule; null means no slot, not a service failure."""
    schedule = {
        "cardiology": "2030-11-03T10:30:00+05:30",
        "general": "2030-10-30T09:00:00+05:30",
    }
    return {"specialty": specialty, "next_slot": schedule.get(specialty)}


def run_tools(
    client, model_id, messages, tool_config, *, max_calls=4, lookup=get_next_appointment
):
    """Bound the loop, group parallel results, validate inputs and allowlist tools."""
    if type(max_calls) is not int or max_calls < 1:
        raise ValueError("max_calls must be a positive integer")
    history = deepcopy(messages)
    for _ in range(max_calls):
        response = client.converse(
            modelId=model_id,
            messages=history,
            toolConfig=tool_config,
            inferenceConfig={"maxTokens": 500, "temperature": 0},
        )
        if response.get("stopReason") != "tool_use":
            return text_reply(response)
        message = response["output"]["message"]
        calls = [b["toolUse"] for b in message["content"] if "toolUse" in b]
        ids = [c.get("toolUseId") for c in calls]
        if not calls or not all(isinstance(i, str) and i for i in ids):
            raise ResponseError("Tool-use response lacks tool IDs")
        if len(set(ids)) != len(ids):
            raise ResponseError("Duplicate tool IDs")
        history.append(message)
        results = []
        for call in calls:
            status = "success"
            try:
                if call.get("name") != "get_next_appointment":
                    raise ValueError("Tool is not allowed")
                Draft202012Validator(APPOINTMENT_SCHEMA).validate(call.get("input"))
                result = lookup(**call["input"])
            except Exception:
                # Do not include service credentials or raw exception text in prompts.
                result = {"error": "Lookup could not be completed. Ask staff for help."}
                status = "error"
            results.append(
                {
                    "toolResult": {
                        "toolUseId": call["toolUseId"],
                        "status": status,
                        "content": [{"json": result}],
                    }
                }
            )
        history.append({"role": "user", "content": results})
    raise ResponseError("Tool loop exhausted its request budget; ask staff for help")


def wait_for_video(
    client, invocation_arn, *, timeout=1200, interval=15, clock=monotonic, pause=sleep
):
    """Monitor a previously submitted job; timeout never implies cancellation."""
    if timeout <= 0 or interval <= 0:
        raise ValueError("timeout and interval must be positive")
    deadline = clock() + timeout
    while True:
        remaining = deadline - clock()
        if remaining <= 0:
            raise TimeoutError(
                f"Monitoring timed out; job may still run: {invocation_arn}"
            )
        response = client.get_async_invoke(invocationArn=invocation_arn)
        state = response["status"]
        if state == "Completed":
            return response["outputDataConfig"]["s3OutputDataConfig"]["s3Uri"]
        if state == "Failed":
            raise ResponseError("Video generation failed; inspect the saved job ARN")
        if state != "InProgress":
            raise ResponseError(f"Unknown job state: {state}")
        pause(min(interval, max(0, deadline - clock())))
