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
var imageBytes = await File.ReadAllBytesAsync("fixtures/synthetic_form_photo.jpg");

var request = new ConverseRequest
{
    ModelId = (Environment.GetEnvironmentVariable("NOVA_MODEL_ID") ?? "us.amazon.nova-lite-v1:0"),
    Messages = new List<Message>
    {
        new Message
        {
            Role = ConversationRole.User,
            Content = new List<ContentBlock>
            {
                new ContentBlock { Text = "This is a photo of a patient intake form. List which fields are filled in and which are left blank." },
                new ContentBlock { Image = new ImageBlock
                {
                    Format = ImageFormat.Jpeg,
                    Source = new ImageSource { Bytes = new MemoryStream(imageBytes) }
                }}
            }
        }
    },
    InferenceConfig = new InferenceConfiguration { MaxTokens = 500, Temperature = 0F }
};

var response = await client.ConverseAsync(request);
Console.WriteLine(ReadFinalText(response));
