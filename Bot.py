import asyncio
import logging
import sys
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

TOKEN = "6989806548:AAFDzbM1BEPG3EKeYwpGc212xw8D1HFPu3E"  # Replace with your bot token
auth_waiting = []
users = []
admins = []

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

async def on_startup(dp):
    logging.info("Bot started, initializing...")

    try:
        with open('users.json', 'r') as file:
            data = json.load(file)
            users.extend(data.get('users', []))
            admins.extend(data.get('admins', []))
    except FileNotFoundError:
        logging.error("users.json file not found.")
        sys.exit(1)

async def on_shutdown(dp):
    logging.info("Bot shutdown.")

@dp.message_handler(commands=['start'])
async def command_start_handler(message: types.Message) -> None:
    """
    Handler for the /start command.
    """
    if message.chat.id not in admins and message.chat.id not in users:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}!\nAuthorization in progress.")
        auth_waiting.append(message.chat.id)
        await bot.send_message(1363003331,
                               f"New user requesting authorization {message.chat.id} \nName:{message.chat.username}")

    elif message.chat.id not in admins and message.chat.id in users:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}! You are authorized, wait for test.")

    elif message.chat.id in admins:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}!\n"
                             f"You are an admin.\n"
                             f"Waiting for authorization:\n")
        for i in auth_waiting:
            await message.answer(i)

@dp.message_handler()
async def echo_handler(message: types.Message) -> None:
    """
    Handler forwards a message back to the sender.
    """
    if message.chat.id not in admins:
        await message.answer("Only admins can chat with the bot.")
    else:
        text = message.text.split()

        if text[0] == 'allow':

            if int(text[1]) in auth_waiting:
                users.append(int(text[1]))
                auth_waiting.remove(int(text[1]))
                await bot.send_message(int(text[1]), str("You are authorized! \nEnjoy!"))
                await bot.send_message(1363003331, f"New user authorized {text[1]}")

            else:
                await message.answer("No such user, waiting for authorization.")

        elif text[0] == 'deny':
            auth_waiting.remove(int(text[1]))
            await bot.send_message(int(text[1]), str("Permission denied."))

        elif text[0] == 'text':
            await tell_user(text[1])
        else:
            await bot.send_message(1363003331, f"No such command")

async def tell_user(text: str):
    for i in users:
        await bot.send_message(i, text)

async def main():
    await on_startup(dp)
    await dp.start_polling()
    await on_shutdown(dp)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
