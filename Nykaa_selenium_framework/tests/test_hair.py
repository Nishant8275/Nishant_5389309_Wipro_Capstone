from selenium.webdriver.common.by import By


class HairPage:

    def __init__(self, driver):
        self.driver = driver

    PRODUCTS = (By.XPATH, "//div[contains(@class,'productWrapper')]")

    def select_first_product(self):

        products = self.driver.find_elements(*self.PRODUCTS)

        assert len(products) > 0, "No products found"

        products[0].click()

        self.driver.switch_to.window(self.driver.window_handles[-1])

        print("Product selected successfully")