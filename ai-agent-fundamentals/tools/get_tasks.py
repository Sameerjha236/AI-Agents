import json
import os
from google.genai import types


tasks_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_tasks",
            description="Get a list of all the tasks",
            parameters={
                "type": "object",
                "properties": {}
            }
        )
    ]
)

def get_tasks():
    # Construct path to tasks.json relative to the tools directory
    file_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'tasks.json')
    
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
get_tasks()