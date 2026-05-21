import os
import pytest
import allure
import time

from seleniumbase import Driver
from utils.logger import LogGen
from utils.screenshot import ScreenshotUtil

logger = LogGen.loggen()


@pytest.fixture()
def driver():
    logger.info("========== STARTING TEST ==========")

    driver = Driver(uc=True)
    driver.maximize_window()
    driver.implicitly_wait(5)

    logger.info("OPENING MAKEMYTRIP WEBSITE")
    driver.get("https://www.makemytrip.com")

    time.sleep(2)
    logger.info(f"CURRENT URL: {driver.current_url}")

    yield driver

    logger.info("========== CLOSING TEST ==========")

    try:
        driver.quit()
        logger.info("BROWSER CLOSED SUCCESSFULLY")
    except Exception as e:
        logger.error(f"ERROR CLOSING BROWSER: {str(e)}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    if "driver" not in item.funcargs:
        return

    driver = item.funcargs["driver"]

    try:
        if report.passed:
            logger.info("TEST PASSED - CAPTURING SCREENSHOT")
            path = ScreenshotUtil.capture(driver, f"{item.name}_PASS")
        else:
            logger.error("TEST FAILED - CAPTURING SCREENSHOT")
            path = ScreenshotUtil.capture(driver, f"{item.name}_FAIL")

        if path and os.path.exists(path):
            allure.attach.file(
                path,
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
    except Exception as e:
        logger.error(f"SCREENSHOT FAILED: {str(e)}")

    import os
    import subprocess

    def pytest_unconfigure(config):
        print("\n------- TESTS COMPLETE! GENERATING PERMANENT ALLURE REPORT --------")

        # Path to your raw data
        results_dir = os.path.join("reports", "allure-results")
        # Path to where you want the beautiful dashboard saved
        report_dir = os.path.join("reports", "allure-report")

        try:
            # -o tells Allure to use a specific Output directory
            # --clean removes the old report before building the new one
            command = f'allure generate "{results_dir}" -o "{report_dir}" --clean'

            # We use subprocess.run so the terminal waits until the report is 100% ready
            subprocess.run(command, shell=True, check=True)

            print(f"SUCCESS: Report generated in: {report_dir}")
        except Exception as e:
            print(f"ERROR: Could not generate Allure report: {e}")


