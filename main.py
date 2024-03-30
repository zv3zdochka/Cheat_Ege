import time
import yaml
from yaml.loader import SafeLoader
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class ReshuEgeSolver:
    settings = dict()

    def __init__(self):
        with open("settings.yml", 'r') as stream:
            self.settings = yaml.load(stream, SafeLoader)

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Включаем Headless режим
        self.driver = webdriver.Chrome(options=chrome_options)  # Используем Chrome

        self.exam_url = 'https://math-ege.sdamgia.ru/test?id=74921366'

    def __log_in(self):
        self.driver.get("https://ege.sdamgia.ru")

        email_field = self.driver.find_element(By.ID, "email")
        email_field.send_keys(self.settings['PROFILE']['EMAIL'])
        password_field = self.driver.find_element(By.ID, "current-password")
        password_field.send_keys(self.settings['PROFILE']['PASSWORD'])
        password_field.submit()
        time.sleep(0.4)

    def __solve_test(self):
        self.driver.get(self.exam_url)

        # Ждем некоторое время, чтобы страница полностью загрузилась
        time.sleep(5)

        # Получаем HTML-код страницы
        html = self.driver.page_source

        # Сохраняем HTML в файл
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(html)

    def run(self):
        self.__log_in()
        self.__solve_test()

if __name__ == "__main__":
    solver = ReshuEgeSolver()
    solver.run()
