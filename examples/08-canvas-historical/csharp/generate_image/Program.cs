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

Console.WriteLine("Historical endpoint: local compilation only. This model is retired.");
if (!args.Contains("--private-extended-access")) return;


using var client = new AmazonBedrockRuntimeClient(RegionEndpoint.GetBySystemName(Environment.GetEnvironmentVariable("AWS_REGION") ?? "us-east-1"));
var modelId = "amazon.nova-canvas-v1:0";

var nativeRequest = JsonSerializer.Serialize(new
{
    taskType = "TEXT_IMAGE",
    textToImageParams = new
    {
        text = "A clean, friendly flat illustration of a stethoscope on a pale blue " +
               "background, simple and professional, suitable for a clinic website."
    },
    imageGenerationConfig = new
    {
        numberOfImages = 1,
        width = 1024,
        height = 1024,
        quality = "standard",   // or "premium"
        seed = 42               // fixed seed -> repeatable image
    }
});

var response = await client.InvokeModelAsync(new InvokeModelRequest
{
    ModelId = modelId,
    ContentType = "application/json",
    Body = new MemoryStream(Encoding.UTF8.GetBytes(nativeRequest))
});

using var doc = JsonDocument.Parse(response.Body);
// Images come back as Base64 strings; decode and save the first one.
var base64Image = doc.RootElement.GetProperty("images")[0].GetString();
await File.WriteAllBytesAsync("stethoscope.png", Convert.FromBase64String(base64Image!));
Console.WriteLine("Saved stethoscope.png");
