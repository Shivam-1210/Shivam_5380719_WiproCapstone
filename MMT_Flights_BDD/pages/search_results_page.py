
from pages.base_page import BasePage
from locators.flight_locators import FlightLocators
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class SearchResultsPage(BasePage):
    def select_first_flight_and_book(self):
        self.logger.info(f"Select first flight and book")


        # 1. Hard wait to let MMT's heavy React components finish loading
        time.sleep(5)

        # 2. Dismiss any tutorial overlays if they appear
        try:
            if self.is_element_visible(FlightLocators.OKAY_GOT_IT_BTN):
                self.click_element_js(FlightLocators.OKAY_GOT_IT_BTN)
        except:
            pass

        initial_tabs = len(self.driver.window_handles)

        # 3. Find and click the very first button inside the first flight card
        first_card_btn_xpath = "(//div[contains(@class, 'listingCard')])[1]//button"
        try:
            first_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, first_card_btn_xpath)))
            self.driver.execute_script("arguments[0].click();", first_btn)
        except:
            pass

        time.sleep(3)  # Wait for the DOM to react (modal from your image opens here)

        # 4. Aggressive Book Now / Tab Opening Loop
        # Keep looking for a "Book Now" button and clicking it until MMT actually opens the new tab.
        book_now_xpath = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'book now')]"

        for attempt in range(5):  # Try up to 5 times
            if len(self.driver.window_handles) > initial_tabs:
                return  # SUCCESS! A new tab opened. We are done here.

            try:
                # Find ALL "Book Now" buttons on the entire page
                buttons = self.driver.find_elements(By.XPATH, book_now_xpath)
                for btn in buttons:
                    # Only interact with the one visibly showing in the popup modal
                    if btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(3)  # Give the browser 3 seconds to spawn the new tab
                        break  # Break the inner loop, outer loop will check the tab count
            except:
                time.sleep(1)

    def apply_non_stop_filter(self):
        self.logger.info(f"Applying non-stop filter")
        # Wait a few seconds to ensure the left-side filter panel has fully populated via API
        time.sleep(4)

        # Use JS click because MakeMyTrip's actual <input> checkboxes are hidden behind custom UI <span> elements
        self.click_element_js(FlightLocators.NON_STOP_FILTER)

    def is_results_page_loaded(self):
        self.logger.info(f"Checking if results page is loaded")
        from selenium.webdriver.support.ui import WebDriverWait

        try:
            # Wait up to 15 seconds for the URL to contain 'flight/search'
            WebDriverWait(self.driver, 15).until(lambda driver: "flight/search" in driver.current_url)
            return True
        except:
            return False

    def verify_booking_page(self):
        self.logger.info(f"Verifying booking page")
        # MMT opens booking in a new tab. Switch to it first.
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        return self.get_text(FlightLocators.REVIEW_PAGE_HEADER)