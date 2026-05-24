from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # LOCATORS
    ADD_TO_BAG = (By.XPATH, "//span[contains(text(),'Add to Bag')]")

    BAG_ICON = (By.XPATH, "//button[contains(.,'Bag') or contains(@class,'bag')]")

    PROCEED_BTN = (
        By.XPATH,
        "//button[contains(.,'Proceed') or contains(.,'Checkout') or contains(.,'Buy') or contains(.,'Continue')]"
    )

    CLOSE_POPUP = (By.XPATH, "//button[contains(@class,'close') or contains(text(),'Close')]")

    # =====================
    # ACTION METHODS
    # =====================

    def add_to_bag(self):
        try:
            btn = self.wait.until(
                EC.element_to_be_clickable(self.ADD_TO_BAG)
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            self.driver.execute_script("arguments[0].click();", btn)

            print("Added to bag")

        except Exception as e:
            raise Exception(f"Add to bag failed: {str(e)}")

    def open_cart(self):
        try:
            bag = self.wait.until(
                EC.presence_of_element_located(self.BAG_ICON)
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", bag)

            # avoid stale + intercept issues
            self.driver.execute_script("arguments[0].click();", bag)

            print("Cart opened")

        except Exception as e:
            raise Exception(f"Cart open failed: {str(e)}")

    def close_popup_if_present(self):
        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CLOSE_POPUP)
            )
            close_btn.click()
        except TimeoutException:
            pass  # popup not present

    def proceed(self):
        try:
            btn = self.wait.until(
                EC.element_to_be_clickable(self.PROCEED_BTN)
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            self.driver.execute_script("arguments[0].click();", btn)

            print("Proceeded to checkout")

        except TimeoutException:
            raise Exception("Proceed button not found")