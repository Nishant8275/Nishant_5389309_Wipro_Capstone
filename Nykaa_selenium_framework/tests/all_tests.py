import time
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.hair_page import HairPage
from pages.cart_page import CartPage
from pages.payment_page import PaymentPage

from utils.logger import Logger
from config.config import Config
from utils.csv_reader import CSVReader


@allure.feature("Nykaa E-Commerce Flow")
class TestNykaaScenarios:

    # =========================================
    # POSITIVE TEST CASE 1
    # Search + Add Product To Cart
    # =========================================

    @allure.story("Add Product To Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_product_to_cart(self, driver):

        log = Logger.get_logger()

        with allure.step("Open Nykaa website"):
            driver.get(Config.BASE_URL)

        home = HomePage(driver)
        hair = HairPage(driver)
        cart = CartPage(driver)

        with allure.step("Search shampoo product"):
            log.info("Searching shampoo")
            home.search_product("shampoo")
            time.sleep(3)

        with allure.step("Open first product"):
            hair.select_first_product()
            log.info("Product page opened")
            time.sleep(3)

        with allure.step("Add product to cart"):
            cart.add_to_bag()
            log.info("Product added to cart")
            time.sleep(3)

        with allure.step("Verify product added successfully"):
            cart_items = driver.find_elements(
                By.XPATH,
                "//span[contains(@class,'count')]"
            )

            assert len(cart_items) > 0, "Product not added to cart"

            log.info("Assertion passed - product added")

    # =========================================
    # POSITIVE TEST CASE 2
    # Open Cart Successfully
    # =========================================

    @allure.story("Open Cart")
    @allure.severity(allure.severity_level.NORMAL)
    def test_open_cart(self, driver):

        log = Logger.get_logger()

        with allure.step("Open Nykaa website"):
            driver.get(Config.BASE_URL)

        home = HomePage(driver)
        hair = HairPage(driver)
        cart = CartPage(driver)

        with allure.step("Search conditioner"):
            home.search_product("conditioner")
            time.sleep(3)

        with allure.step("Select first product"):
            hair.select_first_product()
            time.sleep(3)

        with allure.step("Add product to cart"):
            cart.add_to_bag()
            time.sleep(3)

        with allure.step("Open cart"):
            cart.open_cart()
            log.info("Cart opened")
            time.sleep(5)

        with allure.step("Verify cart page opened"):
            cart_ui = driver.find_elements(
                By.XPATH,
                "//*[contains(text(),'Bag') or contains(text(),'Cart')]"
            )

            assert len(cart_ui) > 0, "Cart UI did not open"

    # =========================================
    # POSITIVE TEST CASE 3
    # Guest Checkout
    # =========================================

    @allure.story("Guest Checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_guest_checkout(self, driver):

        log = Logger.get_logger()

        with allure.step("Open website"):
            driver.get(Config.BASE_URL)

        home = HomePage(driver)
        hair = HairPage(driver)
        cart = CartPage(driver)
        payment = PaymentPage(driver)

        with allure.step("Search hair oil"):
            home.search_product("hair oil")
            time.sleep(3)

        with allure.step("Select first product"):
            hair.select_first_product()
            time.sleep(3)

        with allure.step("Add product to bag"):
            cart.add_to_bag()
            time.sleep(3)

        with allure.step("Open cart"):
            cart.open_cart()
            time.sleep(3)

        with allure.step("Proceed to checkout"):
            cart.proceed()
            time.sleep(5)

        with allure.step("Handle guest popup"):
            payment.handle_login_or_guest()
            time.sleep(5)

        with allure.step("Verify checkout page opened"):
            assert (
                    "checkout" in driver.current_url.lower()
                    or
                    "address" in driver.current_url.lower()
            ), "Checkout page did not open"

    # =========================================
    # POSITIVE TEST CASE 4
    # Fill Address Form
    # =========================================

    @allure.story("Fill Address Form")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_fill_address_form(self, driver):

        log = Logger.get_logger()

        with allure.step("Open Nykaa website"):
            driver.get(Config.BASE_URL)

        home = HomePage(driver)
        hair = HairPage(driver)
        cart = CartPage(driver)
        payment = PaymentPage(driver)

        with allure.step("Search shampoo"):
            home.search_product("shampoo")

        with allure.step("Open first product"):
            hair.select_first_product()

        with allure.step("Add product to cart"):
            cart.add_to_bag()

        with allure.step("Open cart"):
            cart.open_cart()

        with allure.step("Proceed to checkout"):
            cart.proceed()

        with allure.step("Handle guest checkout"):
            payment.handle_login_or_guest()

        with allure.step("Wait for address page"):
            WebDriverWait(driver, 40).until(
                lambda d:
                "address" in d.current_url.lower()
                or
                "checkout" in d.current_url.lower()
            )

        with allure.step("Fill address form"):
            payment.fill_address(
                name="Test User",
                phone="9999999999",
                email="testuser@gmail.com",
                house="221B",
                area="Delhi",
                pincode="110001"
            )

        with allure.step("Verify Ship To This Address button visible"):
            ship_button = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//button[@data-testid='button_shipToThisAddress']"
                    )
                )
            )

            assert ship_button.is_displayed(), \
                "Address page not loaded properly"

    # =========================================
    # NEGATIVE TEST CASE 1
    # Invalid Pincode
    # =========================================

    @allure.story("Invalid Pincode Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_pincode(self, driver):

        with allure.step("Open website"):
            driver.get(Config.BASE_URL)

        home = HomePage(driver)
        hair = HairPage(driver)
        cart = CartPage(driver)
        payment = PaymentPage(driver)

        with allure.step("Search shampoo"):
            home.search_product("shampoo")
            time.sleep(3)

        with allure.step("Select first product"):
            hair.select_first_product()

        with allure.step("Add product to bag"):
            cart.add_to_bag()

        with allure.step("Open cart"):
            cart.open_cart()

        with allure.step("Proceed checkout"):
            cart.proceed()

        with allure.step("Handle guest popup"):
            payment.handle_login_or_guest()

        with allure.step("Wait for address page"):
            WebDriverWait(driver, 40).until(
                lambda d:
                "address" in d.current_url.lower()
            )

        with allure.step("Enter invalid pincode"):
            payment.fill_address(
                "Test User",
                "9999999999",
                "testuser@gmail.com",
                "221B",
                "Delhi",
                "000000"
            )

        with allure.step("Verify user remains on address page"):
            assert "address" in driver.current_url.lower()

    # =========================================
    # NEGATIVE TEST CASE 2
    # Empty Address Fields
    # =========================================

    @allure.story("Empty Address Validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_address_fields(self, driver):
        with allure.step("Open website"):
            driver.get(Config.BASE_URL)

        home = HomePage(driver)
        hair = HairPage(driver)
        cart = CartPage(driver)
        payment = PaymentPage(driver)

        with allure.step("Search shampoo"):
            home.search_product("shampoo")

        with allure.step("Select product"):
            hair.select_first_product()

        with allure.step("Add product to bag"):
            cart.add_to_bag()

        with allure.step("Open cart"):
            cart.open_cart()

        with allure.step("Proceed to checkout"):
            cart.proceed()

        with allure.step("Handle guest popup"):
            payment.handle_login_or_guest()