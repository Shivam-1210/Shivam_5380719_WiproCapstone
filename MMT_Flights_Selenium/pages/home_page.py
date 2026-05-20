import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import LogGen

logger = LogGen.loggen()

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self, url):
        logger.info(f"Opening website: {url}")
        self.driver.get(url)
        self.driver.maximize_window()

    def close_popup(self):
        try:
            time.sleep(2)
            close_btn = self.driver.find_element(By.XPATH, "//span[@data-cy='closeModal']")
            self.driver.execute_script("arguments[0].click();", close_btn)
            logger.info("LOGIN POPUP CLOSED")
            time.sleep(1)
        except:
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.click()
                logger.info("CLICKED OUTSIDE POPUP")
                time.sleep(1)
            except:
                logger.info("NO POPUP FOUND")

    def select_flight(self):
        try:
            flight = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//li[@data-cy="menu_Flights"]'))
            )
            self.driver.execute_script("arguments[0].click();", flight)
            logger.info("FLIGHT CLICKED")
            time.sleep(2)
        except Exception as e:
            logger.info(f"FLIGHT CLICK ISSUE: {str(e)}")
            raise

    def select_one_way(self):
        try:
            one_way = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//li[contains(.,'One Way')]"))
            )
            self.driver.execute_script("arguments[0].click();", one_way)
            logger.info("ONE WAY SELECTED")
            time.sleep(1)
        except Exception as e:
            logger.info(f"ONE WAY CLICK ISSUE: {str(e)}")
            raise

    def select_flight_cities(self, from_city, to_city):
        FROM_CITY_LABEL = (By.XPATH, "//label[@for='fromCity']")
        TO_CITY_LABEL = (By.XPATH, "//label[@for='toCity']")
        FROM_INPUT = (By.XPATH, "//input[@placeholder='From']")
        TO_INPUT = (By.XPATH, "//input[@placeholder='To']")

        def select_city(label_locator, input_locator, city, field_name):
            label_el = self.wait.until(EC.element_to_be_clickable(label_locator))
            self.driver.execute_script("arguments[0].click();", label_el)
            logger.info(f"CLICKED LABEL: {field_name}")
            time.sleep(1)

            input_el = self.wait.until(EC.visibility_of_element_located(input_locator))
            input_el.click()
            time.sleep(0.5)

            input_el.send_keys(Keys.CONTROL + "a")
            input_el.send_keys(Keys.DELETE)
            time.sleep(0.5)

            for ch in city:
                input_el.send_keys(ch)
                time.sleep(0.2)

            logger.info(f"TYPED CITY: {city} in {field_name}")
            time.sleep(1.5)

            input_el.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            input_el.send_keys(Keys.ENTER)

            logger.info(f"SELECTED CITY: {city} in {field_name}")
            time.sleep(1.5)

        select_city(FROM_CITY_LABEL, FROM_INPUT, from_city, "fromCity")
        select_city(TO_CITY_LABEL, TO_INPUT, to_city, "toCity")

    def select_date(self, date_value):
        """
        date_value format: "Fri Jun 19 2026"
        """
        logger.info(f"SELECTING DATE: {date_value}")
        try:
            # 1. Click the departure date area first to ensure calendar is open
            # (Only needed if the calendar doesn't open automatically)

            # 2. Define the date locator
            date_xpath = f"//div[@aria-label='{date_value}']"

            # 3. Wait for the date and click it
            # We use execute_script because MMT elements are often overlapped by overlays
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, date_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", element)

            logger.info(f"DEPARTURE DATE {date_value} SELECTED")
        except Exception as e:
            logger.error(f"FAILED TO SELECT DATE: {str(e)}")
            # Optional: Add logic here to click the 'Next Month' button if date not found
            raise

    def click_search(self):
        logger.info("CLICKING SEARCH BUTTON")

        search_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@class, 'searchBtn') or text()='Search']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            search_btn
        )

        time.sleep(2)
        search_btn.click()

        logger.info("SEARCH BUTTON CLICKED SUCCESSFULLY")
        time.sleep(10)