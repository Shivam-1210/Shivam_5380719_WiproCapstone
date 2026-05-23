import os
from datetime import datetime

class ScreenshotUtil:
    @staticmethod
    def capture_screenshot(driver, name):

        # Keeps screenshots organized inside the reports folder
        screenshot_dir = os.path.join(os.path.dirname(__file__), '..', 'reports', 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Cleans the name to ensure it's a valid filename
        clean_name = "".join([c for c in name if c.isalnum() or c in (' ', '_')]).rstrip()
        filename = f"{clean_name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)

        driver.save_screenshot(filepath)
        return filepath