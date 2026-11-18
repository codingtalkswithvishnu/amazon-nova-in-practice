using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using Amazon.BedrockRuntime;
using Amazon.BedrockRuntime.Model;
using Amazon.Runtime.Documents;

namespace NovaBook;

public static class Support
{
    public static Document ToDocument(object value) =>
        Document.FromObject(JsonSerializer.SerializeToElement(value));

    public static string ReadFinalText(ConverseResponse response)
    {
        if (response.StopReason != StopReason.End_turn && response.StopReason != StopReason.Stop_sequence)
            throw new InvalidOperationException("No complete final answer: " + response.StopReason);
        var blocks = response.Output?.Message?.Content;
        if (blocks == null || blocks.Any(b => b.ToolUse != null))
            throw new InvalidOperationException("Expected final text");
        var text = string.Concat(blocks.Where(b => b.Text != null).Select(b => b.Text));
        if (string.IsNullOrWhiteSpace(text)) throw new InvalidOperationException("No final text");
        return text;
    }

    public static string ReadNativeText(JsonElement response)
    {
        var stop = response.GetProperty("stopReason").GetString();
        if (stop != "end_turn" && stop != "stop_sequence")
            throw new InvalidOperationException("No complete native answer: " + stop);
        var blocks = response.GetProperty("output").GetProperty("message").GetProperty("content");
        var text = string.Concat(blocks.EnumerateArray()
            .Where(b => b.TryGetProperty("text", out _))
            .Select(b => b.GetProperty("text").GetString()));
        if (string.IsNullOrWhiteSpace(text)) throw new InvalidOperationException("No final text");
        return text;
    }

    public static string ValidateExtractedFields(Document document)
    {
        using var payload = JsonDocument.Parse(JsonSerializer.Serialize(document));
        var fields = payload.RootElement;
        var expected = new[] { "age", "chief_complaint", "duration_days", "fever", "medications", "allergies" };
        if (fields.ValueKind != JsonValueKind.Object || fields.EnumerateObject().Count() != expected.Length ||
            expected.Any(name => !fields.TryGetProperty(name, out _)))
            throw new InvalidOperationException("Missing or unexpected extraction fields");
        foreach (var name in expected)
        {
            var value = fields.GetProperty(name);
            if (value.ValueKind == JsonValueKind.Null) continue;
            var valid = name switch
            {
                "age" or "duration_days" => value.ValueKind == JsonValueKind.Number && value.TryGetInt32(out _),
                "chief_complaint" => value.ValueKind == JsonValueKind.String,
                "fever" => value.ValueKind is JsonValueKind.True or JsonValueKind.False,
                _ => value.ValueKind == JsonValueKind.Array &&
                     value.EnumerateArray().All(item => item.ValueKind == JsonValueKind.String)
            };
            if (!valid) throw new InvalidOperationException("Invalid extraction field: " + name);
        }
        return fields.GetRawText();
    }

    public static List<ContentBlock> RunAllowedLookups(Message message)
    {
        var results = new List<ContentBlock>();
        var ids = new HashSet<string>();
        foreach (var block in message.Content.Where(b => b.ToolUse != null))
        {
            var tool = block.ToolUse;
            if (string.IsNullOrWhiteSpace(tool.ToolUseId) || !ids.Add(tool.ToolUseId))
                throw new InvalidOperationException("Missing or duplicate tool ID");
            object result;
            var status = ToolResultStatus.Success;
            try
            {
                var input = tool.Input.AsDictionary();
                if (tool.Name != "get_next_appointment" || input.Count != 1 ||
                    !input.ContainsKey("specialty") || !input["specialty"].IsString())
                    throw new ArgumentException("Invalid tool or arguments");
                var specialty = input["specialty"].AsString();
                if (string.IsNullOrWhiteSpace(specialty)) throw new ArgumentException("Empty specialty");
                var schedule = new Dictionary<string, string>
                {
                    ["cardiology"] = "2030-11-03T10:30:00+05:30",
                    ["general"] = "2030-10-30T09:00:00+05:30"
                };
                result = new { specialty, next_slot = schedule.GetValueOrDefault(specialty) };
            }
            catch (Exception)
            {
                status = ToolResultStatus.Error;
                result = new { error = "Lookup could not be completed; ask staff for help." };
            }
            results.Add(new ContentBlock { ToolResult = new ToolResultBlock
            {
                ToolUseId = tool.ToolUseId, Status = status,
                Content = new List<ToolResultContentBlock>
                    { new ToolResultContentBlock { Json = ToDocument(result) } }
            }});
        }
        if (results.Count == 0) throw new InvalidOperationException("Tool response has no calls");
        return results;
    }
}
