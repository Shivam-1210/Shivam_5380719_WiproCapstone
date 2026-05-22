
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.flight_locators import FlightLocators
import time

class SearchResultsPage(BasePage):
    def select_first_flight_and_book(self):
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC

        # 1. Hard wait to let MMT's heavy React components finish loading
        time.sleep(5)

        # 2. Dismiss any tutorial overlays if they appear
        try:
            if self.is_element_visible(FlightLocators.OKAY_GOT_IT_BTN):
                self.click_element_js(FlightLocators.OKAY_GOT_IT_BTN)
        except:
            pass

        # 3. Smart Button Clicking Logic
        try:
            # Find the very first button inside the first flight card
            first_card_btn_xpath = "(//div[contains(@class, 'listingCard')])[1]//button"
            first_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, first_card_btn_xpath)))

            # Save the text (e.g., "VIEW PRICES" or "BOOK NOW")
            btn_text = first_btn.text.lower()

            # Click it using our JS fallback
            self.driver.execute_script("arguments[0].click();", first_btn)

            # If the button was "View Prices", an accordion opens, and we must click "Book Now" inside it
            if "view" in btn_text or "price" in btn_text:
                time.sleep(2)  # Wait for accordion to slide down
                book_now_xpath = "(//button[contains(text(), 'Book Now') or contains(text(), 'BOOK NOW')])[1]"
                book_now_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, book_now_xpath)))
                self.driver.execute_script("arguments[0].click();", book_now_btn)

        except Exception as e:
            print(f"Failed to execute booking sequence: {e}")
            raise e

    def apply_non_stop_filter(self):

        time.sleep(3)

        self.click_element_js(FlightLocators.NON_STOP_FILTER)

    def verify_booking_page(self):
        # MMT opens booking in a new tab. Switch to it first.
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        return self.get_text(FlightLocators.REVIEW_PAGE_HEADER)