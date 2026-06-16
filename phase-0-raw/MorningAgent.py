import os
from google import genai
from dotenv import load_dotenv
from google.genai import types

from tools import weather_tool, quotes_tool, tasks_tool
from tools import get_weather, get_quotes, get_tasks

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

config = types.GenerateContentConfig(
    tools=[weather_tool, quotes_tool, tasks_tool]
)

history = []

TOOLS = {
    "get_weather": get_weather,
    "get_quotes": get_quotes,
    "get_tasks": get_tasks
}

def tool_chain(part):
    while part.function_call:
        fc = part.function_call
        args = dict(fc.args) if fc.args else {}

        print(f"\n🔧 Calling: {fc.name} with {args}")
        result = TOOLS[fc.name](**args)
        print(f"📦 Result: {result}")

        history.append({
            "role": "model",
            "parts": [part.model_dump()]
        })

        history.append({
            "role": "user",
            "parts": [{
                "function_response": {
                    "name": fc.name,
                    "response": result
                }
            }]
        })

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=history,
            config=config
        )

        part = response.candidates[0].content.parts[0]

    print("\n🤖", part.text)
    history.append({
        "role": "model",
        "parts": [{"text": part.text}]
    })


while True:
    userInput = input("> ")

    if not userInput:
        print("closing the chat")
        break

    history.append({
        "role": "user",
        "parts": [{"text": userInput}]
    })

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=history,
        config=config
    )

    part = response.candidates[0].content.parts[0]

    if part.function_call:
        tool_chain(part)
    else:
        print("\n🤖", part.text)
        history.append({
            "role": "model",
            "parts": [{"text": part.text}]
        })


client.close()