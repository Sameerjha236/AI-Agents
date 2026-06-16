import requests
from google.genai import types
import random

def get_random_number(size):
    return random.randint(0, size)

quotes_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_quotes",
            description="Get a random motivational quote",
            parameters={
                "type": "object",
                "properties": {}
            }
        )
    ]
)

def get_quotes():
    response = requests.get("https://type.fit/api/quotes")

    qoutes = response.json()
    randomInd = get_random_number(len(qoutes)-1)

    return qoutes[randomInd]
