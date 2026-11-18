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
var modelId = "amazon.nova-reel-v1:1";              // confirm the current version ID
var s3Output = "s3://your-output-bucket/reel/";     // must exist and be writable by Bedrock

// Step 1: submit the asynchronous job.
var modelInput = ToDocument(new Dictionary<string, object>
{
    ["taskType"] = "TEXT_VIDEO",
    ["textToVideoParams"] = new Dictionary<string, object>
    {
        ["text"] = "A calm, slow pan across a bright, tidy clinic waiting room, " +
                   "warm natural light, reassuring and professional."
    },
    ["videoGenerationConfig"] = new Dictionary<string, object>
    {
        ["durationSeconds"] = 6, ["fps"] = 24, ["dimension"] = "1280x720", ["seed"] = 7
    }
});

var start = await client.StartAsyncInvokeAsync(new StartAsyncInvokeRequest
{
    ModelId = modelId,
    ModelInput = modelInput,
    OutputDataConfig = new AsyncInvokeOutputDataConfig
    {
        S3OutputDataConfig = new AsyncInvokeS3OutputDataConfig { S3Uri = s3Output }
    }
});
var invocationArn = start.InvocationArn;
Console.WriteLine("Job submitted: " + invocationArn);

// A deadline bounds monitoring; it does not cancel the server-side job.
var deadline = System.Diagnostics.Stopwatch.StartNew();
while (deadline.Elapsed < TimeSpan.FromMinutes(20))
{
    var status = await client.GetAsyncInvokeAsync(new GetAsyncInvokeRequest { InvocationArn = invocationArn });
    if (status.Status == AsyncInvokeStatus.Completed)
    {
        Console.WriteLine(status.OutputDataConfig.S3OutputDataConfig.S3Uri);
        return;
    }
    if (status.Status == AsyncInvokeStatus.Failed)
        throw new InvalidOperationException("Video job failed; inspect saved ARN");
    if (status.Status != AsyncInvokeStatus.InProgress)
        throw new InvalidOperationException("Unknown job state");
    await Task.Delay(TimeSpan.FromSeconds(15));
}
throw new TimeoutException("Monitoring timed out; job may still run: " + invocationArn);
