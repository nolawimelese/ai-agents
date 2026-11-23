import requests, sys, json
from typing import Any

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

    # model loop
    # we get 10 total turns to do a task

    messages: list[Any] = [{"role": "user", "content": prompt}]

    for _ in range(10):
        response = client.chat.completions.create(
        model="qwen3.5-0.8b",
        messages = messages,
        tools=tools,
        tool_choice="auto",
        )

        message = response.choices[0].message

        # respond if no tool request
        if not message.tool_calls:
            print(message.content)
            break
        # add additional 
        messages.append(message.model_dump(exclude_none=True))

        for tool_call in message.tool_calls:

            # tool call should be a function only
            if tool_call.type != "function":
                raise ValueError("Expected a function tool call")

            name = tool_call.function.name

            print(f"Using {name} tool")

            # convert to python dict
            arguments = json.loads(tool_call.function.arguments)

            function = TOOL_REGISTRY[name]

            # unpack args and call the tool (function)
            result = function(**arguments)

            messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result),
            })


if __name__ == "__main__":
    main()
