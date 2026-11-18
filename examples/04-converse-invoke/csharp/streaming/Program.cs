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
var request = new ConverseStreamRequest
{
    ModelId = (Environment.GetEnvironmentVariable("NOVA_MODEL_ID") ?? "us.amazon.nova-lite-v1:0"),
    Messages = new List<Message>
    {
        new Message
        {
            Role = ConversationRole.User,
            Content = new List<ContentBlock> { new ContentBlock { Text = "Write a short, reassuring welcome message for a patient using our clinic's appointment portal for the first time." } }
        }
    },
    InferenceConfig = new InferenceConfiguration { MaxTokens = 300, Temperature = 0.5F }
};

var response = await client.ConverseStreamAsync(request);

// Each event carries a small piece of the answer; we print them as they arrive.
var complete = false;
await foreach (var chunk in response.Stream)
{
    if (chunk is MessageStopEvent stop)
        complete = stop.StopReason == StopReason.End_turn || stop.StopReason == StopReason.Stop_sequence;
    if (chunk is ContentBlockDeltaEvent delta && delta.Delta.Text != null)
    {
        Console.Write(delta.Delta.Text);
    }
}
if (!complete) throw new InvalidOperationException("Stream incomplete");
Console.WriteLine();
