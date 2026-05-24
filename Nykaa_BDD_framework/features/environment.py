import os
import allure
from selenium import webdriver
from utils.logger import Logger


# =========================
# BEFORE SCENARIO
# =========================
def before_scenario(context, scenario):

    context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.log = Logger.get_logger()

    context.log.info(f"START SCENARIO: {scenario.name}")


# =========================
# AFTER STEP HOOK (MAIN FIX)
# =========================
def after_step(context, step):

    try:
        # Take screenshot for EVERY step (optional but useful)
        screenshot = context.driver.get_screenshot_as_png()

        # CLEAN STEP NAME (avoid / or : issues in file names)
        step_name = step.name.replace(" ", "_").replace("/", "_")[:50]

        # =========================
        # PASSED STEP
        # =========================
        if step.status == "passed":

            context.log.info(f"PASSED STEP: {step.name}")

            allure.attach(
                screenshot,
                name=f"PASSED_{step_name}",
                attachment_type=allure.attachment_type.PNG
            )

        # =========================
        # FAILED STEP
        # =========================
        elif step.status == "failed":

            context.log.error(f"FAILED STEP: {step.name}")

            os.makedirs("reports/screenshots", exist_ok=True)

            screenshot_path = f"reports/screenshots/{step_name}.png"
            context.driver.save_screenshot(screenshot_path)

            allure.attach.file(
                screenshot_path,
                name=f"FAILED_{step_name}",
                attachment_type=allure.attachment_type.PNG
            )

    except Exception as e:
        context.log.error(f"after_step error: {str(e)}")


# =========================
# AFTER SCENARIO
# =========================
def after_scenario(context, scenario):

    context.log.info(f"END SCENARIO: {scenario.name}")

    log_file = "logs/automation.log"

    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            allure.attach(
                f.read(),
                name="Execution Logs",
                attachment_type=allure.attachment_type.TEXT
            )

    if hasattr(context, "driver"):
        context.driver.quit()