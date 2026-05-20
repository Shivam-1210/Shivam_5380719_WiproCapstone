# import allure
# import logging
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pages.base_page import BasePage
#
# # Get the logger from your utility
# from utils.logger import LogGen
#
# logger = LogGen.loggen()
#
#
# class FlightSearchPage(BasePage):
#     def __init__(self, driver):
#         super().__init__(driver)
#         # Standard Selenium Wait
#         self.wait = WebDriverWait(self.driver, 20)
#
#     # Locators
#     LISTING_CARD = (By.CSS_SELECTOR, ".listingCard")
#     NO_FLIGHTS_MSG = (By.XPATH, "//p[contains(text(), 'No flights found')]")
#     NON_STOP_FILTER = (By.XPATH, "//span[contains(text(),'Non Stop')]")
#     VIEW_PRICES = (By.XPATH, "//button[span[text()='View Prices']]")
#     BOOK_NOW_BTN = (By.XPATH, "//button[text()='Book Now']")
#
#     @allure.step("Check if flight results page is loaded")
#     def is_results_loaded(self):
#         logger.info("Verifying if flight results are loaded...")
#         try:
#             # 1. Wait for at least one flight card to be visible
#             self.wait.until(EC.visibility_of_element_located(self.LISTING_CARD))
#             logger.info("Flight results detected successfully.")
#             return True
#         except Exception:
#             # 2. If cards aren't found, check if 'No Flights Found' is displayed
#             try:
#                 no_flights = self.driver.find_elements(*self.NO_FLIGHTS_MSG)
#                 if len(no_flights) > 0:
#                     logger.error("MMT returned 'No flights found' for the selected criteria.")
#                     return False
#             except:
#                 pass
#
#             logger.error("Timed out waiting for flight results to appear.")
#             return False
#
#     @allure.step("Apply non-stop flights filter")
#     def apply_non_stop_filter(self):
#         try:
#             element = self.wait.until(EC.element_to_be_clickable(self.NON_STOP_FILTER))
#             self.driver.execute_script("arguments[0].click();", element)
#             logger.info("Non-stop filter applied.")
#         except Exception as e:
#             logger.error(f"Could not apply Non-stop filter: {e}")
#
#     @allure.step("Click View Prices on first flight entry")
#     def click_view_prices(self):
#         try:
#             # Using JS click because MMT buttons are often behind transparent overlays
#             element = self.wait.until(EC.element_to_be_clickable(self.VIEW_PRICES))
#             self.driver.execute_script("arguments[0].click();", element)
#             logger.info("Clicked 'View Prices'.")
#         except Exception as e:
#             logger.error(f"Failed to click View Prices: {e}")
#
#     @allure.step("Click Book Now button")
#     def click_book_now(self):
#         try:
#             element = self.wait.until(EC.element_to_be_clickable(self.BOOK_NOW_BTN))
#             self.driver.execute_script("arguments[0].click();", element)
#             logger.info("Clicked 'Book Now'.")
#         except Exception as e:
#             logger.error(f"Failed to click Book Now: {e}")


#_________________________________________________________________________________________________________________________

import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

from utils.logger import LogGen

logger = LogGen.loggen()


class FlightSearchPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Standard Selenium Wait
        self.wait = WebDriverWait(self.driver, 20)

    # Locators (Updated to match exact MakeMyTrip UI)
    LISTING_CARD = (By.CSS_SELECTOR, ".listingCard")
    NO_FLIGHTS_MSG = (By.XPATH, "//p[contains(text(), 'No flights found')]")
    NON_STOP_FILTER = (By.XPATH, "//label[contains(.,'Non Stop')]")
    VIEW_PRICES = (By.XPATH, "//button[contains(.,'VIEW PRICES')]")
    BOOK_NOW_BTN = (By.XPATH, "//button[contains(.,'BOOK NOW')]")

    @allure.step("Check if flight results page is loaded")
    def is_results_loaded(self):
        logger.info("Verifying if flight results are loaded...")
        try:
            self.wait.until(EC.visibility_of_element_located(self.LISTING_CARD))
            logger.info("Flight results detected successfully.")
            return True
        except Exception:
            try:
                no_flights = self.driver.find_elements(*self.NO_FLIGHTS_MSG)
                if len(no_flights) > 0:
                    logger.error("MMT returned 'No flights found' for the selected criteria.")
                    return False
            except:
                pass
            logger.error("Timed out waiting for flight results to appear.")
            return False

    @allure.step("Apply non-stop flights filter")
    def apply_non_stop_filter(self):
        try:
            # Using presence instead of clickable to bypass MMT overlay banners
            element = self.wait.until(EC.presence_of_element_located(self.NON_STOP_FILTER))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", element)
            logger.info("Non-stop filter applied.")
            time.sleep(2) # Wait for page to refresh results
        except Exception as e:
            logger.warning(f"Could not apply Non-stop filter (may already be selected): {e}")

    @allure.step("Click View Prices on first flight entry")
    def click_view_prices(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.VIEW_PRICES))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", element)
            logger.info("Clicked 'VIEW PRICES'.")
            time.sleep(2) # Wait for the tray to slide open
        except Exception as e:
            logger.error(f"Failed to click View Prices: {e}")
            raise # Stop test if we can't open prices

    @allure.step("Click Book Now button")
    def click_book_now(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.BOOK_NOW_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", element)
            logger.info("Clicked 'BOOK NOW'.")
        except Exception as e:
            logger.error(f"Failed to click Book Now: {e}")
            raise # Stop test if we can't book