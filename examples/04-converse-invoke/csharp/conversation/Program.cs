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
var modelId = (Environment.GetEnvironmentVariable("NOVA_MODEL_ID") ?? "us.amazon.nova-lite-v1:0");

var request = new ConverseRequest
{
    ModelId = modelId,
    // Standing instructions, kept separate from the conversation itself.
    System = new List<SystemContentBlock>
    {
        new SystemContentBlock
        {
            Text = "You are a careful assistant for a clinic's patient-support desk. " +
                   "Answer in plain language, keep to general guidance, and never invent " +
                   "clinical details or give a diagnosis. If something sounds urgent, advise " +
                   "the patient to contact a clinician or emergency services."
        }
    },
    Messages = new List<Message>
    {
        new Message { Role = ConversationRole.User,
            Content = new List<ContentBlock> { new ContentBlock { Text = "I was asked to fast before my blood test. What does that involve?" } } },
        new Message { Role = ConversationRole.Assistant,
            Content = new List<ContentBlock> { new ContentBlock { Text = "Fasting usually means no food or drink except water for a set number of hours beforehand." } } },
        new Message { Role = ConversationRole.User,
            Content = new List<ContentBlock> { new ContentBlock { Text = "For how many hours, and can I take my regular medication?" } } },
    },
    InferenceConfig = new InferenceConfiguration { MaxTokens = 400, Temperature = 0.3F, TopP = 0.9F }
};

var response = await client.ConverseAsync(request);
Console.WriteLine(ReadFinalText(response));
