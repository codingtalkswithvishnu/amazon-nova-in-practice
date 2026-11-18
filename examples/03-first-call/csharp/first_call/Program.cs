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


// The Bedrock runtime client, pointed at the region where Nova access is enabled.
using var client = new AmazonBedrockRuntimeClient(RegionEndpoint.GetBySystemName(Environment.GetEnvironmentVariable("AWS_REGION") ?? "us-east-1"));

// Confirm the exact model ID for your account/region in the Bedrock console.
var modelId = (Environment.GetEnvironmentVariable("NOVA_MODEL_ID") ?? "us.amazon.nova-lite-v1:0");

var request = new ConverseRequest
{
    ModelId = modelId,
    Messages = new List<Message>
    {
        new Message
        {
            Role = ConversationRole.User,
            Content = new List<ContentBlock>
            {
                new ContentBlock { Text = "In two sentences, explain what Amazon Bedrock is to a new engineer." }
            }
        }
    },
    InferenceConfig = new InferenceConfiguration { MaxTokens = 300, Temperature = 0.3F }
};

var response = await client.ConverseAsync(request);

// The model's text sits inside the returned structure. Chapter 4 explains it fully.
Console.WriteLine(ReadFinalText(response));
