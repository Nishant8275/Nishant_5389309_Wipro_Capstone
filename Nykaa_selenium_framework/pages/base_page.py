from selenium.webdriver.support.ui import WebDriverWait
from config.config import Config


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)