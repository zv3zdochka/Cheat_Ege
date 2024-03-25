import asyncio
import json
import datetime
import aiohttp
from bs4 import BeautifulSoup
from sdamgia import SdamGIA
import time
import sys


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
        print(url)

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


async def main():
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
    asyncio.run(main())
