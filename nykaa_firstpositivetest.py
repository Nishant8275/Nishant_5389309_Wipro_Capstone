"""""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time



driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()

try:

    # -----------------------------------
    driver.get("https://www.nykaa.com/")

    print("Nykaa opened successfully")

    time.sleep(5)

    # -----------------------------------
    search_box = driver.find_element(
        By.NAME,
        "search-suggestions-nykaa"
    )

    search_box.send_keys("shampoo")

    search_box.send_keys(Keys.ENTER)

    print("Product searched successfully")

    time.sleep(5)

    # -----------------------------------
    products = driver.find_elements(
        By.XPATH,
        "//div[contains(@class,'productWrapper')]"
    )

    products[0].click()

    print("First product opened")

    time.sleep(5)

    # -----------------------------------
    driver.switch_to.window(driver.window_handles[-1])

    print("Switched to product tab")

    time.sleep(3)

    # -----------------------------------
    add_to_bag = driver.find_element(
        By.XPATH,
        "//span[contains(text(),'Add to Bag')]"
    )

    add_to_bag.click()

    print("Product added to bag")

    time.sleep(5)

    # -----------------------------------
    bag = driver.find_element(
        By.XPATH,
        "//button[contains(@class,'css-g4vs13')]"
    )

    bag.click()

    print("Cart opened")

    time.sleep(5)

    # -----------------------------------
    try:
        frame = driver.find_element(By.TAG_NAME, "iframe")

        driver.switch_to.frame(frame)

        print("Switched to cart frame")

    except:
        print("No frame present")

    time.sleep(3)

    # -----------------------------------
    proceed = driver.find_element(
        By.XPATH,
        "//span[contains(text(),'Proceed')]"
    )

    proceed.click()

    print("Proceed button clicked")

    time.sleep(5)

    # -----------------------------------
    if "payment" in driver.page_source.lower():

        print("POSITIVE TEST CASE PASSED")

    else:

        print("Payment page not reached")

    # -----------------------------------
    driver.save_screenshot("positive_test_pass.png")

except Exception as e:

    print("POSITIVE TEST FAILED")

    print(e)

    driver.save_screenshot("positive_test_fail.png")

finally:

    time.sleep(5)

    driver.quit()