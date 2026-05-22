import os
from datetime import datetime


class ScreenshotUtil:

    @staticmethod
    def take_screenshot(driver, name="failure"):
        try:
            if driver is None:
                return

            if not driver.session_id:
                print("Driver already closed, skipping screenshot")
                return

            os.makedirs("screenshots", exist_ok=True)

            file_path = f"screenshots/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(file_path)

        except Exception as e:
            print(f"Screenshot failed safely: {e}")