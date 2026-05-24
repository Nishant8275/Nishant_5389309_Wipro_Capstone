from selenium.webdriver.support.ui import WebDriverWait
from config.config import Config


class BasePage:

    def __init__(self, context):
        # In BDD, we use context instead of pytest driver fixture
        self.driver = context.driver
        self.wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT)