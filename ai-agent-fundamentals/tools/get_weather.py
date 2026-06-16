# tools/get_weather.py

import requests

from google.genai import types

weather_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="Get current weather for a city",
            parameters={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name"
                    }
                },
                "required": ["city"]
            }
        )
    ]
)
def get_weather(city):
    response = requests.get(
        "http://api.weatherapi.com/v1/current.json",
        params={
            "key": "303113d3d7844da187a65852261006",
            "q": city,
            "aqi": "no"
        }
    )

    data = response.json()

    return {
        "city": data["location"]["name"],
        "temperature": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"]
    }