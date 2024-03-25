import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
import json

TOKEN = "6989806548:AAFDzbM1BEPG3EKeYwpGc212xw8D1HFPu3E"
auth_waiting = []
users = []
admins = []
ban = []
nicknames = {}
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    nicknames[message.chat.id] = str(message.chat.username)

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

    nicknames[message.chat.id] = str(message.chat.username)

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
            auth_waiting.remove(int(text[1]))
            await bot.send_message(int(text[1]), str("Permission denied."))
            await bot.send_message(1363003331, f"Authorisation of user {text[1]} denied")
            update_json()

        elif text[0] == 'text':
            await tell_user(text[1])

        elif text[0] == 'users':
            await bot.send_message(1363003331, str(users))

        elif text[0] == 'all':
            await bot.send_message(1363003331, str(nicknames))

        elif text[0] == 'banned':
            await bot.send_message(1363003331, str(ban))

        elif text[0] == 'ban':
            ban.append(int(text[1]))
            users.remove(int(text[1]))
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
    print(ban)
    print(users)
    print(nicknames)
    # with open('data.json', 'r') as f:
    #     data = {}
    #     data['admins'] = admins
    #     data['users'] = users
    #     json.dump(data, f)
    #     del data


async def tell_user(text: str):
    for i in users:
        await bot.send_message(i, text)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        with open('users.json', 'r', errors='ignore') as file:
            data = dict(json.load(file))
            print(data)
            users = data.get('users')
            admins = data.get('admins')

    except FileNotFoundError:
        exit("Add users.json file")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
