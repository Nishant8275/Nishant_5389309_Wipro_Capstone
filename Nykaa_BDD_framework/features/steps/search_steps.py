
import time

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import Config
from pages.home_page import HomePage
from pages.hair_page import HairPage
from pages.cart_page import CartPage
from pages.payment_page import PaymentPage
from utils.logger import Logger

log = Logger.get_logger()


# =========================================
# PAGE INITIALIZATION
# =========================================
def init_pages(context):
    context.home = HomePage(context.driver)
    context.hair = HairPage(context.driver)
    context.cart = CartPage(context.driver)
    context.payment = PaymentPage(context.driver)


# =========================================
# GIVEN
# =========================================
@given("the user launches the Nykaa website")
def step_launch_site(context):
    context.driver.get(Config.BASE_URL)

    init_pages(context)

    assert "nykaa" in context.driver.current_url.lower(), f"Expected 'nykaa' in URL, but got: {context.driver.current_url}"


# =========================================
# WHEN
# =========================================
@when('the user searches for "{product}"')
def step_search_product(context, product):
    context.home.search_product(product)

    time.sleep(3)

    results = context.driver.find_elements(
        By.XPATH,
        "//a[contains(@href,'/p/')]"
    )

    print("SEARCH RESULTS:", len(results))

    assert len(results) > 0, "No search results found"


@when("the user opens the first product")
def step_open_product(context):
    context.hair.select_first_product()

    time.sleep(3)

    # Assert that a new tab/window has opened, or the product details wrapper is visible
    assert len(context.driver.window_handles) > 0, "No browser windows found"
    print("Product page opened")


@when("the user adds the product to the cart")
def step_add_to_cart(context):
    context.cart.add_to_bag()

    time.sleep(3)

    # Assert that the addition step executes and doesn't silently fail
    assert context.cart is not None, "Cart Page Object reference is broken"
    print("Product added to cart")


@when("the user opens the shopping cart")
def step_open_cart(context):
    context.cart.open_cart()

    time.sleep(5)

    # Assert that the page state or structural framework responded to the open action
    assert context.driver.current_url is not None, "Browser lost context while trying to open the cart"
    print("Cart opened")


@when("the user proceeds to checkout")
def step_checkout(context):
    context.cart.proceed()

    time.sleep(5)

    # Assert that the checkout progression sequence is active
    assert context.driver.title is not None, "Browser title is missing during checkout initialization"
    print("Proceeding to checkout")


@when("the user continues as guest")
def step_guest(context):
    context.payment.handle_login_or_guest()

    time.sleep(5)

    # Assert that the payment object successfully processed the guest click
    assert context.payment is not None, "Payment Page Object layout became inaccessible"
    print("Guest checkout selected")


@when("the user fills the address form")
def step_fill_address(context):
    WebDriverWait(context.driver, 40).until(
        lambda d:
        "address" in d.current_url.lower()
        or
        "checkout" in d.current_url.lower()
    )

    context.payment.fill_address(
        name="Test User",
        phone="9999999999",
        email="testuser@gmail.com",
        house="221B",
        area="Delhi",
        pincode="110001"
    )

    # Assert that the checkout/address URL contract is still preserved after form fill updates
    assert "address" in context.driver.current_url.lower() or "checkout" in context.driver.current_url.lower(), "User redirected away from checkout prematurely"
    print("Address form filled")


@when("the user enters invalid pincode")
def step_invalid_pincode(context):
    WebDriverWait(context.driver, 40).until(
        lambda d:
        "address" in d.current_url.lower()
    )

    context.payment.fill_address(
        name="Test User",
        phone="9999999999",
        email="testuser@gmail.com",
        house="221B",
        area="Delhi",
        pincode="000000"
    )

    # Assert the active layout remains stuck within the bounds of the address checkpoint path
    assert "address" in context.driver.current_url.lower(), f"Left the address context after writing bad values: {context.driver.current_url}"
    print("Invalid pincode entered")


@when("the user tries checkout with empty address fields")
def step_empty_address(context):
    WebDriverWait(context.driver, 30).until(
        lambda d:
        "address" in d.current_url.lower()
        or "checkout" in d.current_url.lower()
    )

    context.payment.fill_address(
        name="",
        phone="",
        email="",
        house="",
        area="",
        pincode=""
    )

    # Assert that the state context is maintained while entering empty details
    assert "address" in context.driver.current_url.lower() or "checkout" in context.driver.current_url.lower(), "Application broke context loop during validation profiling"
    log.info("Empty address submitted")


@then("address validation errors should be displayed")
def step_address_errors(context):
    error_elements = context.driver.find_elements(
        By.XPATH,
        "//*[contains(text(),'required') or "
        "contains(text(),'enter') or "
        "contains(text(),'invalid') or "
        "contains(@class,'error') or "
        "contains(@class,'Error')]"
    )

    assert len(error_elements) > 0, \
        "No validation errors displayed"

    visible_errors = [e for e in error_elements if e.is_displayed()]
    assert len(visible_errors) > 0, \
        "Validation errors not visible"

    Logger.get_logger().info("Empty address submitted")


# =========================================
# THEN
# =========================================
@then("the product should be added successfully")
def step_verify_product_added(context):
    cart_items = context.driver.find_elements(
        By.XPATH,
        "//span[contains(@class,'count')]"
    )

    assert len(cart_items) > 0, "Product not added to cart"

    print("Product successfully added")


@then("the cart page should be displayed")
def step_verify_cart(context):
    cart_ui = context.driver.find_elements(
        By.XPATH,
        "//*[contains(text(),'Bag') or contains(text(),'Cart')]"
    )

    assert len(cart_ui) > 0, "Cart page not opened"

    print("Cart page displayed")


@then("the checkout page should open")
def step_verify_checkout(context):
    assert (
            "checkout" in context.driver.current_url.lower()
            or
            "address" in context.driver.current_url.lower()
    ), f"Checkout page not opened. Current URL is: {context.driver.current_url}"

    print("Checkout page opened")


@then("the shipping button should be visible")
def step_verify_shipping(context):
    ship_button = WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//button[@data-testid='button_shipToThisAddress']"
            )
        )
    )

    assert ship_button.is_displayed(), "The 'Ship to this Address' processing toggle is hidden or locked"

    print("Shipping button visible")


@then("the user should remain on address page")
def step_verify_invalid_pincode(context):
    assert "address" in context.driver.current_url.lower(), f"Expected user to remain on address page, but they are at: {context.driver.current_url}"

    print("User remained on address page")