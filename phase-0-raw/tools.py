import os
from google import genai
from dotenv import load_dotenv
from google.genai import types

from tools import weather_tool, get_weather

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

config = types.GenerateContentConfig(
    tools=[weather_tool]
)

history = []

while True:
    user_input = input("> ")

    if not user_input:
        break

    # 1. store user message
    history.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    # 2. call model
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=history,
        config=config
    )

    part = response.candidates[0].content.parts[0]

    # -------------------
    # TOOL CALL FLOW
    # -------------------
    if part.function_call:

        fc = part.function_call

        print("\n🔧 Tool requested:", fc.name)
        print("Args:", fc.args)

        # execute tool
        if fc.name == "get_weather":
            result = get_weather(**fc.args)

        # send tool call back (IMPORTANT: preserve original call)
        history.append({
            "role": "model",
            "parts": [part.model_dump()]
        })

        # send tool result
        history.append({
            "role": "user",
            "parts": [{
                "function_response": {
                    "name": fc.name,
                    "response": result
                }
            }]
        })

        # ask Gemini again for final answer
        final_response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=history,
            config=config
        )

        final_part = final_response.candidates[0].content.parts[0]

        print("\n🤖 Final:", final_part.text)

        history.append({
            "role": "model",
            "parts": [{"text": final_part.text}]
        })

    # -------------------
    # NORMAL FLOW
    # -------------------
    else:
        print("\n🤖", part.text)

        history.append({
            "role": "model",
            "parts": [{"text": part.text}]
        })

client.close()