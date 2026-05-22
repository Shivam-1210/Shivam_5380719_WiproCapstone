#
# import time
# import allure
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pages.base_page import BasePage
# from utils.logger import LogGen
#
# logger = LogGen.loggen()
#
#
# class BookingPage(BasePage):
#     def __init__(self, driver):
#         super().__init__(driver)
#         self.wait = WebDriverWait(self.driver, 20)
#
#     # Looks for the prominent header shown in your screenshot
#     PAGE_HEADER = (By.XPATH, "//*[contains(text(), 'Complete your booking')]")
#
#     ADD_ADULT_BTN = (By.XPATH, "//button[contains(.,'+ ADD NEW ADULT')]")
#     # Locators for the passenger details section
#
#     FIRST_NAME = (By.XPATH, "//input[contains(@placeholder, 'First')]")
#     LAST_NAME = (By.XPATH, "//input[contains(@placeholder, 'Last')]")
#     EMAIL = (By.XPATH, "//input[contains(@placeholder, 'Email')]")
#     MOBILE = (By.XPATH, "//input[contains(@placeholder, 'Mobile')]")
#
#     # Generic continue/next button locator
#     CONTINUE_BTN = (By.XPATH,
#                     "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue')]")
#
#     @allure.step("Check if Booking page is loaded")
#     def is_loaded(self):
#         logger.info("Verifying if the Booking Review page is loaded...")
#         try:
#             # Wait for the main header to become visible
#             self.wait.until(EC.visibility_of_element_located(self.PAGE_HEADER))
#             logger.info("Booking page loaded successfully.")
#
#             # Optional: Scroll down slightly as MMT headers can block elements
#             self.driver.execute_script("window.scrollBy(0, 300);")
#             time.sleep(2)
#             return True
#         except Exception as e:
#             logger.error(f"Timed out waiting for 'Complete your booking' header: {e}")
#             return False
#
#     @allure.step("Enter First Name: {first_name}")
#     def enter_first_name(self, first_name):
#         try:
#             element = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME))
#             self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#             element.clear()
#             element.send_keys(first_name)
#         except Exception as e:
#             logger.error(f"Failed to enter first name: {e}")
#
#     @allure.step("Enter Last Name: {last_name}")
#     def enter_last_name(self, last_name):
#         try:
#             element = self.wait.until(EC.element_to_be_clickable(self.LAST_NAME))
#             element.clear()
#             element.send_keys(last_name)
#         except Exception as e:
#             logger.error(f"Failed to enter last name: {e}")
#
#     @allure.step("Enter Email: {email}")
#     def enter_email(self, email):
#         try:
#             element = self.wait.until(EC.element_to_be_clickable(self.EMAIL))
#             self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#             element.clear()
#             element.send_keys(email)
#         except Exception as e:
#             logger.error(f"Failed to enter email: {e}")
#
#     @allure.step("Enter Mobile: {mobile}")
#     def enter_mobile(self, mobile):
#         try:
#             element = self.wait.until(EC.element_to_be_clickable(self.MOBILE))
#             element.clear()
#             element.send_keys(mobile)
#         except Exception as e:
#             logger.error(f"Failed to enter mobile number: {e}")
#
#     @allure.step("Check if contact section is completed")
#     def is_contact_section_completed(self):
#         try:
#             # Just verifying the email field contains data as a proxy for completion
#             element = self.wait.until(EC.presence_of_element_located(self.EMAIL))
#             if element.get_attribute('value') != "":
#                 logger.info("Contact details populated successfully.")
#                 return True
#             return False
#         except Exception:
#             return False

