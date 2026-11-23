import requests, sys

from openai import OpenAI


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
        messages=[{"role": "user", "content": prompt}]
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
