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

    # Looks for the prominent header shown in your screenshot
    PAGE_HEADER = (By.XPATH, "//*[contains(text(), 'Complete your booking')]")

    ADD_ADULT_BTN = (By.XPATH, "//button[contains(.,'+ ADD NEW ADULT')]")
    # Locators for the passenger details section

    FIRST_NAME = (By.XPATH, "//input[contains(@placeholder, 'First')]")
    LAST_NAME = (By.XPATH, "//input[contains(@placeholder, 'Last')]")
    EMAIL = (By.XPATH, "//input[contains(@placeholder, 'Email')]")
    MOBILE = (By.XPATH, "//input[contains(@placeholder, 'Mobile')]")

    # Generic continue/next button locator
    CONTINUE_BTN = (By.XPATH,
                    "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue')]")

    @allure.step("Check if Booking page is loaded")
    def is_loaded(self):
        logger.info("Verifying if the Booking Review page is loaded...")
        try:
            # Wait for the main header to become visible
            self.wait.until(EC.visibility_of_element_located(self.PAGE_HEADER))
            logger.info("Booking page loaded successfully.")

            # Optional: Scroll down slightly as MMT headers can block elements
            self.driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Timed out waiting for 'Complete your booking' header: {e}")
            return False

    @allure.step("Enter First Name: {first_name}")
    def enter_first_name(self, first_name):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.clear()
            element.send_keys(first_name)
        except Exception as e:
            logger.error(f"Failed to enter first name: {e}")

    @allure.step("Enter Last Name: {last_name}")
    def enter_last_name(self, last_name):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.LAST_NAME))
            element.clear()
            element.send_keys(last_name)
        except Exception as e:
            logger.error(f"Failed to enter last name: {e}")

    @allure.step("Enter Email: {email}")
    def enter_email(self, email):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.EMAIL))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.clear()
            element.send_keys(email)
        except Exception as e:
            logger.error(f"Failed to enter email: {e}")

    @allure.step("Enter Mobile: {mobile}")
    def enter_mobile(self, mobile):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.MOBILE))
            element.clear()
            element.send_keys(mobile)
        except Exception as e:
            logger.error(f"Failed to enter mobile number: {e}")

    @allure.step("Check if contact section is completed")
    def is_contact_section_completed(self):
        try:
            # Just verifying the email field contains data as a proxy for completion
            element = self.wait.until(EC.presence_of_element_located(self.EMAIL))
            if element.get_attribute('value') != "":
                logger.info("Contact details populated successfully.")
                return True
            return False
        except Exception:
            return False

#---------------------------------------------------------------------------------

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
#     # --- Locators ---
#     PAGE_HEADER = (By.XPATH, "//*[contains(text(), 'Complete your booking')]")
#
#     # MMT Quirk: You often have to click this to make the name fields appear
#     ADD_ADULT_BTN = (By.XPATH, "//button[contains(.,'+ ADD NEW ADULT')]")
#
#     FIRST_NAME = (By.XPATH, "//input[contains(@placeholder, 'First')]")
#     LAST_NAME = (By.XPATH, "//input[contains(@placeholder, 'Last')]")
#     GENDER_MALE = (By.XPATH, "//label[contains(.,'MALE')]")
#
#     EMAIL = (By.XPATH, "//input[contains(@placeholder, 'Email')]")
#     MOBILE = (By.XPATH, "//input[contains(@placeholder, 'Mobile')]")
#
#     # State selection (Required for MMT checkout)
#     STATE_DROPDOWN = (By.XPATH, "//div[contains(@class, 'selectState')]")
#     STATE_SEARCH = (By.XPATH, "//input[@placeholder='Search State']")
#     STATE_OPTION = (By.XPATH, "//li[contains(text(),'Maharashtra')]")  # Example
#
#     CONTINUE_BTN = (By.XPATH, "//button[contains(text(),'Continue')] | //button[contains(.,'CONTINUE')]")
#
#     # --- Methods ---
#
#     @allure.step("Check if Booking page is loaded")
#     def is_loaded(self):
#         logger.info("Verifying if the Booking Review page is loaded...")
#         try:
#             # Switch to the newest tab is handled in the test script,
#             # so here we just check for the header.
#             self.wait.until(EC.visibility_of_element_located(self.PAGE_HEADER))
#             return True
#         except Exception as e:
#             logger.error(f"Booking page header not found: {e}")
#             return False
#
#     @allure.step("Enter Passenger Details: {first_name} {last_name}")
#     def enter_passenger_info(self, first_name, last_name):
#         try:
#             # 1. Click Add Adult if visible
#             try:
#                 add_btn = self.driver.find_element(*self.ADD_ADULT_BTN)
#                 self.driver.execute_script("arguments[0].click();", add_btn)
#             except:
#                 logger.info("Add Adult button not found, fields might already be visible.")
#
#             # 2. Fill Names
#             f_name_el = self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))
#             f_name_el.send_keys(first_name)
#             self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
#
#             # 3. Select Gender (Crucial for validation)
#             self.driver.find_element(*self.GENDER_MALE).click()
#
#         except Exception as e:
#             logger.error(f"Error filling passenger info: {e}")
#             raise
#
#     @allure.step("Enter Contact Info: {email}, {mobile}")
#     def enter_contact_details(self, email, mobile):
#         try:
#             email_el = self.wait.until(EC.visibility_of_element_located(self.EMAIL))
#             self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_el)
#             email_el.clear()
#             email_el.send_keys(email)
#
#             mobile_el = self.driver.find_element(*self.MOBILE)
#             mobile_el.clear()
#             mobile_el.send_keys(mobile)
#         except Exception as e:
#             logger.error(f"Error filling contact details: {e}")
#             raise
#
#     @allure.step("Click Continue to Payment")
#     def click_continue(self):
#         try:
#             btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN))
#             self.driver.execute_script("arguments[0].click();", btn)
#             logger.info("Clicked Continue button.")
#         except Exception as e:
#             logger.error(f"Could not click Continue: {e}")
#
#     @allure.step("Check if contact section is completed")
#     def is_contact_section_completed(self):
#         try:
#             # We check if the 'Continue' button is now enabled/visible
#             return self.driver.find_element(*self.CONTINUE_BTN).is_displayed()
#         except:
#             return False