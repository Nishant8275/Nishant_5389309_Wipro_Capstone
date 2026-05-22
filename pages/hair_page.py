from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class HairPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    PRODUCTS = (By.XPATH, "//div[contains(@class,'productWrapper')]")

    def select_first_product(self):
        products = self.driver.find_elements(
            By.XPATH,
            "(//div[contains(@class,'productWrapper')])[1]"
        )

        assert len(products) > 0, "No products found"

        products[0].click()

        # WAIT FOR NEW TAB
        self.wait.until(EC.number_of_windows_to_be(2))

        # switch tab
        self.driver.switch_to.window(self.driver.window_handles[-1])

        print("Product page opened")