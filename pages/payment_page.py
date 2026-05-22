import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import Logger


class PaymentPage:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.log = Logger.get_logger()

    # =========================
    # CONTACT SECTION
    # =========================
    NAME = (By.XPATH, "//input[@placeholder='Name']")

    PHONE = (By.XPATH, "//input[@placeholder='Phone']")

    EMAIL = (By.XPATH, "//input[@placeholder='Email']")

    # =========================
    # ADDRESS SECTION
    # =========================
    HOUSE = (
        By.XPATH,
        "//input[@placeholder='House/ Flat/ Office No.']"
    )

    AREA = (
        By.XPATH,
        "//textarea[@placeholder='Road Name/ Area /Colony']"
    )

    PINCODE = (
        By.XPATH,
        "//input[@placeholder='Pincode']"
    )

    # =========================
    # BUTTONS
    # =========================
    SHIP_BUTTON = (
        By.XPATH,
        "//button[@data-testid='button_shipToThisAddress']"
    )

    GUEST_BUTTON = (
        By.XPATH,
        "//button[contains(.,'Guest') or contains(.,'guest')]"
    )

    # =========================
    # HANDLE GUEST LOGIN
    # =========================
    def handle_login_or_guest(self):

        try:

            guest = self.wait.until(
                EC.element_to_be_clickable(self.GUEST_BUTTON)
            )

            guest.click()

            self.log.info("Guest button clicked")

        except Exception as e:

            self.log.info("No login/guest popup")

    # =========================
    # FILL ADDRESS
    # =========================
    def fill_address(
            self,
            name,
            phone,
            email,
            house,
            area,
            pincode
    ):

        try:

            # WAIT FOR ADDRESS PAGE
            self.wait.until(
                lambda d: "address" in d.current_url.lower()
            )

            self.log.info("Address page opened")

            # =========================
            # NAME
            # =========================
            name_field = self.wait.until(
                EC.visibility_of_element_located(self.NAME)
            )

            name_field.clear()
            name_field.send_keys(name)

            self.log.info(f"Entered Name: {name}")

            # =========================
            # PHONE
            # =========================
            phone_field = self.wait.until(
                EC.visibility_of_element_located(self.PHONE)
            )

            phone_field.clear()
            phone_field.send_keys(phone)

            self.log.info(f"Entered Phone: {phone}")

            # =========================
            # EMAIL
            # =========================
            email_field = self.wait.until(
                EC.visibility_of_element_located(self.EMAIL)
            )

            email_field.clear()
            email_field.send_keys(email)

            self.log.info(f"Entered Email: {email}")

            # =========================
            # HOUSE / FLAT
            # =========================
            house_field = self.wait.until(
                EC.visibility_of_element_located(self.HOUSE)
            )

            house_field.clear()
            house_field.send_keys(house)

            self.log.info(f"Entered House: {house}")

            # =========================
            # AREA
            # =========================
            area_field = self.wait.until(
                EC.visibility_of_element_located(self.AREA)
            )

            area_field.clear()
            area_field.send_keys(area)

            self.log.info(f"Entered Area: {area}")

            # =========================
            # PINCODE
            # =========================
            # PINCODE
            pin_field = self.wait.until(
                EC.visibility_of_element_located(self.PINCODE)
            )

            pin_field.clear()
            pin_field.send_keys(pincode)

            self.log.info(f"Entered Pincode: {pincode}")

            # WAIT FOR ADDRESS VALIDATION
            time.sleep(3)

            self.log.info("Address filled successfully")

        except Exception as e:

            self.log.error(f"Address filling failed: {e}")

            raise

    # =========================
    # CONTINUE TO PAYMENT
    # =========================
    def continue_to_payment(self):

        try:
            ship_btn = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(self.SHIP_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                ship_btn
            )

            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(self.SHIP_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].click();",
                ship_btn
            )

            self.log.info("Ship button clicked successfully")

        except Exception as e:
            self.log.error(f"Ship button failed: {e}")
            raise