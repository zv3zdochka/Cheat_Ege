import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BufferedInputFile
from aiogram.utils.markdown import hbold
import time
import os


LOG_FILE = os.getcwd() + f"/logs/log{time.gmtime().tm_hour}.{time.gmtime().tm_min}.{time.gmtime().tm_sec}.log"
AMIN_ID = None


TOKEN = "YOUR_TOKEN_HERE"
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user is not None:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
        await message.answer_dice()
    else:
        await message.answer("Who tf are you?")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=LOG_FILE)
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()
