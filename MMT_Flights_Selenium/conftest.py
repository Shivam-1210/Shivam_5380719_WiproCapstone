import os
import pytest
import allure
import subprocess
import time
from datetime import datetime

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




def pytest_unconfigure(config):
    print("\n------- TESTS COMPLETE! GENERATING PERMANENT ALLURE REPORT --------")

    # 1. Get the absolute path to your project root (where conftest.py lives)
    project_root = os.path.dirname(os.path.abspath(__file__))

    # 2. Build absolute paths to the directories
    results_dir = os.path.join(project_root, "reports", "allure-results")
    report_dir = os.path.join(project_root, "reports", "allure-report")

    print(f"Reading raw data from: {results_dir}")
    print(f"Building report inside: {report_dir}")

    try:
        # 3. Use a list format for subprocess which is much safer for Windows paths
        command = ["allure", "generate", results_dir, "-o", report_dir, "--clean"]

        # Run the command and wait for it to finish
        subprocess.run(command, shell=True, check=True)

        print(f"✅ SUCCESS: Report successfully generated!")
        print("-------------------------------------------------------------------\n")

    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Allure generation failed with exit code {e.returncode}")
    except Exception as e:
        print(f"❌ ERROR: Could not generate Allure report: {e}")
