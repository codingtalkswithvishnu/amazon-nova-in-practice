using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Amazon;
using Amazon.BedrockAgentRuntime;
using Amazon.BedrockAgentRuntime.Model;
using Amazon.Runtime.Documents;

if (!args.Contains("--live"))
{
    Console.WriteLine("Build checked. For a paid AWS call, configure identity and pass --live.");
    return;
}


// Knowledge Base operations use the Bedrock Agent Runtime client.
using var client = new AmazonBedrockAgentRuntimeClient(RegionEndpoint.GetBySystemName(Environment.GetEnvironmentVariable("AWS_REGION") ?? "us-east-1"));

var knowledgeBaseId = Environment.GetEnvironmentVariable("NOVA_KNOWLEDGE_BASE_ID") ?? throw new InvalidOperationException("Set NOVA_KNOWLEDGE_BASE_ID");          // created once in the Bedrock console
var modelArn = Environment.GetEnvironmentVariable("NOVA_GENERATION_MODEL_ARN") ?? throw new InvalidOperationException("Set NOVA_GENERATION_MODEL_ARN");

var response = await client.RetrieveAndGenerateAsync(new RetrieveAndGenerateRequest
{
    Input = new RetrieveAndGenerateInput
    {
        Text = "What are the fictional clinic Saturday opening hours?"
    },
    RetrieveAndGenerateConfiguration = new RetrieveAndGenerateConfiguration
    {
        Type = RetrieveAndGenerateType.KNOWLEDGE_BASE,
        KnowledgeBaseConfiguration = new KnowledgeBaseRetrieveAndGenerateConfiguration
        {
            KnowledgeBaseId = knowledgeBaseId,
            ModelArn = modelArn
        }
    }
});

// A grounded answer, plus citations back to your source documents.
Console.WriteLine(response.Output.Text);
foreach (var citation in response.Citations ?? new List<Citation>())
    foreach (var reference in citation.RetrievedReferences ?? new List<RetrievedReference>())
        Console.WriteLine("Source: " + reference.Location);
