import os
import time


class ScreenshotUtil:
    @staticmethod
    def capture(driver, test_name):
        """
        Captures a screenshot and saves it to the reports/screenshots directory.
        Returns the absolute path to the saved screenshot.
        """
        # Define the directory where screenshots will be saved
        screenshot_dir = os.path.join(os.getcwd(), "reports", "screenshots")

        # Automatically create the directory if it doesn't exist
        os.makedirs(screenshot_dir, exist_ok=True)

        # Create a unique filename using the test name and a timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"{test_name}_{timestamp}.png"
        file_path = os.path.join(screenshot_dir, file_name)

        try:
            driver.save_screenshot(file_path)
            return file_path
        except Exception as e:
            print(f"Failed to capture screenshot: {str(e)}")
            return None