import asyncio
import json
import asyncio
import aiofiles
import os

import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()

settings = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": ""
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "isHeaderFooterEnabled": False,
    "isCssBackgroundEnabled": True
}

chrome_options.add_argument('--enable-print-browser')
# chrome_options.add_argument('--headless')

prefs = {
    'printing.print_preview_sticky_settings.appState': json.dumps(settings),
    'savefile.default_directory': r'C:\Users\batsi\PycharmProjects\Ege_Cheater'
}
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_experimental_option('prefs', prefs)


class PdfLeaker:
    def __init__(self, url):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.url = url
        self.login = "he@gmail.com"
        self.password = "123"

    async def log_in(self):
        self.driver.get("https://ege.sdamgia.ru")
        await asyncio.sleep(3)
        while True:
            try:
                email_field = self.driver.find_element(By.ID, "email")
                email_field.send_keys(self.login)
                password_field = self.driver.find_element(By.ID, "current-password")
                password_field.send_keys(self.password)
                await asyncio.sleep(0.4)
                password_field.submit()
                await asyncio.sleep(0.4)
                break
            except selenium.common.exceptions.NoSuchElementException:
                await asyncio.sleep(2)

    async def leak(self):
        self.driver.get(f"{self.url}&print=true")
        await asyncio.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "input#cb_ans").click()
        self.driver.find_element(By.CSS_SELECTOR, "input#cb_sol").click()
        self.driver.execute_script('window.print();')
        self.driver.close()

    async def do_file(self):
        async with aiofiles.open(self.url, 'rb') as old_file:
            async with aiofiles.open('math_74921366.pdf', 'wb') as new_file:
                contents = await old_file.read()
                await new_file.write(contents)
        os.remove(self.url)

    async def run(self):
        await self.log_in()
        await self.leak()
        print(self.url)
        print(r'math-ege.sdamgia.ru_test_id=74921366&print=true.pdf')
        s = r'math-ege.sdamgia.ru_test_id=74921366&print=true.pdf'
        await self.do_file()
        print('Requests completed')


async def main():
    solver = PdfLeaker('https://math-ege.sdamgia.ru/test?id=74921366')
    await solver.run()


if __name__ == "__main__":
    asyncio.run(main())
