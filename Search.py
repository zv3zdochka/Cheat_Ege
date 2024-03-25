try:
    import time
    import sys
    import os
    from bs4 import BeautifulSoup
    from concurrent.futures import ThreadPoolExecutor
    import concurrent
    import typing
    import requests
    from requests.auth import HTTPProxyAuth
    import json
    from sdamgia import SdamGIA
    import datetime
    import asyncio
    import logging
    from aiogram import Bot, Dispatcher, types
    from aiogram.enums import ParseMode
    from aiogram.filters import CommandStart, Command
    from aiogram.types import Message, BufferedInputFile, FSInputFile
    from aiogram.utils.markdown import hbold
    from aiogram import exceptions
    import random

except ModuleNotFoundError:
    sys.exit("Required libraries are missing. Please install them using:\n"
             "pip install -r requirements.txt\n"
             "You can find the requirements.txt file at: https://github.com/zv3zdochka/LAW.git")

TOKEN = "7104080784:AAFiU0STuHAsW-KsFOF5cwVozmdn1UCflB0"
auth_waiting = []
users = []
admins = []
ban = []
sleep_time = 10
nicknames = {}
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

logging.basicConfig(level=logging.INFO, filename='log.txt')
log = logging.getLogger('broadcast')

proxies = {
    "http": "http://45.11.20.11:3000",
    "socks": "socks5://45.11.20.11:3001"
}

auth = ('xj1DIJ', 'GgyGrVxW')


class PageChecker:
    def __init__(self, subject_name, targets, start, threads_number=3):
        self.workers = threads_number
        self.subject_name = subject_name
        self.targets = targets
        self.current_num = 0
        self.subject_url = self.subject_url_by_name(subject_name)
        self.founded = []
        self.start_id = self.get_current_test_num_start() - 20

    def check_page(self, page_id):
        if page_id is None:
            return
        url = f"{self.subject_url}/test?id={page_id}"
        print(url)

        try:
            with requests.Session() as session:
                response = session.get(url, proxies=proxies, auth=auth)

                if response.status_code == 200:
                    text = BeautifulSoup(response.text, 'html.parser').get_text()

                    if len(text) == 118:
                        return f"Page not found: {page_id}"

                    for target in self.targets:
                        if target in text:
                            return f"Target {target} found on page {page_id}"

                    if "JavaScript" in text:
                        return f"JavaScript detected on the page {id}"

        except Exception as e:
            log.log(40, f"Exception processing page {page_id}. On time {datetime.datetime.now()}\n")
            return f"Error processing page {page_id}: {e}"

    def get_current_test_num_start(self):
        try:
            sdamgia = SdamGIA()
            num = int(sdamgia.generate_test(self.subject_name, {1: 1}))
            del sdamgia
            return num
        except KeyError:
            log.log(40, f"Vpn or proxy error. On time {datetime.datetime.now()}\n")
            exit("Switch off your VPN and try again")

    def get_current_test_num(self):
        try:
            sdamgia = SdamGIA()
            self.current_num = int(sdamgia.generate_test(self.subject_name, {1: 1}))
            del sdamgia
        except KeyError:
            log.log(40, f"Vpn or proxy error. On time {datetime.datetime.now()}\n")
            exit("Switch off your VPN and try again")

    def id_generator_up(self):
        self.get_current_test_num()
        while self.start_id <= self.current_num:
            yield self.start_id
            self.start_id += 1
        else:
            while True:
                yield None

    def main(self, generator):
        with ThreadPoolExecutor(max_workers=self.workers) as worker:
            ids = generator()
            futures = {worker.submit(self.check_page, next(ids)): id for id in range(50)}
            while futures:

                done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

                for future in done:
                    page_id = futures.pop(future)

                    try:
                        result = future.result()
                        if result:
                            self.founded.append([self.subject_name, result])

                    except Exception as exc:
                        log.log(40, f"Exception processing page {page_id}: {exc}. On time {datetime.datetime.now()}\n")

                    new_id = next(ids)
                    if new_id is None:
                        break
                    futures[worker.submit(self.check_page, new_id)] = new_id
            worker.shutdown(wait=True)

    def search_from_to(self):
        self.main(self.id_generator_up)

    @staticmethod
    def subject_url_by_name(name):
        subjects = {
            'math': 'https://math-ege.sdamgia.ru',
            'mathb': 'https://mathb-ege.sdamgia.ru',
            'phys': 'https://phys-ege.sdamgia.ru',
            'inf': 'https://inf-ege.sdamgia.ru',
            'rus': 'https://rus-ege.sdamgia.ru',
            'bio': 'https://bio-ege.sdamgia.ru',
            'en': 'https://en-ege.sdamgia.ru',
            'chem': 'https://chem-ege.sdamgia.ru',
            'geo': 'https://geo-ege.sdamgia.ru',
            'soc': 'https://soc-ege.sdamgia.ru',
            'de': 'https://de-ege.sdamgia.ru',
            'fr': 'https://fr-ege.sdamgia.ru',
            'lit': 'https://lit-ege.sdamgia.ru',
            'sp': 'https://sp-ege.sdamgia.ru',
            'hist': 'https://hist-ege.sdamgia.ru',
        }
        return subjects.get(name)


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


async def search():
    global sleep_time, data, data_u
    while True:

        s_t = time.time()
        for key, value in data.items():

            pch = PageChecker(key, value[0], value[1], threads)
            pch.search_from_to()
            if pch.founded:
                for j in pch.founded:
                    asyncio.run(broadcaster(f"New test found\n"
                                            f"Subject: {pch.subject_name}\n"
                                            f"Test id: {j}"))

                with open('found.txt', 'a') as f:
                    f.write(f"Found in subject {j[0]}: {j[1]}. On time {datetime.datetime.now()}\n")

            n_d = data[pch.subject_name]
            n_d[1] = pch.current_num
            data[pch.subject_name] = n_d
            del pch
        with open(inp[0], 'w') as file:
            json.dump(data, file, ensure_ascii=False)

        print('cycle')

        if time.time() - s_t < 5:
            sleep_time += 1
        elif time.time() - s_t > 15:
            sleep_time -= 1

        print(sleep_time)

        time.sleep(sleep_time)


if __name__ == "__main__":
    inp = sys.argv[1:]
    if len(inp) != 2:
        with open('log.txt', 'a') as f:
            log.log(40, "Wrong command. On time {datetime.datetime.now()}\n")
        exit('Usage: python Search.py nameoffile.json quantity_of_threads')
    threads = int(inp[1])
    if not (1 <= threads <= 16):
        log.log(40, f"Invalid number of threads. On time {datetime.datetime.now()}\n")
        exit("Invalid number of threads. Please choose a value between 1 and 16. Recommended number of threads is 2~3.")
    try:
        with open(inp[0], 'r', errors='ignore', encoding='windows-1251') as file:
            data = json.load(file)

            for key, value in data.items():
                data[key] = [value[0], value[1]]

    except FileNotFoundError:
        log.log(40, f"No data file. On time {datetime.datetime.now()}\n")
        exit("Add data.json file")

    try:
        with open('users.json', 'r', errors='ignore') as file:

            data_u = dict(json.load(file))
            users = data_u.get('users')
            admins = data_u.get('admins')
            nicknames = dict(data_u.get('nicknames'))
            ban = data_u.get('ban')

    except FileNotFoundError:
        exit("Add users.json file")
    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(main()),
        ioloop.create_task(search())
    ]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()

