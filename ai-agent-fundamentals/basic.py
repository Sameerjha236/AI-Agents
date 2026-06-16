import os 
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

while True:
    user_input = input("> ")
    if(len(user_input) == 0):
        break

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input,

    )

    print(response.text)