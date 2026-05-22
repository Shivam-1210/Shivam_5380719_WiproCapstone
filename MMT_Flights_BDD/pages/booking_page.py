from pages.base_page import BasePage
from locators.flight_locators import BookingLocators
import time


class BookingPage(BasePage):

    def switch_to_new_tab(self):
        """MMT opens the review page in a new tab. We must switch to it."""
        time.sleep(3)  # Wait for the tab to spawn
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])

    def handle_review_page_popups(self):
        """Attempts to close common blocking overlays on the review page"""
        import time
        time.sleep(2)  # Give the popup a moment to render if it's going to

        # 1. Try to close the Login/Signup Modal
        try:
            if self.is_element_visible(BookingLocators.LOGIN_MODAL_CLOSE):
                self.click_element_js(BookingLocators.LOGIN_MODAL_CLOSE)
        except:
            pass

        # 2. Try to close the "Are you sure you don't want insurance?" warning
        try:
            if self.is_element_visible(BookingLocators.CONFIRM_NO_INSURANCE_BTN):
                self.click_element_js(BookingLocators.CONFIRM_NO_INSURANCE_BTN)
        except:
            pass

    def decline_insurance(self):
        import time
        # Hard wait to let the dynamic pricing engine load on the new tab
        time.sleep(5)

        self.handle_review_page_popups()

        # 1. Scroll directly to the insurance section so it's visible
        self.scroll_to_element(BookingLocators.INSURANCE_NO_RADIO)

        # 2. Click it
        self.click_element_js(BookingLocators.INSURANCE_NO_RADIO)

        # 3. Handle the confirmation popup that often appears AFTER declining
        self.handle_review_page_popups()

    def enter_passenger_details(self, first_name, last_name):
        import time
        self.handle_review_page_popups()

        # 1. Scroll directly to the Add Adult button
        self.scroll_to_element(BookingLocators.ADD_ADULT_BTN)

        # 2. Click it to open the form (since we know it's closed by default)
        self.click_element_js(BookingLocators.ADD_ADULT_BTN)
        time.sleep(1)  # Wait for the form to expand down

        # 3. Fill the details
        self.click_element_js(BookingLocators.GENDER_MALE)
        self.enter_text(BookingLocators.FIRST_NAME, first_name)
        self.enter_text(BookingLocators.LAST_NAME, last_name)


    def enter_contact_details(self, mobile, email):
        self.enter_text(BookingLocators.MOBILE_NUMBER, mobile)
        self.enter_text(BookingLocators.EMAIL_ADDRESS, email)

    def proceed_to_payment(self):
        # 1. Click main continue button
        self.click_element_js(BookingLocators.CONTINUE_BTN)

        # 2. MMT often throws a "Confirm your details" popup here
        time.sleep(2)
        try:
            if self.is_element_visible(BookingLocators.CONFIRM_DETAILS_BTN):
                self.click_element_js(BookingLocators.CONFIRM_DETAILS_BTN)
        except:
            pass

        # 3. MMT loads the Seat/Meal selection page. We click "Skip to Payment" or "Continue"
        time.sleep(4)
        try:
            self.click_element_js(BookingLocators.SKIP_ADDONS_BTN)
        except:
            pass  # Sometimes it routes directly to payment

    def is_payment_page_loaded(self):
        # We look for the payment options header to confirm we made it to the gateway
        return self.is_element_visible(BookingLocators.PAYMENT_PAGE_HEADER)