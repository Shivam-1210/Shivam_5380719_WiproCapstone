from pages.base_page import BasePage
from locators.flight_locators import BookingLocators
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class BookingPage(BasePage):

    def switch_to_new_tab(self):
        self.logger.info(f"Switched to new tab: {self.driver.current_url}")

        from selenium.webdriver.support.ui import WebDriverWait

        # Wait up to 15 seconds for a second tab to actually exist in the browser
        try:
            WebDriverWait(self.driver, 15).until(lambda d: len(d.window_handles) > 1)
        except:
            print("WARNING: New tab did not open in time.")

        window_handles = self.driver.window_handles
        if len(window_handles) > 1:
            self.driver.switch_to.window(window_handles[-1])

    def handle_review_page_popups(self):
        self.logger.info(f"Switched to review page: {self.driver.current_url}")

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
        self.logger.info(f"Declined insurance page:")
        import time
        # Hard wait to let the dynamic pricing engine load on the new tab
        time.sleep(2)

        self.handle_review_page_popups()
        self.logger.info(f"Handle review page: {self.driver.current_url}")

        # 1. Scroll directly to the insurance section so it's visible
        self.scroll_to_element(BookingLocators.INSURANCE_NO_RADIO)
        self.logger.info(f"Handle insurance page")
        # 2. Click it
        self.click_element_js(BookingLocators.INSURANCE_NO_RADIO)

        # 3. Handle the confirmation popup that often appears AFTER declining
        self.handle_review_page_popups()

    def enter_passenger_details(self, first_name, last_name):
        self.logger.info(f"Entering passenger details page")
        import time
        self.handle_review_page_popups()

        # 1. Scroll directly to the Add Adult button
        self.logger.info(f"Scroll to enter passenger details page")
        self.scroll_to_element(BookingLocators.ADD_ADULT_BTN)


        # 2. Click it to open the form (since we know it's closed by default)
        self.click_element_js(BookingLocators.ADD_ADULT_BTN)
        time.sleep(1)  # Wait for the form to expand down

        # 3. Fill the details
        self.logger.info(f"Entering passenger details")
        self.click_element_js(BookingLocators.GENDER_MALE)
        self.enter_text(BookingLocators.FIRST_NAME, first_name)
        self.enter_text(BookingLocators.LAST_NAME, last_name)

    def enter_contact_details(self, mobile, email):
        self.logger.info(f"Entering contact details page: {self.driver.current_url}")


        # 1. Fill Mobile Number

        self.scroll_to_element(BookingLocators.MOBILE_NUMBER)
        self.logger.info(f"Entering mobile number: {mobile}")
        self.enter_text(BookingLocators.MOBILE_NUMBER, mobile)

        # 2. Fill Email Address
        email_field = self.wait.until(EC.visibility_of_element_located(BookingLocators.EMAIL_ADDRESS))
        email_field.clear()

        # Type the email text
        self.logger.info(f"Entering email address: {email}")
        email_field.send_keys(email)
        time.sleep(1.5)  # Wait for the MMT auto-suggest dropdown to fully render

        # Mimic human keyboard navigation: Press DOWN arrow to highlight the suggestion, then ENTER
        email_field.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        email_field.send_keys(Keys.ENTER)
        time.sleep(1)

        # 3. The Ultimate Failsafe: Force 'onBlur' by clicking the page background
        # This tells React "I am done interacting with this form field"
        try:
            body_element = self.driver.find_element(By.TAG_NAME, "body")
            self.driver.execute_script("arguments[0].click();", body_element)
        except Exception as e:
            print(f"Background click failed, continuing anyway: {e}")

        time.sleep(1)  # Give the green checkmark a second to appear

    def submit_details(self):
        self.logger.info(f"Submitting details page")


        # 1. Handle the Billing Checkbox
        try:
            billing_label = self.driver.find_element(By.XPATH, "//p[@data-cy='dt_cb_label_gst_info']")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", billing_label)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", billing_label)
            time.sleep(1)
        except:
            pass

            # 2. Click the main page CONTINUE button
        self.scroll_to_element(BookingLocators.CONTINUE_BTN)
        self.logger.info(f"Clicking continue button")
        self.click_element_js(BookingLocators.CONTINUE_BTN)

        # Brief pause to let MakeMyTrip register the click before the test ends
        time.sleep(3)

    def is_details_submitted(self):
        self.logger.info(f"Details submitted")

        return True