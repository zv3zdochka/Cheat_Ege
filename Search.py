try:
    import time
    import sys
    import os
    from bs4 import BeautifulSoup
    from concurrent.futures import ThreadPoolExecutor
    import concurrent
    import requests
    from requests.auth import HTTPProxyAuth
    import json
    from sdamgia import SdamGIA
    import datetime
except ModuleNotFoundError:
    with open('log.txt', 'a') as f:
        f.write(f"Required libraries are missing.\n")
    sys.exit("Required libraries are missing. Please install them using:\n"
             "pip install -r requirements.txt\n"
             "You can find the requirements.txt file at: https://github.com/zv3zdochka/LAW.git")


class PageChecker:
    def __init__(self, subject_name, targets, start, threads_number=3):
        self.workers = threads_number
        self.start_id = start
        self.subject_name = subject_name
        self.targets = targets
        self.current_num = 0
        self.subject_url = self.subject_url_by_name(subject_name)
        self.founded = []

    def check_page(self, page_id):
        if page_id is None:
            return
        url = f"{self.subject_url}/test?id={page_id}"
        print(url)

        try:
            with requests.Session() as session:
                #response = session.get(url, proxies=proxyDict, auth=auth)
                response = session.get(url)
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
            with open('log.txt' 'a') as f:
                f.write(f"Exception processing page {page_id}. On time {datetime.datetime.now()}\n")
            return f"Error processing page {page_id}: {e}"

    def get_current_test_num(self):
        try:
            sdamgia = SdamGIA()
            self.current_num = int(sdamgia.generate_test(self.subject_name, {1: 1}))
            del sdamgia
        except KeyError:
            with open('log.txt' 'a') as f:
                f.write(f"Vpn or proxy error. On time {datetime.datetime.now()}\n")
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
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            ids = generator()
            futures = {executor.submit(self.check_page, next(ids)): id for id in range(50)}
            while futures:

                done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

                for future in done:
                    page_id = futures.pop(future)

                    try:
                        result = future.result()
                        if result:
                            self.founded.append([self.subject_name, result])

                    except Exception as exc:
                        with open('log.txt', 'a') as f:
                            f.write(f"Exception processing page {page_id}: {exc}. On time {datetime.datetime.now()}\n")

                    new_id = next(ids)
                    if new_id is None:
                        break
                    futures[executor.submit(self.check_page, new_id)] = new_id
            executor.shutdown(wait=True)

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


def do():
    # TODO: Delete thsi shit and add normal bot 
    # connect to tg bot
    pass


if __name__ == "__main__":
    inp = sys.argv[1:]
    if len(inp) != 2:
        with open('log.txt', 'a') as f:
            f.write(f"Wrong command. On time {datetime.datetime.now()}\n")
        exit('Usage: python Search.py nameoffile.json quantity_of_threads')
    threads = int(inp[1])
    if not (1 <= threads <= 16):
        with open('log.txt', 'a') as f:
            f.write(f"Invalid number of threads. On time {datetime.datetime.now()}\n")
        exit("Invalid number of threads. Please choose a value between 1 and 16. Recommended number of threads is 2~3.")
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
    sleep_time = 10
    while True:
        s_t = time.time()
        print(data)
        for key, value in data.items():
            pch = PageChecker(key, value[0], value[1], threads)
            pch.search_from_to()
            for j in pch.founded:
                with open('found.txt', 'a') as f:
                    do()
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
        elif time.time() - s_t > 15:
            sleep_time -= 1
        print(sleep_time)
        time.sleep(sleep_time)
