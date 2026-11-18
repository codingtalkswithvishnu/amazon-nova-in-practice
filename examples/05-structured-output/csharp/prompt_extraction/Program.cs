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

// Synthetic note — never use real patient data while developing.
var clinicalNote =
    "Patient is a 54-year-old presenting with a dry cough for 5 days and mild fever. " +
    "No shortness of breath. History of hypertension, on amlodipine. No known allergies.";

var request = new ConverseRequest
{
    ModelId = (Environment.GetEnvironmentVariable("NOVA_MODEL_ID") ?? "us.amazon.nova-lite-v1:0"),
    System = new List<SystemContentBlock>
    {
        new SystemContentBlock { Text =
            "You are a careful clinical-documentation assistant. " +
            "Extract only what is explicitly stated. If a field is not mentioned, use null. " +
            "Never infer, guess, or add a diagnosis. Return valid JSON only, with no extra text." }
    },
    Messages = new List<Message>
    {
        new Message
        {
            Role = ConversationRole.User,
            Content = new List<ContentBlock> { new ContentBlock { Text =
                "Extract these fields from the clinical note as JSON with keys " +
                "age, chief_complaint, duration_days, fever (true/false/null), " +
                "medications (list), allergies (list).\n\n" +
                "Clinical note:\n" + clinicalNote } }
        }
    },
    InferenceConfig = new InferenceConfiguration { MaxTokens = 400, Temperature = 0F }
};

var response = await client.ConverseAsync(request);
Console.WriteLine(ReadFinalText(response));
