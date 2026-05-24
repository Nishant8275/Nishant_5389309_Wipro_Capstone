from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    def __init__(self, context):
        self.driver = context.driver
        self.wait = WebDriverWait(self.driver, 15)

    # =====================
    # LOCATORS
    # =====================

    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Sign in')]")
    MOBILE_FIELD = (By.NAME, "emailMobile")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Proceed')]")

    # =====================
    # ACTIONS
    # =====================

    def open_login(self):
        btn = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )

        self.driver.execute_script("arguments[0].click();", btn)
        print("Login popup opened")

    def enter_mobile(self, mobile):

        field = self.wait.until(
            EC.visibility_of_element_located(self.MOBILE_FIELD)
        )

        field.clear()
        field.send_keys(mobile)

        print(f"Entered mobile: {mobile}")

    def submit(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(self.SUBMIT_BUTTON)
        )

        self.driver.execute_script("arguments[0].click();", btn)

        print("Login submitted")