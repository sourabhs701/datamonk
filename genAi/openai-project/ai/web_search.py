from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def call_web_search(query):
    completion = client.chat.completions.create(
        model="gpt-4o-search-preview", 
        web_search_options={
            "search_context_size": "low"
        },
        messages=[
            {
                "role": "user", 
                "content": query
            }
        ],
        max_tokens=3000
    )
    return completion.choices[0].message.content

