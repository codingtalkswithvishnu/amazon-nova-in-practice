using static NovaBook.Support;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Amazon;
using Amazon.BedrockRuntime;
using Amazon.BedrockRuntime.Model;
using Amazon.Runtime.Documents;

if (!args.Contains("--live"))
{
    Console.WriteLine("Build checked. For a paid AWS call, configure identity and pass --live.");
    return;
}


using var client = new AmazonBedrockRuntimeClient(RegionEndpoint.GetBySystemName(Environment.GetEnvironmentVariable("AWS_REGION") ?? "us-east-1"));

var clinicalNote =
    "Patient is a 54-year-old with a dry cough for 5 days and mild fever. " +
    "On amlodipine for hypertension. No known allergies.";

// The tool's input schema IS the output shape we want back, expressed as a JSON schema document.
var schema = ToDocument(new Dictionary<string, object>
{
    ["type"] = "object",
    ["properties"] = new Dictionary<string, object>
    {
        ["age"] = new Dictionary<string, object> { ["type"] = new[] { "integer", "null" } },
        ["chief_complaint"] = new Dictionary<string, object> { ["type"] = new[] { "string", "null" } },
        ["duration_days"] = new Dictionary<string, object> { ["type"] = new[] { "integer", "null" } },
        ["fever"] = new Dictionary<string, object> { ["type"] = new[] { "boolean", "null" } },
        ["medications"] = new Dictionary<string, object> { ["type"] = new[] { "array", "null" }, ["items"] = new Dictionary<string, object> { ["type"] = "string" } },
        ["allergies"] = new Dictionary<string, object> { ["type"] = new[] { "array", "null" }, ["items"] = new Dictionary<string, object> { ["type"] = "string" } },
    },
    ["required"] = new[] { "age", "chief_complaint", "duration_days", "fever",
        "medications", "allergies" },
    ["additionalProperties"] = false
});

var request = new ConverseRequest
{
    ModelId = (Environment.GetEnvironmentVariable("NOVA_MODEL_ID") ?? "us.amazon.nova-lite-v1:0"),
    System = new List<SystemContentBlock>
    {
        new SystemContentBlock { Text = "Extract only what is explicitly stated. Use null for anything absent. Never guess." }
    },
    Messages = new List<Message>
    {
        new Message { Role = ConversationRole.User,
            Content = new List<ContentBlock> { new ContentBlock { Text = "Clinical note:\n" + clinicalNote } } }
    },
    ToolConfig = new ToolConfiguration
    {
        Tools = new List<Tool>
        {
            new Tool { ToolSpec = new ToolSpecification
            {
                Name = "record_extracted_fields",
                Description = "Record the structured fields extracted from a clinical note.",
                InputSchema = new ToolInputSchema { Json = schema }
            }}
        },
        // Force the model to use our tool, so we always get structured output.
        ToolChoice = new ToolChoice { Tool = new SpecificToolChoice { Name = "record_extracted_fields" } }
    },
    InferenceConfig = new InferenceConfiguration { MaxTokens = 500, Temperature = 0F }
};

var response = await client.ConverseAsync(request);

// Shape validation remains an application responsibility.
if (response.StopReason != StopReason.Tool_use)
    throw new InvalidOperationException("Expected a complete extraction call");
var calls = response.Output.Message.Content.Where(b => b.ToolUse != null).ToList();
if (calls.Count != 1 || calls[0].ToolUse.Name != "record_extracted_fields")
    throw new InvalidOperationException("Expected one extraction call");
Console.WriteLine(ValidateExtractedFields(calls[0].ToolUse.Input));
