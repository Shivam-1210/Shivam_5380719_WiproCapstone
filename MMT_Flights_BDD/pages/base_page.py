from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # We tell the wait to automatically ignore elements that go "stale" during DOM refreshes
        self.wait = WebDriverWait(
            self.driver,
            15,
            ignored_exceptions=[StaleElementReferenceException]
        )

    def click_element(self, locator):
        """Waits for an element to be clickable and clicks it, with a JS fallback."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except ElementClickInterceptedException:
            # Fallback: If an ad or loading overlay blocks the click, force it via JavaScript
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, locator, text):
        """Waits for an element to be visible, clears it, and sends text."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def is_element_visible(self, locator):
        """Returns True if visible within the timeout, otherwise False."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_text(self, locator):
        """Retrieves text from a visible element."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text