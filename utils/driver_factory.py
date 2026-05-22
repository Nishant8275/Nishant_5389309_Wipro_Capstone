from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    return driver