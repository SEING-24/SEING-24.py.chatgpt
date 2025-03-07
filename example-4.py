"""
This script uses the OpenAI API to simulate a chat-based assistant that helps users find flight information between two cities.

Modules:
    - os: Provides a way of using operating system dependent functionality.
    - json: Provides functions for working with JSON data.
    - openai: Provides access to the OpenAI API.

Functions:
    - get_flight_info(origin_city: str, destination_city: str): Returns mock flight information between two cities.
    
Variables:
    - token: The API token retrieved from the environment variable "GITHUB_TOKEN".
    - endpoint: The API endpoint for the OpenAI service.
    - model_name: The name of the model to use for the OpenAI API.
    - tool: A dictionary defining the function tool that the model can invoke to retrieve flight information.
    - client: An instance of the OpenAI client initialized with the endpoint and API token.
    - messages: A list of messages representing the chat history.
    - response: The response from the OpenAI API after sending the chat messages and tool definition.

Usage:
    The script initializes the OpenAI client and sends a chat message asking for flight information from Seattle to Miami.
    If the model requests a tool call, the script invokes the `get_flight_info` function with the provided arguments,
    appends the result to the chat history, and sends another request to the model to continue the conversation.
"""

import os
import json
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

# Define a function that returns flight information between two cities (mock implementation)
def get_flight_info(origin_city: str, destination_city: str):
    if origin_city == "Seattle" and destination_city == "Miami":
        return json.dumps({
            "airline": "Delta",
            "flight_number": "DL123",
            "flight_date": "May 7th, 2024",
            "flight_time": "10:00AM"})
    return json.dumps({"error": "No flights found between the cities"})

# Define a function tool that the model can ask to invoke in order to retrieve flight information
tool={
    "type": "function",
    "function": {
        "name": "get_flight_info",
        "description": """Returns information about the next flight between two cities.
            This includes the name of the airline, flight number and the date and time
            of the next flight""",
        "parameters": {
            "type": "object",
            "properties": {
                "origin_city": {
                    "type": "string",
                    "description": "The name of the city where the flight originates",
                },
                "destination_city": {
                    "type": "string", 
                    "description": "The flight destination city",
                },
            },
            "required": [
                "origin_city",
                "destination_city"
            ],
        },
    },
}

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

messages=[
    {"role": "system", "content": "You are an assistant that helps users find flight information."},
    {"role": "user", "content": "I'm interested in going to Miami. What is the next flight there from Seattle?"},
]

response = client.chat.completions.create(
    messages=messages,
    tools=[tool],
    model=model_name,
)

# We expect the model to ask for a tool call
if response.choices[0].finish_reason == "tool_calls":

    # Append the model response to the chat history
    messages.append(response.choices[0].message)

    # We expect a single tool call
    if response.choices[0].message.tool_calls and len(response.choices[0].message.tool_calls) == 1:

        tool_call = response.choices[0].message.tool_calls[0]

        # We expect the tool to be a function call
        if tool_call.type == "function":

            # Parse the function call arguments and call the function
            function_args = json.loads(tool_call.function.arguments.replace("'", '"'))
            print(f"Calling function `{tool_call.function.name}` with arguments {function_args}")
            callable_func = locals()[tool_call.function.name]
            function_return = callable_func(**function_args)
            print(f"Function returned = {function_return}")

            # Append the function call result fo the chat history
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": function_return,
                }
            )

            # Get another response from the model
            response = client.chat.completions.create(
                messages=messages,
                tools=[tool],
                model=model_name,
            )

            print(f"Model response = {response.choices[0].message.content}")