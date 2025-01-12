import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Handler for `/start` and `/help` commands
@dp.message(Command(commands=["start", "help"]))
async def command_start_handler(message: Message):
    """
    This handler receives messages with `/start` or `/help` commands.
    """
    await message.reply("Hi\nI am Echo Bot!\nPowered by aiogram and made by the Sakshi.")

# Handler for echoing all other messages
@dp.message()
async def echo(message: Message):
    """
    This will echo back any received message.
    """
    await message.answer(message.text)

if __name__ == "__main__":
    import asyncio

    async def main():
        # Start the bot
        await dp.start_polling(bot)

    asyncio.run(main())
