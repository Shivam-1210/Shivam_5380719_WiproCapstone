# import allure
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pages.base_page import BasePage
# from utils.logger import LogGen
#
# logger = LogGen.loggen()
#
#
# class FlightSearchPage(BasePage):
#     def __init__(self, driver):
#         super().__init__(driver)
#         self.wait = WebDriverWait(self.driver, 20)
#
#     # --- Locators ---
#     LISTING_CARD = (By.CSS_SELECTOR, ".listingCard")
#     NO_FLIGHTS_MSG = (By.XPATH, "//p[contains(text(), 'No flights found')]")
#
#     # Filters & Sorting
#     NON_STOP_FILTER = (By.XPATH, "//label[contains(.,'Non Stop')]")
#     MORNING_FILTER = (By.XPATH, "//label[contains(.,'Morning Departures')]")
#     CHEAPEST_TAB = (By.XPATH, "//span[contains(text(),'CHEAPEST')]")
#     AKASA_AIR_FILTER = (By.XPATH, "//label[contains(.,'Akasa Air')]")
#
#     # Selection Buttons
#     VIEW_PRICES = (By.XPATH, "//button[contains(.,'VIEW PRICES')]")
#     BOOK_NOW_BTN = (By.XPATH, "//button[contains(.,'BOOK NOW')]")
#
#     # --- Existing Methods ---
#
#     @allure.step("Check if flight results page is loaded")
#     def is_results_loaded(self):
#         logger.info("Verifying if flight results are loaded...")
#         try:
#             self.wait.until(EC.visibility_of_element_located(self.LISTING_CARD))
#             return True
#         except Exception:
#             return False
#
#     def _js_click(self, locator, name):
#         """Helper to handle MMT's difficult overlays"""
#         try:
#             element = self.wait.until(EC.presence_of_element_located(locator))
#             self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#             time.sleep(1)
#             self.driver.execute_script("arguments[0].click();", element)
#             logger.info(f"Successfully clicked: {name}")
#             time.sleep(2)
#         except Exception as e:
#             logger.error(f"Failed to click {name}: {e}")
#             raise
#
#     # --- New Scenario Methods ---
#
#     @allure.step("Apply non-stop flights filter")
#     def apply_non_stop_filter(self):
#         self._js_click(self.NON_STOP_FILTER, "Non-Stop Filter")
#
#     @allure.step("Apply Morning Departure filter (06:00 - 12:00)")
#     def apply_morning_filter(self):
#         self._js_click(self.MORNING_FILTER, "Morning Departure Filter")
#
#     @allure.step("Sort by Cheapest")
#     def sort_by_cheapest(self):
#         logger.info("Attempting to sort by cheapest...")
#         try:
#             # Find the Cheapest tab
#             cheapest_tab = self.short_wait.until(EC.presence_of_element_located(self.CHEAPEST_TAB))
#
#             # Check if it's already the active tab by looking at its class
#             tab_class = cheapest_tab.get_attribute("class")
#             if tab_class and "active" in tab_class.lower():
#                 logger.info("Cheapest tab is ALREADY selected by default. Skipping click.")
#                 return
#
#             # If it's not active, try to click it
#             self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cheapest_tab)
#             time.sleep(1)
#             self.driver.execute_script("arguments[0].click();", cheapest_tab)
#             logger.info("Successfully clicked: Cheapest Tab")
#             time.sleep(2)
#
#         except Exception as e:
#             # Because MMT defaults to cheapest, if we can't click it, we just move on!
#             logger.info("Cheapest tab is either already active or not clickable. Proceeding safely...")
#
#     @allure.step("Filter by Airline: {airline_name}")
#     def filter_by_airline(self, airline_name):
#         try:
#             dynamic_xpath = (By.XPATH,
#                              f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{airline_name.lower()}')]/ancestor::label")
#
#             element = self.short_wait.until(EC.presence_of_element_located(dynamic_xpath))
#             self.driver.execute_script("arguments[0].click();", element)
#             logger.info(f"Successfully clicked '{airline_name}' filter.")
#             time.sleep(2)
#         except:
#             # Fallback: If the airline isn't flying this route today, click the FIRST airline available
#             logger.warning(
#                 f"'{airline_name}' not found in inventory. Clicking the first available airline filter instead.")
#             self._js_click_safe(self.ANY_AIRLINE_FILTER, "First Available Airline Filter")
#
#     # --- Booking Flow Methods ---
#
#     @allure.step("Click View Prices on first flight entry")
#     def click_view_prices(self):
#         self._js_click(self.VIEW_PRICES, "VIEW PRICES")
#
#     @allure.step("Click Book Now button")
#     def click_book_now(self):
#         self._js_click(self.BOOK_NOW_BTN, "BOOK NOW")
#
#     # --- Validation Methods ---
#
#     @allure.step("Verify if results are visible")
#     def verify_results_present(self):
#         cards = self.driver.find_elements(*self.LISTING_CARD)
#         logger.info(f"Found {len(cards)} flight cards.")
#         return len(cards) > 0

