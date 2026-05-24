# utils/screenshot_util.py

import os
from datetime import datetime


class ScreenshotUtil:

    @staticmethod
    def take_screenshot(driver, name="failure"):

        try:

            # check driver exists
            if driver is None:
                return

            # check session active
            if not driver.session_id:
                print("Driver already closed, skipping screenshot")
                return

            # create folder
            folder_path = "reports/screenshots"

            os.makedirs(folder_path, exist_ok=True)

            # timestamp
            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            # file path
            file_path = (
                f"{folder_path}/{name}_{timestamp}.png"
            )

            # save screenshot
            driver.save_screenshot(file_path)

            print(f"Screenshot saved: {file_path}")

            return file_path

        except Exception as e:

            print(f"Screenshot failed safely: {e}")