# import allure
# import logging
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from pages.base_page import BasePage
# from utils.logger import LogGen
#
# logger = LogGen.loggen()
#
# class HomePage(BasePage):
#     def __init__(self, driver):
#         self.driver = driver
#         self.wait = WebDriverWait(self.driver, 20)
#
#     # Locators (Ensure these match your E2E version)
#     FROM_CITY_LABEL = (By.CSS_SELECTOR, "label[for='fromCity']")
#     FROM_INPUT = (By.CSS_SELECTOR, "input[placeholder='From']")
#     SUGGESTION_LIST = (By.CSS_SELECTOR, "li[role='option']")
#     CLOSE_BTN = (By.CSS_SELECTOR, "span.commonModal__close")
#
#     # Passenger Locators
#     TRAVELLERS_LABEL = (By.XPATH, "//label[@for='travellers']")
#     APPLY_BTN = (By.XPATH, "//button[@data-cy='travellerApplyBtn']")
#
#     # Error Locators
#     # This now specifically targets the red error text in your screenshot
#     ERROR_CONTAINER = (By.XPATH,
#                        "//*[contains(text(),'cannot be the same')] | "
#                        "//*[contains(text(),'cannot be more than adults')]"
#                        )
#
#
#     @allure.step("Dismiss overlay if present")
#     def dismiss_modal_if_any(self):
#         """Try multiple locators to ensure the login modal is closed"""
#         locators = [
#             (By.CSS_SELECTOR, "span.commonModal__close"),
#             (By.XPATH, "//span[@data-cy='closeModal']"),
#             (By.ID, "webklipper-publisher-widget-container-notification-close-div")
#         ]
#         for locator in locators:
#             try:
#                 elements = self.driver.find_elements(*locator)
#                 if elements:
#                     elements[0].click()
#                     logger.info(f"Dismissed modal using: {locator}")
#                     time.sleep(1)
#                     break
#             except:
#                 continue
#         # Fallback: Click the body to dismiss simple overlays
#         try:
#             self.driver.find_element(By.TAG_NAME, "body").click()
#         except:
#             pass
#
#     def select_flight_cities(self, from_city, to_city):
#         """Improved selection to prevent TimeoutException"""
#         try:
#             # 1. Click From City Label (Use JS to bypass overlays)
#             from_lbl = self.wait.until(EC.element_to_be_clickable(self.FROM_CITY_LABEL))
#             self.driver.execute_script("arguments[0].click();", from_lbl)
#
#             # 2. Wait for Input and Type
#             input_field = self.wait.until(EC.visibility_of_element_located(self.FROM_INPUT))
#             input_field.send_keys(from_city)
#             time.sleep(2)  # Allow suggestions to load
#
#             # 3. Select first suggestion
#             suggestions = self.wait.until(EC.presence_of_all_elements_located(self.SUGGESTION_LIST))
#             suggestions[0].click()
#             logger.info(f"Selected From City: {from_city}")
#
#         except Exception as e:
#             logger.error(f"Failed city selection: {e}")
#             raise
#
#     def load(self, url):
#         logger.info(f"Opening website: {url}")
#         self.driver.get(url)
#         self.driver.maximize_window()
#
#     def close_popup(self):
#         try:
#             time.sleep(2)
#             close_btn = self.driver.find_element(By.XPATH, "//span[@data-cy='closeModal']")
#             self.driver.execute_script("arguments[0].click();", close_btn)
#             logger.info("LOGIN POPUP CLOSED")
#             time.sleep(1)
#         except:
#             try:
#                 body = self.driver.find_element(By.TAG_NAME, "body")
#                 body.click()
#                 logger.info("CLICKED OUTSIDE POPUP")
#                 time.sleep(1)
#             except:
#                 logger.info("NO POPUP FOUND")
#
#     def select_flight(self):
#         try:
#             flight = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, '//li[@data-cy="menu_Flights"]'))
#             )
#             self.driver.execute_script("arguments[0].click();", flight)
#             logger.info("FLIGHT CLICKED")
#             time.sleep(2)
#         except Exception as e:
#             logger.info(f"FLIGHT CLICK ISSUE: {str(e)}")
#             raise
#
#     def select_flight_mode(self):
#
#             flight = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-cy="menu_Flights"]')))
#             self.driver.execute_script("arguments[0].click();", flight)
#             one_way = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(.,'One Way')]")))
#             self.driver.execute_script("arguments[0].click();", one_way)
#
#
#     def select_one_way(self):
#         try:
#             one_way = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//li[contains(.,'One Way')]"))
#             )
#             self.driver.execute_script("arguments[0].click();", one_way)
#             logger.info("ONE WAY SELECTED")
#             time.sleep(1)
#         except Exception as e:
#             logger.info(f"ONE WAY CLICK ISSUE: {str(e)}")
#             raise
#
#     def select_flight_cities(self, from_city, to_city):
#         FROM_CITY_LABEL = (By.XPATH, "//label[@for='fromCity']")
#         TO_CITY_LABEL = (By.XPATH, "//label[@for='toCity']")
#         FROM_INPUT = (By.XPATH, "//input[@placeholder='From']")
#         TO_INPUT = (By.XPATH, "//input[@placeholder='To']")
#
#         def select_city(label_locator, input_locator, city, field_name):
#             # 1. Click the main field to open the search box
#             label_el = self.wait.until(EC.element_to_be_clickable(label_locator))
#             # Use a real click first, fallback to JS if blocked
#             try:
#                 label_el.click()
#             except:
#                 self.driver.execute_script("arguments[0].click();", label_el)
#
#             logger.info(f"CLICKED LABEL: {field_name}")
#
#             # 2. Wait for the search input to appear (Use a more generic locator if needed)
#             # Often the search box has class 'react-autosuggest__input'
#             search_input_xpath = "//input[contains(@class, 'react-autosuggest__input')]"
#             input_el = self.wait.until(EC.visibility_of_element_located((By.XPATH, search_input_xpath)))
#
#             # 3. Type the city (Fixed double-typing bug)
#             input_el.clear()
#             for char in city:
#                 input_el.send_keys(char)
#                 time.sleep(0.1)  # Natural typing speed helps suggestions load
#
#             logger.info(f"TYPED CITY: {city} in {field_name}")
#             time.sleep(2)  # Wait for suggestions to populate
#
#             # 4. Select the first suggestion
#             input_el.send_keys(Keys.ARROW_DOWN)
#             time.sleep(0.5)
#             input_el.send_keys(Keys.ENTER)
#             logger.info(f"SELECTED CITY: {city}")
#
#     def select_date(self, date_value):
#         """
#         date_value format: "Fri Jun 19 2026"
#         """
#         logger.info(f"SELECTING DATE: {date_value}")
#         try:
#             # 1. Click the departure date area first to ensure calendar is open
#             # (Only needed if the calendar doesn't open automatically)
#
#             # 2. Define the date locator
#             date_xpath = f"//div[@aria-label='{date_value}']"
#
#             # 3. Wait for the date and click it
#             # We use execute_script because MMT elements are often overlapped by overlays
#             element = self.wait.until(EC.presence_of_element_located((By.XPATH, date_xpath)))
#             self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
#             time.sleep(1)
#             self.driver.execute_script("arguments[0].click();", element)
#
#             logger.info(f"DEPARTURE DATE {date_value} SELECTED")
#         except Exception as e:
#             logger.error(f"FAILED TO SELECT DATE: {str(e)}")
#             # Optional: Add logic here to click the 'Next Month' button if date not found
#             raise
#
#     @allure.step("Select Passengers")
#     def select_passengers(self, adults, infants):
#         # Use JavaScript click to bypass any remaining overlays (like the calendar)
#         label = self.wait.until(EC.presence_of_element_located(self.TRAVELLERS_LABEL))
#         self.driver.execute_script("arguments[0].click();", label)
#         time.sleep(1)
#
#         # Select Adults
#         adult_xpath = f"//li[@data-cy='adults-{adults}']"
#         self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH, adult_xpath))
#
#         # Select Infants
#         if int(infants) > 0:
#             infant_xpath = f"//li[@data-cy='infants-{infants}']"
#             self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH, infant_xpath))
#
#         # Error check: On MMT, the error appears instantly in the popup
#         time.sleep(1)
#
#     def click_search(self):
#         logger.info("CLICKING SEARCH BUTTON")
#
#         search_btn = self.wait.until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "//a[contains(@class, 'searchBtn') or text()='Search']")
#             )
#         )
#
#         self.driver.execute_script(
#             "arguments[0].scrollIntoView({block:'center'});",
#             search_btn
#         )
#
#         time.sleep(2)
#         search_btn.click()
#
#         logger.info("SEARCH BUTTON CLICKED SUCCESSFULLY")
#         time.sleep(10)
#
#     # Locator for the error message that pops up
#     ERROR_MESSAGE_LOCATOR = (By.XPATH, "//p[contains(@class,'errorMessage')] | //div[contains(@class,'error')]")
#
#     @allure.step("Capture UI error message")
#     def get_ui_error_message(self):
#         try:
#             # Wait specifically for the error message to become visible
#             error_el = self.wait.until(EC.visibility_of_element_located(self.ERROR_CONTAINER))
#             return error_el.text
#         except:
#             # Fallback for logging
#             container = self.driver.find_element(By.CLASS_NAME, "fsw")
#             return container.text.encode('ascii', 'ignore').decode('ascii')

