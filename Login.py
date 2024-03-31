import time
import json
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
#chrome_options.add_argument('--headless')

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

    def log_in(self):
        self.driver.get("https://ege.sdamgia.ru")
        time.sleep(5)
        email_field = self.driver.find_element(By.ID, "email")
        email_field.send_keys(self.login)
        password_field = self.driver.find_element(By.ID, "current-password")
        password_field.send_keys(self.password)
        password_field.submit()
        time.sleep(0.4)

    def leak(self):
        # self.driver.get(self.url)
        # time.sleep(0.4)
        #
        # link = self.driver.find_element(By.LINK_TEXT, 'Версия для печати и копирования в MS Word')
        #
        # link.click()
        # time.sleep(1)
        self.driver.get(f"{self.url}&print=true")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "input#cb_ans").click()
        self.driver.find_element(By.CSS_SELECTOR, "input#cb_sol").click()
        self.driver.execute_script('window.print();')
        self.driver.close()

    def run(self):
        self.log_in()
        self.leak()
        print('Requests completed')


if __name__ == "__main__":
    solver = PdfLeaker('https://math-ege.sdamgia.ru/test?id=74921366')
    solver.run()
