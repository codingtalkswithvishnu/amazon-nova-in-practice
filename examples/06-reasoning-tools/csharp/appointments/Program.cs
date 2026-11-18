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
var modelId = (Environment.GetEnvironmentVariable("NOVA_MODEL_ID") ?? "us.amazon.nova-pro-v1:0");

// Step 1: describe the tool to the model.
var schema = ToDocument(new Dictionary<string, object>
{
    ["type"] = "object",
    ["properties"] = new Dictionary<string, object>
    {
        ["specialty"] = new Dictionary<string, object>
            { ["type"] = "string", ["description"] = "e.g. cardiology, general" }
    },
    ["required"] = new[] { "specialty" }
});

var toolConfig = new ToolConfiguration
{
    Tools = new List<Tool>
    {
        new Tool { ToolSpec = new ToolSpecification
        {
            Name = "get_next_appointment",
            Description = "Get the next available appointment slot for a medical specialty.",
            InputSchema = new ToolInputSchema { Json = schema }
        }}
    }
};

var messages = new List<Message>
{
    new Message { Role = ConversationRole.User,
        Content = new List<ContentBlock> { new ContentBlock { Text = "When is the next cardiology appointment available?" } } }
};

// Bound requests and stop immediately when the model gives a final answer.
for (var attempt = 0; attempt < 4; attempt++)
{
    var response = await client.ConverseAsync(new ConverseRequest
    {
        ModelId = modelId, Messages = messages, ToolConfig = toolConfig,
        InferenceConfig = new InferenceConfiguration { MaxTokens = 500, Temperature = 0F }
    });
    if (response.StopReason != StopReason.Tool_use)
    {
        Console.WriteLine(ReadFinalText(response));
        return;
    }
    messages.Add(response.Output.Message);
    var results = RunAllowedLookups(response.Output.Message);
    messages.Add(new Message { Role = ConversationRole.User, Content = results });
}
throw new InvalidOperationException("Tool loop exhausted its request budget");
