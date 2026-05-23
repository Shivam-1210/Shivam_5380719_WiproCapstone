import time

from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import logger
from utils.logger import LogGen

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        self.logger = LogGen.loggen()

    def click_element(self, locator):

        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicked on element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click {locator}")
            raise e

    def enter_text(self, locator, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Entered text '{text}' into {locator}")
        except Exception as e:
            self.logger.error(f"Failed to enter text in {locator}")
            raise e

    def get_text(self, locator):
        self.logger.info(f"Getting text from {locator}")
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.text
        except Exception as e:
            self.logger.error(f"Failed to get text from {locator}")
            raise e

    def is_element_visible(self, locator):
        self.logger.info(f"Checking visibility of {locator}")
        """Returns True if visible within the timeout, otherwise False."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            self.logger.error(f"Timed out while checking visibility of {locator}")
            return False

    def click_element_js(self, locator):
        self.logger.info(f"Clicking {locator}")
        """Forces a click using JavaScript to bypass overlapping UI elements."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_to_element(self, locator):
        self.logger.info(f"Scrolling {locator}")
        """Scrolls the page until the element is in the center of the viewport."""

        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.logger.info(f"Scrolled {locator}")
        time.sleep(1)