import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import openai
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Model name for OpenAI
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher()

# Class to store the previous response from ChatGPT
class Reference:
    """A class to store previously received responses from the ChatGPT API."""
    def __init__(self):
        self.response = ""

reference = Reference()

# Function to clear the previous conversation and context
def clear_past():
    """Clears the previous conversation context."""
    reference.response = ""

# Start command handler
@dispatcher.message(Command("start"))
async def welcome(message: Message):
    """Sends a welcome message to the user."""
    await message.answer("Hi! I am Tele Bot, created by Sakshi. How can I assist you?")

# Help command handler
@dispatcher.message(Command("help"))
async def help_command(message: Message):
    """Provides help information to the user."""
    help_text = "Here are the commands you can use:\n" \
                "/start - Start the bot\n" \
                "/help - Get help information\n" \
                "Just type your query, and I'll respond!"
    await message.answer(help_text)

# ChatGPT handler
@dispatcher.message()
async def chatgpt_handler(message: Message):
    """
    Processes the user's input and generates a response using the ChatGPT API.
    """
    logging.info(f"USER: {message.text}")
    try:
        # Send the user's input and previous response to the ChatGPT API
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "assistant", "content": reference.response},
                {"role": "user", "content": message.text}
            ]
        )
        # Get the AI's response
        reference.response = response.choices[0].message["content"]
        logging.info(f"ChatGPT: {reference.response}")

        # Send the response back to the user
        await message.answer(reference.response)
    except Exception as e:
        logging.error(f"Error in ChatGPT handler: {e}")
        await message.answer("Sorry, something went wrong. Please try again later.")

# Main entry point
async def main():
    try:
        # Start the bot
        await dispatcher.start_polling(bot)
    except Exception as e:
        logging.error(f"Error starting the bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())
