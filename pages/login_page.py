from selenium.webdriver.common.by import By
import time


class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    # Locators
    login_button = (By.XPATH, "//button[contains(text(),'Sign in')]")
    mobile_field = (By.NAME, "emailMobile")
    submit_button = (By.XPATH, "//button[contains(text(),'Proceed')]")

    def open_login(self):
        self.driver.find_element(*self.login_button).click()
        time.sleep(5)

    def enter_mobile(self, mobile):
        self.driver.find_element(*self.mobile_field).send_keys(mobile)
        time.sleep(5)

    def submit(self):
        self.driver.find_element(*self.submit_button).click()
        time.sleep(3)