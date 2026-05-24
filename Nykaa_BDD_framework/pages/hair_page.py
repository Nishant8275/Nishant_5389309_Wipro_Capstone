from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class HairPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def select_first_product(self):

        # Wait for products
        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//a[contains(@href,'/p/')]")
            )
        )

        products = self.driver.find_elements(
            By.XPATH,
            "//a[contains(@href,'/p/')]"
        )

        print("PRODUCT COUNT:", len(products))

        assert len(products) > 0, "No products found"

        first_product = products[0]

        product_url = first_product.get_attribute("href")

        print("CLICKING PRODUCT:", product_url)

        # Open product directly
        self.driver.get(product_url)

        # Wait for product page
        self.wait.until(
            lambda d:
            "/p/" in d.current_url
            or
            "product" in d.current_url.lower()
        )

        print("Product page opened successfully")