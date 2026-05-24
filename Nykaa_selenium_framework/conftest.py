import subprocess
import pytest

from utils.driver_factory import get_driver


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def pytest_sessionfinish(session, exitstatus):
    # Generate and open proper Allure report
    subprocess.Popen(
        "allure serve reports/allure-results",
        shell=True
    )