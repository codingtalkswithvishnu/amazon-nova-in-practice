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

// Nova's native request format, serialised to JSON by hand.
var body = JsonSerializer.Serialize(new
{
    schemaVersion = "messages-v1",
    messages = new[]
    {
        new { role = "user", content = new[] { new { text = "Name three benefits of a managed model service." } } }
    },
    inferenceConfig = new { maxTokens = 300, temperature = 0.3 }
});

var request = new InvokeModelRequest
{
    ModelId = (Environment.GetEnvironmentVariable("NOVA_MODEL_ID") ?? "us.amazon.nova-lite-v1:0"),
    ContentType = "application/json",
    Body = new MemoryStream(Encoding.UTF8.GetBytes(body))
};

var response = await client.InvokeModelAsync(request);

// The native response is a JSON body you parse yourself.
using var doc = JsonDocument.Parse(response.Body);
Console.WriteLine(ReadNativeText(doc.RootElement));
