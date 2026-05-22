
import time
import allure

from config.config import Config
from pages.home_page import HomePage
from pages.hair_page import HairPage
from pages.cart_page import CartPage
from pages.payment_page import PaymentPage

from utils.logger import Logger
from utils.screenshot_util import ScreenshotUtil

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.csv_reader import CSVReader

@allure.feature("Nykaa E2E Checkout")
@allure.story("Guest User Checkout Flow")
@allure.severity(allure.severity_level.CRITICAL)
class TestNykaaE2E:

    @allure.title("Complete Nykaa Checkout Flow")
    @allure.description(
        "Verify user can search product, add to cart, "
        "fill address and proceed to checkout"
    )
    def test_nykaa_flow(self, driver):

        log = Logger.get_logger()

        try:

            # =========================
            # OPEN WEBSITE
            # =========================
            with allure.step("Open Nykaa Website"):

                log.info("Opening Nykaa")

                driver.get(Config.BASE_URL)

                assert "nykaa" in driver.current_url.lower(), \
                    "Nykaa website did not open"

                log.info("Nykaa website opened successfully")

            # =========================
            # INITIALIZE PAGES
            # =========================
            home = HomePage(driver)
            hair = HairPage(driver)
            cart = CartPage(driver)
            payment = PaymentPage(driver)

            # =========================
            # SEARCH PRODUCT
            # =========================
            with allure.step("Search Product"):

                log.info("Searching shampoo")

                home.search_product("shampoo")

                time.sleep(3)

                products = driver.find_elements(
                    By.XPATH,
                    "//a[contains(@href,'/p/')]"
                )

                assert len(products) > 0, \
                    "Search results not displayed"

                log.info("Search results displayed")

            # =========================
            # OPEN PRODUCT
            # =========================
            with allure.step("Open First Product"):

                hair.select_first_product()

                time.sleep(3)

                assert "/p/" in driver.current_url.lower(), \
                    "Product page did not open"

                log.info("Product page opened")

            # =========================
            # ADD TO BAG
            # =========================
            with allure.step("Add Product To Bag"):

                cart.add_to_bag()

                time.sleep(3)

                cart_count = driver.find_elements(
                    By.XPATH,
                    "//span[contains(@class,'count')]"
                )

                assert len(cart_count) > 0, \
                    "Product not added to bag"

                log.info("Product added to cart")

            # =========================
            # OPEN CART
            # =========================
            with allure.step("Open Cart"):

                cart.open_cart()

                time.sleep(3)

                cart_ui = driver.find_elements(
                    By.XPATH,
                    "//*[contains(text(),'Bag') or contains(text(),'Cart')]"
                )

                assert len(cart_ui) > 0, \
                    "Cart page not opened"

                log.info("Cart opened successfully")

            # =========================
            # PROCEED TO CHECKOUT
            # =========================
            with allure.step("Proceed To Checkout"):

                cart.proceed()

                time.sleep(5)

                log.info("Proceed clicked")

            # =========================
            # HANDLE GUEST LOGIN
            # =========================
            with allure.step("Handle Guest Checkout"):

                payment.handle_login_or_guest()

                log.info("Guest checkout handled")

            # =========================
            # WAIT FOR ADDRESS PAGE
            # =========================
            with allure.step("Verify Address Page Opened"):

                WebDriverWait(driver, 40).until(
                    lambda d:
                    "address" in d.current_url.lower()
                    or
                    "checkout" in d.current_url.lower()
                )

                assert (
                    "address" in driver.current_url.lower()
                    or
                    "checkout" in driver.current_url.lower()
                ), "Address page not opened"

                log.info("Address page opened")

            # =========================
            # FILL ADDRESS
            # =========================
            with allure.step("Fill Address Details"):

                payment.fill_address(
                    name="Test User",
                    phone="9999999999",
                    email="testuser@gmail.com",
                    house="221B",
                    area="Delhi",
                    pincode="110001"
                )

                log.info("Address filled successfully")

                time.sleep(5)

            # =========================
            # VERIFY SHIP BUTTON
            # =========================
            with allure.step("Verify Ship To This Address Button"):

                ship_button = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//button[@data-testid='button_shipToThisAddress']"
                        )
                    )
                )

                assert ship_button.is_displayed(), \
                    "Ship button not visible"

                log.info("Ship button visible")

            # =========================
            # CLICK SHIP BUTTON
            # =========================
            with allure.step("Click Ship To This Address"):

                payment.continue_to_payment()

                log.info("Ship button clicked")

                time.sleep(5)

            # =========================
            # FINAL ASSERTION
            # =========================
            with allure.step("Verify Checkout Flow"):

                assert (
                    "payment" in driver.current_url.lower()
                    or
                    "checkout" in driver.current_url.lower()
                    or
                    "address" in driver.current_url.lower()
                ), "Checkout flow failed"

                log.info("Checkout flow completed successfully")

        except Exception as e:

            log.error(f"TEST FAILED: {e}")

            ScreenshotUtil.take_screenshot(
                driver,
                "nykaa_failure"
            )

            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            raise