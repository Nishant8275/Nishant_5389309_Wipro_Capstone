from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


# Launch browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()

try:
    # Open Nykaa
    driver.get("https://www.nykaa.com/")

    time.sleep(5)

    # Search shampoo
    search_box = driver.find_element(By.NAME, "search-suggestions-nykaa")

    search_box.send_keys("shampoo")

    search_box.send_keys(Keys.ENTER)

    time.sleep(5)

    # Click first product
    products = driver.find_elements(
        By.XPATH,
        "//div[contains(@class,'productWrapper')]"
    )

    if len(products) > 0:
        products[0].click()

    time.sleep(10)

    # Switch tab
    driver.switch_to.window(driver.window_handles[-1])

    # Validation
    assert "shampoo" in driver.page_source.lower()

    print("TEST PASSED ✅")

    # Screenshot
    driver.save_screenshot("nykaa_test.png")

except Exception as e:

    print("TEST FAILED ❌")
    print(e)

finally:
    time.sleep(3)
    driver.quit()