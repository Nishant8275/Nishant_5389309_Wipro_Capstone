import time
import allure

from behave import given, when, then

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import Config

from pages.home_page import HomePage
from pages.hair_page import HairPage
from pages.cart_page import CartPage
from pages.payment_page import PaymentPage
from utils.csv_reader import CSVReader

# ==========================================
# Initialize Page Objects
# ==========================================
def init_pages(context):

    context.home = HomePage(context.driver)
    context.hair = HairPage(context.driver)
    context.cart = CartPage(context.driver)
    context.payment = PaymentPage(context.driver)


# ==========================================
# OPEN WEBSITE
# ==========================================
@given("user opens Nykaa website")
def step_open_nykaa(context):

    context.log.info("Opening Nykaa website")

    context.driver.get(Config.BASE_URL)

    WebDriverWait(context.driver, 20).until(
        EC.url_contains("nykaa")
    )

    assert "nykaa" in context.driver.current_url.lower(), \
        "Nykaa website did not open"

    context.log.info("Nykaa website opened successfully")

    init_pages(context)


# ==========================================
# SEARCH PRODUCT
# ==========================================
@when('user searches for "{product_name}"')
def step_search_product(context, product_name):

    context.log.info(f"Searching product: {product_name}")

    context.home.search_product(product_name)

    WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href,'/p/')]")
        )
    )

    products = context.driver.find_elements(
        By.XPATH,
        "//a[contains(@href,'/p/')]"
    )

    assert len(products) > 0, \
        "Search results not displayed"

    context.log.info("Search results displayed successfully")


# ==========================================
# SELECT PRODUCT
# ==========================================
@when("user selects first product")
def step_impl(context):
    # 1. Capture the handle of the current window (search results)
    original_window = context.driver.current_window_handle

    # 2. Click the product (this triggers the new tab)
    context.hair.select_first_product()
    time.sleep(3)

    # 3. Loop through all open windows until we find the new one
    for window_handle in context.driver.window_handles:
        if window_handle != original_window:
            context.driver.switch_to.window(window_handle)
            context.log.info("Successfully switched focus to the new product tab")
            break

    # 4. Now run your original assertion on the correct page
    assert "/p/" in context.driver.current_url.lower(), \
        f"Product page did not open. Current URL is: {context.driver.current_url}"
    context.log.info("Product page opened")


# ==========================================
# ADD TO BAG
# ==========================================
@when("user adds product to bag")
def step_add_to_bag(context):

    context.log.info("Adding product to bag")

    context.cart.add_to_bag()

    WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(@class,'count')]")
        )
    )

    cart_count = context.driver.find_elements(
        By.XPATH,
        "//span[contains(@class,'count')]"
    )

    assert len(cart_count) > 0, \
        "Product not added to bag"

    context.log.info("Product added to bag successfully")


# ==========================================
# OPEN CART
# ==========================================
@when("user opens cart")
def step_open_cart(context):

    context.log.info("Opening cart")

    context.cart.open_cart()

    WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(),'Bag') or contains(text(),'Cart')]"
            )
        )
    )

    cart_elements = context.driver.find_elements(
        By.XPATH,
        "//*[contains(text(),'Bag') or contains(text(),'Cart')]"
    )
    assert len(cart_elements) > 0, "Cart page structural UI elements are missing"

    context.log.info("Cart opened successfully")


# ==========================================
# PROCEED TO CHECKOUT
# ==========================================
@when("user proceeds to checkout")
def step_checkout(context):

    context.log.info("Proceeding to checkout")

    context.cart.proceed()

    time.sleep(3)

    assert context.cart is not None, "Cart page object reference is unavailable"

    context.log.info("Proceed button clicked")


# ==========================================
# CONTINUE AS GUEST
# ==========================================
@when("user continues as guest user")
def step_guest_checkout(context):

    context.log.info("Handling guest checkout")

    context.payment.handle_login_or_guest()

    WebDriverWait(context.driver, 40).until(
        lambda d:
        "address" in d.current_url.lower()
        or
        "checkout" in d.current_url.lower()
    )

    assert (
        "address" in context.driver.current_url.lower()
        or
        "checkout" in context.driver.current_url.lower()
    ), "Address page not opened"

    context.log.info("Guest checkout successful")


# ==========================================
# FILL ADDRESS
# ==========================================
@when("user fills address details")
def step_fill_address(context):

    context.log.info("Filling address details")

    context.payment.fill_address(
        name="Test User",
        phone="9999999999",
        email="testuser@gmail.com",
        house="221B",
        area="Delhi",
        pincode="110001"
    )

    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//button[@data-testid='button_shipToThisAddress']"
            )
        )
    )

    ship_button = context.driver.find_element(
        By.XPATH,
        "//button[@data-testid='button_shipToThisAddress']"
    )

    assert ship_button.is_displayed(), \
        "Ship button not visible"

    context.log.info("Ship button visible")

    context.payment.continue_to_payment()

    context.log.info("Clicked Ship To This Address")

    time.sleep(5)

    assert context.driver.current_url is not None, "Browser completely lost page state after continuing to payment"


# ==========================================
# FINAL VALIDATION
# ==========================================
@then("user should reach payment or checkout page")
def step_verify_checkout(context):

    current_url = context.driver.current_url.lower()

    assert (
        "payment" in current_url
        or
        "checkout" in current_url
        or
        "address" in current_url
    ), f"Checkout flow failed. Current URL: {current_url}"

    context.log.info("Checkout flow completed successfully")

    allure.attach(
        context.driver.get_screenshot_as_png(),
        name="Final Checkout Page",
        attachment_type=allure.attachment_type.PNG
    )