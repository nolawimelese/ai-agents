import requests, sys

from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam

def add(a, b):
    return a + b

TOOL_REGISTRY = {
    "add": add
}

# added type to make pylance happy
tools: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        }
    }
]

def main():

    # collect prompt
    prompt = input()

    # endpoint via openai
    client = OpenAI(
        base_url="http://localhost:1235/v1",
        api_key="lm-studio",
        timeout=60.0,
        max_retries=0,
    )

    response = client.chat.completions.create(
    model="qwen3.5-0.8b",
    messages=[{"role": "user", "content": prompt}],
    tools=tools,
    tool_choice="auto",
    )

    message = response.choices[0].message
    print(message.content)


if __name__ == "__main__":
    main()
