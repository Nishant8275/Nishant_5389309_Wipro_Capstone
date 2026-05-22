
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class HomePage:

    def __init__(self, driver):
        self.driver = driver

    # Locator
    search_box = (
        By.NAME,
        "search-suggestions-nykaa"
    )

    # Methods
    def open_website(self):

        self.driver.get("https://www.nykaa.com/")

        self.driver.maximize_window()

        time.sleep(5)

    def search_product(self, product_name):

        search = self.driver.find_element(*self.search_box)

        search.send_keys(product_name)

        search.send_keys(Keys.ENTER)

        time.sleep(5)