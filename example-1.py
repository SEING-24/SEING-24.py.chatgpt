"""
This sample demonstrates a basic call to the chat completion API. 
It is leveraging the GitHub AI model inference endpoint and your GitHub token. The call is synchronous.
"""
import os
from openai import OpenAI

def main():
    """
    Main function to interact with the OpenAI API.

    This function retrieves the GITHUB_TOKEN from the environment variables,
    sets up the OpenAI client with the specified endpoint and model name,
    and sends a chat completion request to the API. The response from the API
    is then printed to the console.

    Environment Variables:
        GITHUB_TOKEN (str): The API key for authenticating with the OpenAI service.

    API Endpoint:
        https://models.inference.ai.azure.com

    Model:
        gpt-4o-mini

    Request Parameters:
        messages (list): A list of message dictionaries to send to the API.
            Each dictionary contains a "role" (e.g., "system", "user") and "content" (str).
        model (str): The name of the model to use for the request.
        temperature (float): Sampling temperature to use for the request.
        max_tokens (int): Maximum number of tokens to generate in the response.
        top_p (float): Nucleus sampling parameter.

    Prints:
        str: The content of the first message in the response choices.
    """
    token = os.environ["GITHUB_TOKEN"]
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o-mini"

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
            }
        ],
        model=model_name,
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0
    )

    print(response.choices[0].message.content)

if __name__=='__main__':
    main()