#---------------------------------------------------------------------------
import allure
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import LogGen

logger = LogGen.loggen()

class HomePage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    # --- Locators ---
    FROM_CITY_LABEL = (By.XPATH, "//label[@for='fromCity']")
    TO_CITY_LABEL = (By.XPATH, "//label[@for='toCity']")
    SEARCH_INPUT = (By.XPATH, "//input[contains(@class, 'react-autosuggest__input')]")
    SUGGESTION_LIST = (By.CSS_SELECTOR, "li[role='option']")
    TRAVELLERS_LABEL = (By.XPATH, "//label[@for='travellers']")
    ERROR_CONTAINER = (By.XPATH, "//*[contains(text(),'cannot be the same')] | //*[contains(text(),'cannot be more than adults')]")

    def load(self, url):
        logger.info(f"Opening website: {url}")
        self.driver.get(url)
        self.driver.maximize_window()

    @allure.step("Dismiss login/overlay modal")
    def dismiss_modal_if_any(self):
        locators = [
            (By.CSS_SELECTOR, "span.commonModal__close"),
            (By.XPATH, "//span[@data-cy='closeModal']"),
            (By.ID, "webklipper-publisher-widget-container-notification-close-div")
        ]
        for locator in locators:
            try:
                elements = self.driver.find_elements(*locator)
                if elements:
                    elements[0].click()
                    logger.info(f"Dismissed modal using: {locator}")
                    time.sleep(1)
                    return
            except:
                continue
        try: self.driver.find_element(By.TAG_NAME, "body").click()
        except: pass

    # Alias for older tests that use close_popup
    def close_popup(self):
        self.dismiss_modal_if_any()

    @allure.step("Select Flight mode")
    def select_flight(self):
        flight = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@data-cy="menu_Flights"]')))
        self.driver.execute_script("arguments[0].click();", flight)

    @allure.step("Select One Way")
    def select_one_way(self):
        one_way = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(.,'One Way')]")))
        self.driver.execute_script("arguments[0].click();", one_way)

    @allure.step("Select Flight and One Way mode")
    def select_flight_and_one_way(self):
        self.select_flight()
        self.select_one_way()
        logger.info("Flight mode and One Way selected")

    @allure.step("Select Cities: {from_city} to {to_city}")
    def select_flight_cities(self, from_city, to_city):
        def select_city_logic(label_locator, city_name, field_name):
            label_el = self.wait.until(EC.element_to_be_clickable(label_locator))
            self.driver.execute_script("arguments[0].click();", label_el)

            input_el = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
            input_el.clear()
            input_el.send_keys(city_name)
            time.sleep(2)  # Wait for suggestions

            suggestions = self.wait.until(EC.presence_of_all_elements_located(self.SUGGESTION_LIST))
            suggestions[0].click()
            logger.info(f"Selected {field_name}: {city_name}")
            time.sleep(1)

        select_city_logic(self.FROM_CITY_LABEL, from_city, "From City")
        select_city_logic(self.TO_CITY_LABEL, to_city, "To City")

    @allure.step("Select Passengers")
    def select_passengers(self, adults, infants):
        label = self.wait.until(EC.presence_of_element_located(self.TRAVELLERS_LABEL))
        self.driver.execute_script("arguments[0].click();", label)
        time.sleep(1)

        adult_xpath = f"//li[@data-cy='adults-{adults}']"
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH, adult_xpath))

        if int(infants) > 0:
            infant_xpath = f"//li[@data-cy='infants-{infants}']"
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH, infant_xpath))
        time.sleep(1)

    @allure.step("Capture UI error message")
    def get_ui_error_message(self):
        try:
            error_el = self.wait.until(EC.visibility_of_element_located(self.ERROR_CONTAINER))
            return error_el.text
        except:
            container_text = self.driver.find_element(By.CLASS_NAME, "fsw").text
            return container_text

    @allure.step("Select Date: {date_value}")
    def select_date(self, date_value):
        logger.info(f"SELECTING DATE: {date_value}")
        try:
            date_xpath = f"//div[@aria-label='{date_value}']"
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, date_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", element)
            logger.info(f"DEPARTURE DATE {date_value} SELECTED")
        except Exception as e:
            logger.error(f"FAILED TO SELECT DATE: {str(e)}")
            raise

    @allure.step("Click Search Button")
    def click_search(self):
        logger.info("CLICKING SEARCH BUTTON")
        search_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'searchBtn') or text()='Search']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_btn)
        time.sleep(2)
        search_btn.click()
        logger.info("SEARCH BUTTON CLICKED SUCCESSFULLY")
        time.sleep(5)






