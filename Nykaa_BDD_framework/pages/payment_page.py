from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import Logger


class PaymentPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

        # FIX: Initialize the logger so self.log exists
        self.log = Logger.get_logger()

    # =========================
    # LOCATORS
    # =========================

    NAME = (By.XPATH, "//input[@placeholder='Name']")
    PHONE = (By.XPATH, "//input[@placeholder='Phone']")
    EMAIL = (By.XPATH, "//input[@placeholder='Email']")

    HOUSE = (By.XPATH, "//input[@placeholder='House/ Flat/ Office No.']")
    AREA = (By.XPATH, "//textarea[@placeholder='Road Name/ Area /Colony']")
    PINCODE = (By.XPATH, "//input[@placeholder='Pincode']")

    SHIP_BUTTON = (By.XPATH, "//button[@data-testid='button_shipToThisAddress']")

    GUEST_BUTTON = (By.XPATH, "//button[contains(.,'Guest') or contains(.,'guest')]")

    # =========================
    # ACTIONS
    # =========================

    def handle_login_or_guest(self):
        try:
            guest = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GUEST_BUTTON)
            )
            guest.click()
            self.log.info("Guest button clicked")

        except Exception:
            self.log.info("No guest popup found")

    # =========================
    # FILL ADDRESS
    # =========================

    def fill_address(self, name, phone, email, house, area, pincode):
        try:

            # WAIT FOR PAGE
            WebDriverWait(self.driver, 30).until(
                lambda d: "address" in d.current_url.lower()
            )

            self.log.info("Address page opened")

            self._fill(self.NAME, name, "Name")
            self._fill(self.PHONE, phone, "Phone")
            self._fill(self.EMAIL, email, "Email")
            self._fill(self.HOUSE, house, "House")
            self._fill(self.AREA, area, "Area")
            self._fill(self.PINCODE, pincode, "Pincode")

            self.log.info("Address filled successfully")

        except Exception as e:
            self.log.error(f"Address filling failed: {e}")
            raise

    # =========================
    # REUSABLE METHOD (VERY IMPORTANT)
    # =========================

    def _fill(self, locator, value, field_name):
        if value is None:
            return

        field = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(locator)
        )

        field.clear()
        field.send_keys(value)

        self.log.info(f"Entered {field_name}: {value}")

    # =========================
    # CONTINUE TO PAYMENT
    # =========================

    def continue_to_payment(self):
        try:
            ship_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(self.SHIP_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                ship_btn
            )

            self.driver.execute_script("arguments[0].click();", ship_btn)

            self.log.info("Ship button clicked successfully")

        except Exception as e:
            self.log.error(f"Ship button failed: {e}")
            raise