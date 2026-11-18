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

// A synthetic referral PDF you have on disk. Never use real patient documents.
var documentBytes = await File.ReadAllBytesAsync("fixtures/synthetic_referral.pdf");

var request = new ConverseRequest
{
    ModelId = (Environment.GetEnvironmentVariable("NOVA_MODEL_ID") ?? "us.amazon.nova-lite-v1:0"),
    System = new List<SystemContentBlock>
    {
        new SystemContentBlock { Text = "You summarise clinical referrals for a busy GP. " +
            "Be factual, concise, and never add clinical judgement." }
    },
    Messages = new List<Message>
    {
        new Message
        {
            Role = ConversationRole.User,
            Content = new List<ContentBlock>
            {
                new ContentBlock { Text = "Summarise this referral in three short bullet points: reason, relevant history, requested action." },
                new ContentBlock { Document = new DocumentBlock
                {
                    Format = DocumentFormat.Pdf,   // confirm formats for the chosen model
                    Name = "Synthetic Referral",
                    Source = new DocumentSource { Bytes = new MemoryStream(documentBytes) }
                }}
            }
        }
    },
    InferenceConfig = new InferenceConfiguration { MaxTokens = 500, Temperature = 0.2F }
};

var response = await client.ConverseAsync(request);
Console.WriteLine(ReadFinalText(response));
