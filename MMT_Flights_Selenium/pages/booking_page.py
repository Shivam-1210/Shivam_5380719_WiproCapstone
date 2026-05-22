

import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import LogGen

logger = LogGen.loggen()


class BookingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(self.driver, 20)

    # Locators
    PAGE_HEADER = (By.XPATH, "//*[contains(text(), 'Complete your booking')]")
    ADD_ADULT_BTN = (By.XPATH, "//button[contains(.,'+ ADD NEW ADULT')]")
    FIRST_NAME = (By.XPATH, "//input[contains(@placeholder, 'First')]")
    LAST_NAME = (By.XPATH, "//input[contains(@placeholder, 'Last')]")
    EMAIL = (By.XPATH, "//input[@placeholder='Email ID' or contains(@placeholder, 'Email')]")
    MOBILE = (By.XPATH, "//input[@placeholder='Mobile Number' or contains(@placeholder, 'Mobile')]")

    def _safe_send_keys(self, locator, value, field_name):
        """Helper method to handle scrolling, animations, and interractability"""
        try:
            # 1. Wait for PRESENCE in the DOM, not Visibility
            # This is crucial for elements hidden down the page
            element = self.wait.until(EC.presence_of_element_located(locator))

            # 2. Scroll it into the center of the viewport (forces it to become visible)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            # 3. CRITICAL: Wait for animation/overlays to settle
            time.sleep(0.8)

            # 4. Try to click and type normally
            try:
                element.click()
                element.clear()
                element.send_keys(value)
                logger.info(f"Successfully entered {field_name}: {value}")
            except Exception:
                # 5. JS Fallback if a popup is blocking the 'click'
                logger.warning(f"Standard entry for {field_name} blocked. Using JS Fallback.")
                self.driver.execute_script("arguments[0].value = '';", element)  # Clear
                self.driver.execute_script(f"arguments[0].value = '{value}';", element)  # Type
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                                           element)

        except Exception as e:
            logger.error(f"Failed to interact with {field_name}: {e}")
            raise e

    @allure.step("Check if Booking page is loaded")
    def is_loaded(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.PAGE_HEADER))
            return True
        except:
            return False

    @allure.step("Click Add Adult Button")
    def click_add_adult(self):
        element = self.wait.until(EC.element_to_be_clickable(self.ADD_ADULT_BTN))
        element.click()
        logger.info("Clicked '+ ADD NEW ADULT' button.")

    # Now all your entry methods use the 'Safe' helper
    @allure.step("Enter First Name")
    def enter_first_name(self, name):
        self._safe_send_keys(self.FIRST_NAME, name, "First Name")

    @allure.step("Enter Last Name")
    def enter_last_name(self, name):
        self._safe_send_keys(self.LAST_NAME, name, "Last Name")

    @allure.step("Enter Email")
    def enter_email(self, email):
        self._safe_send_keys(self.EMAIL, email, "Email")
    time.sleep(2)

    @allure.step("Enter Mobile")
    def enter_mobile(self, mobile):
        self._safe_send_keys(self.MOBILE, mobile, "Mobile")
    time.sleep(2)

    @allure.step("Check if contact section is completed")
    def is_contact_section_completed(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.EMAIL))
            return element.get_attribute('value') != ""
        except:
            return False