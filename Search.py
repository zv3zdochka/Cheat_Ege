try:
    import datetime
    import aiohttp
    from bs4 import BeautifulSoup
    from sdamgia import SdamGIA
    import asyncio
    import sys
    import time
    from aiogram import Bot, Dispatcher, types
    from aiogram.types import Message, FSInputFile
    from aiogram.utils.markdown import hbold
    from aiogram.enums import ParseMode
    from aiogram.filters import CommandStart
    import json

except ModuleNotFoundError:
    sys.exit("Required libraries are missing. Please install them using:\n"
             "pip install -r requirements.txt\n"
             "You can find the requirements.txt file at: https://github.com/zv3zdochka/LAW.git")

TOKEN = "7104080784:AAFiU0STuHAsW-KsFOF5cwVozmdn1UCflB0"
auth_waiting = []
users = []
admins = []
ban = []
nicknames = {}
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

proxies = {
    "http": "http://45.11.20.11:3000",
    "socks": "socks5://45.11.20.11:3001"
}

auth = ('xj1DIJ', 'GgyGrVxW')


class PageChecker:
    def __init__(self, subject_name, targets, start):
        self.start_id = start
        self.subject_name = subject_name
        self.targets = targets
        self.current_num = 0
        self.subject_url = self.subject_url_by_name(subject_name)
        self.founded = []

    async def check_page(self, session, page_id):
        if page_id is None:
            return

        url = f"{self.subject_url}/test?id={page_id}"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    text = BeautifulSoup(html, 'html.parser').get_text()

                    if len(text) == 118:
                        return f"Page not found: {page_id}"

                    for target in self.targets:
                        if target in text:
                            return f"Target {target} found on page {page_id}"

                    if "JavaScript" in text:
                        return f"JavaScript detected on the page {id}"

        except Exception as e:
            with open('log.txt', 'a') as f:
                f.write(f"Exception processing page {page_id}. On time {datetime.datetime.now()}\n")
            return f"Error processing page {page_id}: {e}"

    async def fetch_all(self, ids):
        async with aiohttp.ClientSession() as session:
            tasks = [self.check_page(session, page_id) for page_id in ids]
            return await asyncio.gather(*tasks)

    async def main(self, generator):
        ids = generator()
        while True:
            chunk = [next(ids) for _ in range(50)]
            results = await self.fetch_all(chunk)
            for page_id, result in zip(chunk, results):
                if result:
                    self.founded.append([self.subject_name, result])
                    print(result)
            if None in chunk:
                break

    async def search_from_to(self):
        await self.main(self.id_generator_up)

    def id_generator_up(self):
        self.get_current_test_num()
        while self.start_id <= self.current_num:
            yield self.start_id
            self.start_id += 1
        else:
            while True:
                yield None

    def get_current_test_num(self):
        try:
            sdamgia = SdamGIA()
            self.current_num = int(sdamgia.generate_test(self.subject_name, {1: 1}))
            del sdamgia
        except KeyError:
            with open('log.txt', 'a') as f:
                f.write(f"Vpn or proxy error. On time {datetime.datetime.now()}\n")
            exit("Switch off your VPN and try again")

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
    # main loop
    sleep_time = 15
    while True:
        s_t = time.time()
        print(data)
        for key, value in data.items():
            pch = PageChecker(key, value[0], value[1])
            await pch.search_from_to()
            for j in pch.founded:
                print(j)
                await broadcaster(str(j))
                with open('found.txt', 'a') as f:
                    f.write(f"Found in subject {j[0]}: {j[1]}. On time {datetime.datetime.now()}\n")
            n_d = data[pch.subject_name]
            n_d[1] = pch.current_num
            data[pch.subject_name] = n_d
            del pch
            print('sub')
        with open(inp[0], 'w') as file:
            json.dump(data, file, ensure_ascii=False)
        print('cycle')
        if time.time() - s_t < 5:
            sleep_time += 1
        elif time.time() - s_t > 10:
            sleep_time -= 1
        print(sleep_time)
        await asyncio.sleep(sleep_time)


if __name__ == "__main__":
    inp = sys.argv[1:]
    if len(inp) != 1:
        with open('log.txt', 'a') as f:
            f.write(f"Wrong command. On time {datetime.datetime.now()}\n")
        exit('Usage: python Search.py nameoffile.json quantity_of_threads')
    try:
        with open(inp[0], 'r', errors='ignore', encoding="windows-1251") as file:
            data = json.load(file)
            for key, value in data.items():
                data[key] = [value[0], value[1]]

    except FileNotFoundError:
        with open('log.txt' 'a') as f:
            f.write(f"No data file. On time {datetime.datetime.now()}\n")
        exit("Add data.json file")
    try:
        with open('users.json', 'r', errors='ignore') as file:
            data_bot = dict(json.load(file))
            print(data_bot)
            users = data_bot.get('users')
            admins = data_bot.get('admins')
            nicknames = dict(data_bot.get('nicknames'))
            ban = data_bot.get('ban')

    except FileNotFoundError:
        exit("Add users.json file")


    async def run_all():
        await asyncio.gather(search(), main())


    asyncio.run(run_all())
