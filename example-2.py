"""
This script demonstrates a multi-turn conversation with the OpenAI chat completion API.

The script performs the following steps:
1. Imports necessary libraries and modules.
2. Retrieves the API token from environment variables.
3. Sets the endpoint URL and model name for the OpenAI API.
4. Initializes the OpenAI client with the specified endpoint and API key.
5. Creates a chat completion request with a series of messages to simulate a conversation.
6. Prints the response from the assistant.

The conversation includes:
- A system message defining the assistant's role.
- A user query about the capital of France.
- The assistant's response with the capital of France.
- A follow-up user query about the capital of Spain.

Environment Variables:
- GITHUB_TOKEN: The API token for authenticating with the OpenAI API.

Dependencies:
- openai: The OpenAI Python client library.
- os: Standard library for accessing environment variables.
"""
import os
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What is the capital of France?",
        },
        {
            "role": "assistant",
            "content": "The capital of France is Paris.",
        },
        {
            "role": "user",
            "content": "What about Spain?",
        }
    ],
    model=model_name,
)

print(response.choices[0].message.content)