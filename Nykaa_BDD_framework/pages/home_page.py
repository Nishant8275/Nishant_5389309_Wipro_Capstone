from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)   # ✅ FIX ADDED


    def search_product(self, product):

        search_box = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Search on Nykaa']")
            )
        )

        search_box.clear()
        search_box.send_keys(product)
        search_box.submit()