import asyncio
import logging
import random
import sys
import time

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
import json

TOKEN = "7104080784:AAFiU0STuHAsW-KsFOF5cwVozmdn1UCflB0"
auth_waiting = []
users = []
admins = []
ban = []
nicknames = {}
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    nicknames[str(message.chat.id)] = str(message.chat.username)

    if message.chat.id in ban:
        pass

    elif message.chat.id not in admins and message.chat.id not in users:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)} !\nAuthorization in progress.")
        auth_waiting.append(message.chat.id)
        await bot.send_message(1363003331,
                               f"New user requesting authorization \nId: {message.chat.id} \nName: {message.chat.username}")

    elif message.chat.id not in admins and message.chat.id in users:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}! You are authorized, wait for test.")

    elif message.chat.id in admins:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)} !\n"
                             f"You are an admin.\n"
                             f"Waiting for authorization:\n")
        for i in auth_waiting:
            await message.answer(i)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    nicknames[str(message.chat.id)] = str(message.chat.username)

    if message.chat.id in ban:
        pass

    elif message.chat.id not in admins:
        await message.answer("Only admins can chat with the bot.")

    else:
        text = message.text.split()
        if text[0] == 'allow':

            if int(text[1]) in auth_waiting:
                users.append(int(text[1]))
                auth_waiting.remove(int(text[1]))
                await bot.send_message(int(text[1]), str("You are authorized! \nEnjoy!"))
                await bot.send_message(1363003331, f"New user authorized {text[1]}")
                update_json()

            else:
                await message.answer("No such user, waiting for authorization.")

        elif text[0] == 'deny':
            if int(text[1]) in auth_waiting:
                auth_waiting.remove(int(text[1]))
                await bot.send_message(int(text[1]), str("Permission denied."))
                await bot.send_message(1363003331, f"Authorisation of user {text[1]} denied")
                update_json()
            else:
                await message.answer("No such user, waiting for authorization.")

        elif text[0] == 'text':
            await tell_user(text[1])

        elif text[0] == 'users':
            await bot.send_message(1363003331, str(users))

        elif text[0] == 'all':
            await bot.send_message(1363003331, str(nicknames))

        elif text[0] == 'banned':
            await bot.send_message(1363003331, str(ban))

        elif text[0] == 'save':
            await bot.send_document(1363003331, FSInputFile(path='data.json'))
            await bot.send_document(1363003331, FSInputFile(path='users.json'))
            await bot.send_document(1363003331, FSInputFile(path='log.txt'))
            await bot.send_document(1363003331, FSInputFile(path='found.txt'))

        elif text[0] == 'ban':
            ban.append(int(text[1]))

            try:
                users.remove(int(text[1]))
            except ValueError:
                pass

            await bot.send_message(1363003331, f"User {text[1]} was successfully baned. ")
            update_json()

        elif text[0] == 'free':
            ban.remove(int(text[1]))
            await bot.send_message(1363003331, f"User {text[1]} is free. ")
            update_json()

        elif text[0] == 'delete':
            await bot.send_message(int(text[1]), 'Administrator deleted you.')
            users.remove(int(text[1]))
            await bot.send_message(1363003331, f"User {text[1]} was successfully deleted. ")
            update_json()

        else:
            await bot.send_message(1363003331, f"No such command")


def update_json():
    try:
        with open('users.json', 'w') as f:
            data = {}
            data['admins'] = admins
            data['users'] = users
            data['ban'] = ban
            data['nicknames'] = nicknames
            json.dump(data, f)
            del data
    except Exception as e:
        exit(e)


async def tell_user(text: str):
    for i in users:
        await bot.send_message(i, text)


async def main() -> None:
    await dp.start_polling(bot)


async def broadcaster(st: str):
    try:
        await tell_user(st)
    except Exception as e:
        exit(e)


async def get_info():
    print("begin")
    while True:
        r = random.randrange(0, 10)
        time.sleep(r)
        await broadcaster(str(r * 19))


if __name__ == "__main__":
    try:
        with open('users.json', 'r', errors='ignore') as file:
            data = dict(json.load(file))
            print(data)
            users = data.get('users')
            admins = data.get('admins')
            nicknames = dict(data.get('nicknames'))
            ban = data.get('ban')

    except FileNotFoundError:
        exit("Add users.json file")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(get_info())
    asyncio.run(main())
