from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import LogGen

logger = LogGen.loggen()

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logger
        self.logger.info("BasePage initialized")

    def click(self, locator):
        self.logger.info(f"Clicking on locator: {locator}")
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
            self.logger.info(f"Successfully clicked on locator: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click on locator: {locator} | Exception: {str(e)}")
            raise

    def type(self, locator, text):
        self.logger.info(f"Typing '{text}' into locator: {locator}")
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Successfully typed into locator: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to type into locator: {locator} | Exception: {str(e)}")
            raise

    def send_text(self, locator, text):
        self.type(locator, text)

    def get_text(self, locator):
        self.logger.info(f"Getting text from locator: {locator}")
        try:
            text = self.wait.until(EC.visibility_of_element_located(locator)).text
            self.logger.info(f"Successfully got text '{text}' from locator: {locator}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from locator: {locator} | Exception: {str(e)}")
            raise

    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False