import os
import shutil
import allure
from allure_commons.types import AttachmentType

from seleniumbase import Driver

from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader

logger = LogGen.loggen()


def before_all(context):
    # Clean up old results before starting
    if os.path.exists("reports/allure-results"):
        shutil.rmtree("reports/allure-results")
    os.makedirs("reports/allure-results", exist_ok=True)



def before_scenario(context, scenario):
    logger.info(f"========== STARTING SCENARIO: {scenario.name} ==========")

    # Initialize SeleniumBase in Undetected Chromedriver (UC) Mode
    context.driver = Driver(uc=True, headless=False)

    context.driver.maximize_window()
    context.driver.implicitly_wait(ConfigReader.get_implicit_wait())


def after_step(context, step):
    # Take a screenshot for EVERY step
    # We use a try-except block to prevent the test from crashing if the driver is already closed
    try:
        screenshot = context.driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name=f"{step.name} (Status: {step.status})",
            attachment_type=AttachmentType.PNG
        )
    except Exception as e:
        print(f"Could not capture screenshot for step {step.name}: {e}")


def after_scenario(context, scenario):
    logger.info(f"========== CLOSING SCENARIO: {scenario.name} ==========")

    if hasattr(context, 'driver'):
        try:
            # Attach the automation log to the Allure report for deep debugging
            if os.path.exists("logs/automation.log"):
                with open("logs/automation.log", "r") as log_file:
                    allure.attach(
                        log_file.read(),
                        name="Execution Logs",
                        attachment_type=allure.attachment_type.TEXT
                    )

            context.driver.quit()
            logger.info("BROWSER CLOSED SUCCESSFULLY")

        except Exception as e:
            logger.error(f"ERROR CLOSING BROWSER: {str(e)}")


def after_all(context):
    print("\n[INFO] Tests finished. Generating Allure Report")

    # Build the HTML report into the allure-report folder
    os.system("allure generate reports/allure-results -o reports/allure-report --clean")

    print("[INFO] Allure report successfully saved in the 'reports/allure-report' folder.")