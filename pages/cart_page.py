
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # LOCATORS
    ADD_TO_BAG = (By.XPATH, "//span[contains(text(),'Add to Bag')]")
    BAG_ICON = (By.XPATH, "//button[contains(.,'Bag')]")
    PROCEED_BTN = (
        By.XPATH,
        "//button[contains(.,'Proceed') or contains(.,'Checkout') or contains(.,'Buy') or contains(.,'Continue')]"
    )

    # ACTIONS
    def add_to_bag(self):
        self.wait.until(
            EC.element_to_be_clickable(self.ADD_TO_BAG)
        ).click()
        print("Added to bag")

    def open_cart(self):
        bag = self.wait.until(
            EC.element_to_be_clickable(self.BAG_ICON)
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", bag)

        try:
            bag.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", bag)

        print("Cart opened")

    def proceed(self):

        try:
            # wait for button (no iframe guessing unless needed)
            btn = self.wait.until(
                EC.element_to_be_clickable(self.PROCEED_BTN)
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)

            try:
                btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)

            print("Proceeded to checkout")

        except TimeoutException:
            print("Proceed button not found")