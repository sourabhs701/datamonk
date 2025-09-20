from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def call_api(messages, tools=None):
    completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo-0613", 
        tools=tools,
        messages=messages,
        max_tokens=3000   
    )
    return completion