#---------------------------------------------------------------------------------


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

    PAGE_HEADER = (By.XPATH, "//*[contains(text(), 'Complete your booking')]")
    ADD_ADULT_BTN = (By.XPATH, "//button[contains(.,'+ ADD NEW ADULT')]")

    # Improved locators to be more specific
    FIRST_NAME = (By.XPATH, "//input[contains(@placeholder, 'First')]")
    LAST_NAME = (By.XPATH, "//input[contains(@placeholder, 'Last')]")
    # EMAIL = (By.XPATH, "//input[contains(@placeholder, 'Email')]")
    # MOBILE = (By.XPATH, "//input[contains(@placeholder, 'Mobile')]")

    EMAIL = (By.XPATH, "//input[@placeholder='Email ID' or contains(@placeholder, 'Email')]")
    MOBILE = (By.XPATH, "//input[@placeholder='Mobile Number' or contains(@placeholder, 'Mobile')]")

    @allure.step("Check if Booking page is loaded")
    def is_loaded(self):
        logger.info("Verifying if the Booking Review page is loaded...")
        try:
            self.wait.until(EC.visibility_of_element_located(self.PAGE_HEADER))
            logger.info("Booking page loaded successfully.")
            self.driver.execute_script("window.scrollBy(0, 300);")
            return True
        except Exception as e:
            logger.error(f"Timed out waiting for header: {e}")
            return False

    @allure.step("Close unexpected login popup on booking page")
    def close_login_popup_if_present(self):
        try:
            # Look for an 'X' or 'Close' button on a popup
            close_btn = (By.XPATH, "//span[contains(@class, 'close') or contains(@class, 'Close')]")
            if self.driver.find_elements(*close_btn):
                self.driver.find_element(*close_btn).click()
                logger.info("Closed an unexpected popup on the booking page.")
        except:
            pass  # If no popup, just continue

    @allure.step("Click Add Adult Button")
    def click_add_adult(self):
        """CRITICAL: You must click this before names can be entered!"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.ADD_ADULT_BTN))
            element.click()
            logger.info("Clicked '+ ADD NEW ADULT' button.")
        except Exception as e:
            logger.error(f"Could not click Add Adult button: {e}")
            raise e  # Tell Pytest the test failed here!

    @allure.step("Enter First Name: {first_name}")
    def enter_first_name(self, first_name):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME))
            # Scroll to center to avoid headers/footers blocking the click
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.clear()
            element.send_keys(first_name)
            logger.info(f"Entered First Name: {first_name}")
        except Exception as e:
            logger.error(f"Failed to enter first name: {e}")
            raise e  # CRITICAL FIX: Re-raise the error!

    @allure.step("Enter Last Name: {last_name}")
    def enter_last_name(self, last_name):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.LAST_NAME))
            element.clear()
            element.send_keys(last_name)
            logger.info(f"Entered Last Name: {last_name}")
        except Exception as e:
            logger.error(f"Failed to enter last name: {e}")
            raise e

    @allure.step("Enter Email: {email}")
    def enter_email(self, email):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.EMAIL))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)

            element.clear()
            element.send_keys(email)
            logger.info(f"Entered Email: {email}")
        except Exception as e:
            logger.error(f"Failed to enter email: {e}")
            raise e

    @allure.step("Enter Mobile: {mobile}")
    def enter_mobile(self, mobile):
        try:
            # 1. Wait for visibility
            element = self.wait.until(EC.visibility_of_element_located(self.MOBILE))

            # 2. Force scroll to ensure no floating footer/header blocks it
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            # 3. Use JS to clear and set value if normal send_keys fails
            element.click()  # Focus the element first
            element.clear()
            element.send_keys(mobile)
            logger.info(f"Entered Mobile: {mobile}")
        except Exception as e:
            # If standard interaction fails, try a Javascript fallback
            logger.warning("Standard Mobile entry failed, attempting JS fallback...")
            try:
                self.driver.execute_script(f"arguments[0].value='{mobile}';", element)
                logger.info("Entered Mobile via JS fallback.")
            except:
                logger.error(f"Failed to enter mobile number: {e}")
                raise e

    @allure.step("Check if contact section is completed")
    def is_contact_section_completed(self):
        """Verifies if the contact details were populated successfully"""
        try:
            # Verifying the email field contains data as a proxy for completion
            element = self.wait.until(EC.presence_of_element_located(self.EMAIL))
            if element.get_attribute('value') != "":
                logger.info("Contact details populated successfully.")
                return True
            return False
        except Exception as e:
            logger.error(f"Error checking contact section: {e}")
            return False