using System.Text.Json;
using Amazon.BedrockRuntime;
using Amazon.BedrockRuntime.Model;
using static NovaBook.Support;

var checks = 0;
void Check(bool condition) { if (!condition) throw new Exception("Contract check failed"); checks++; }
void Reject(Action operation)
{
    try { operation(); }
    catch (InvalidOperationException) { checks++; return; }
    throw new Exception("Expected rejection");
}
var fields = new { age = 54, chief_complaint = "cough", duration_days = 5,
                   fever = true, medications = new[] { "amlodipine" }, allergies = Array.Empty<string>() };
var json = ValidateExtractedFields(ToDocument(fields));
Check(JsonDocument.Parse(json).RootElement.GetProperty("age").GetInt32() == 54);
Reject(() => ValidateExtractedFields(ToDocument(new { age = "54" })));
Reject(() => ValidateExtractedFields(ToDocument(new { age = "54", chief_complaint = "cough",
     duration_days = 5, fever = true, medications = new[] { "amlodipine" }, allergies = Array.Empty<string>() })));
ConverseResponse Answer(StopReason stop) => new() { StopReason = stop,
    Output = new ConverseOutput { Message = new Message { Role = ConversationRole.Assistant,
        Content = new List<ContentBlock> { new() { Text = "Hello " }, new() { Text = "reader" } } } } };
Check(ReadFinalText(Answer(StopReason.End_turn)) == "Hello reader");
Reject(() => ReadFinalText(Answer(StopReason.Max_tokens)));
Message Tool(string name, string specialty) => new() { Role = ConversationRole.Assistant,
    Content = new List<ContentBlock> { new() { ToolUse = new ToolUseBlock {
        ToolUseId = "id1", Name = name, Input = ToDocument(new { specialty }) } } } };
var missing = RunAllowedLookups(Tool("get_next_appointment", "unknown"))[0].ToolResult;
Check(missing.Status == ToolResultStatus.Success);
Check(missing.Content[0].Json.AsDictionary()["next_slot"].IsNull());
var denied = RunAllowedLookups(Tool("delete_records", "general"))[0].ToolResult;
Check(denied.Status == ToolResultStatus.Error);
var duplicate = Tool("get_next_appointment", "general");
duplicate.Content.Add(duplicate.Content[0]);
Reject(() => RunAllowedLookups(duplicate));
using var native = JsonDocument.Parse("""
{"stopReason":"end_turn","output":{"message":{"content":[{"text":"Hello"}]}}}
""");
Check(ReadNativeText(native.RootElement) == "Hello");
using var truncated = JsonDocument.Parse("""
{"stopReason":"max_tokens","output":{"message":{"content":[{"text":"Partial"}]}}}
""");
Reject(() => ReadNativeText(truncated.RootElement));
Console.WriteLine($"{checks} C# contract checks passed; no AWS calls.");