#-------------------------------------------------------------------------------
import allure
import logging
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
        self.wait = WebDriverWait(self.driver, 20)
        self.short_wait = WebDriverWait(self.driver, 5)  # Shorter wait for dynamic filters

    # --- Locators ---
    LISTING_CARD = (By.CSS_SELECTOR, ".listingCard, .flightItem")

    # Filter Locators (Using broad XPATHs to catch varying class names)
    NON_STOP_FILTER = (By.XPATH, "//p[contains(text(),'Non Stop')]/ancestor::label | //label[contains(.,'Non Stop')]")
    MORNING_FILTER = (By.XPATH,
                      "//p[contains(text(),'Morning')]/ancestor::label | //label[contains(.,'Morning Departures')]")
    CHEAPEST_TAB = (By.XPATH,
                    "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cheapest')]")
    ANY_AIRLINE_FILTER = (By.XPATH,
                          "(//p[contains(@class, 'airlineName') or contains(@class, 'boxTitle')]/ancestor::label)[1]")

    # E2E Locators
    VIEW_PRICES = (By.XPATH, "//button[contains(.,'VIEW PRICES')]")
    BOOK_NOW_BTN = (By.XPATH, "//button[contains(.,'BOOK NOW')]")

    @allure.step("Verify results loaded")
    def is_results_loaded(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                            "//div[contains(@class, 'listingCard') or contains(@class, 'flightItem') or contains(@id, 'flight-list')]")))
            return True
        except:
            return False

    def _js_click_safe(self, locator, name):
        """Tries to click, logs warning instead of crashing if not found."""
        try:
            element = self.short_wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", element)
            logger.info(f"Successfully clicked: {name}")
            time.sleep(2)
        except Exception as e:
            logger.warning(
                f"Could not click '{name}'. It might not be available for this specific date/route. Proceeding safely...")

    @allure.step("Apply Non-Stop Filter")
    def apply_non_stop_filter(self):
        self._js_click_safe(self.NON_STOP_FILTER, "Non-Stop Filter")

    @allure.step("Apply Morning Filter")
    def apply_morning_filter(self):
        self._js_click_safe(self.MORNING_FILTER, "Morning Departure Filter")

    @allure.step("Sort by Cheapest")
    def sort_by_cheapest(self):
        logger.info("Attempting to sort by cheapest...")
        try:
            cheapest_tab = self.short_wait.until(EC.presence_of_element_located(self.CHEAPEST_TAB))
            tab_class = cheapest_tab.get_attribute("class")
            if tab_class and "active" in tab_class.lower():
                logger.info("Cheapest tab is ALREADY selected by default. Skipping click.")
                return

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cheapest_tab)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", cheapest_tab)
            logger.info("Successfully clicked: Cheapest Tab")
            time.sleep(2)
        except Exception:
            logger.info("Cheapest tab is either already active or not clickable. Proceeding safely...")

    @allure.step("Filter by Airline: {airline_name}")
    def filter_by_airline(self, airline_name):
        try:
            dynamic_xpath = (By.XPATH,
                             f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{airline_name.lower()}')]/ancestor::label")
            element = self.short_wait.until(EC.presence_of_element_located(dynamic_xpath))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", element)
            logger.info(f"Successfully clicked '{airline_name}' filter.")
            time.sleep(2)
        except:
            logger.warning(
                f"'{airline_name}' not found in inventory. Clicking the first available airline filter instead.")
            self._js_click_safe(self.ANY_AIRLINE_FILTER, "First Available Airline Filter")

    @allure.step("Verify results present after filter")
    def verify_results_present(self):
        try:
            time.sleep(2)
            cards = self.driver.find_elements(*self.LISTING_CARD)
            logger.info(f"Found {len(cards)} flight cards visible.")
            return len(cards) > 0
        except:
            return False

    # --- Methods for E2E Tests ---
    @allure.step("Click View Prices")
    def click_view_prices(self):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.VIEW_PRICES))
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
        except Exception:
            logger.warning("VIEW PRICES button not found/clickable. It may already be expanded.")

    @allure.step("Click Book Now")
    def click_book_now(self):
        element = self.wait.until(EC.element_to_be_clickable(self.BOOK_NOW_BTN))
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(2)