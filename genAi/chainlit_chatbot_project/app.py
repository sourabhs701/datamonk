import chainlit as cl
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

FINANCE_BOT_SYSTEM_PROMPT = (
    "You are a friendly finance assistant. You explain complex financial "
    "concepts in a clear and simple way, suitable for a beginner. "
    "Avoid jargon where possible."
)

# Store conversation history
@cl.on_chat_start
async def start():
    cl.user_session.set("messages", [
        {"role": "system", "content": FINANCE_BOT_SYSTEM_PROMPT}
    ])

# Action callback when the user clicks "Give me an example"
@cl.action_callback("give_example")
async def on_action(action: cl.Action):
    topic = action.payload["topic"]

    try:
        response = await client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": FINANCE_BOT_SYSTEM_PROMPT},
                {"role": "user", "content": f"Give me a simple, real-world example of {topic}."}
            ]
        )
        await cl.Message(content=response.choices[0].message.content).send()
    except Exception as e:
        await cl.Message(content=f"Sorry, I encountered an error: {str(e)}").send()

# Main chatbot logic
@cl.on_message
async def main(message: cl.Message):
    # Get conversation history
    messages = cl.user_session.get("messages", [])
    messages.append({"role": "user", "content": message.content})

    try:
        response = await client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=messages
        )

        bot_response = response.choices[0].message.content

        # Add bot response to history
        messages.append({"role": "assistant", "content": bot_response})
        cl.user_session.set("messages", messages)

        # Create action with better topic extraction
        # You might want to improve this logic based on your needs
        actions = [
            cl.Action(
                name="give_example",
                payload={"topic": message.content},
                label="Give me an example"
            )
        ]

        await cl.Message(content=bot_response, actions=actions).send()

    except Exception as e:
        await cl.Message(content=f"Sorry, I encountered an error: {str(e)}").send()
