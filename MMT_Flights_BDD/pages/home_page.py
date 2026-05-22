from pages.base_page import BasePage
from locators.flight_locators import FlightLocators
import time

class HomePage(BasePage):
    def close_promotional_popup(self):
        try:
            self.click_element(FlightLocators.POPUP_CLOSE_BTN)
            time.sleep(1)
        except:
            self.logger.info("No promotional popup appeared.")

    def click_flights_section(self):
        self.click_element(FlightLocators.FLIGHTS_MENU_ICON)

    def select_trip_type(self, trip_type):
        if trip_type == "One Way":
            self.click_element(FlightLocators.ONE_WAY_RADIO)
        elif trip_type == "Round Trip":
            self.click_element(FlightLocators.ROUND_TRIP_RADIO)

    def enter_source_city(self, city):
        self.click_element(FlightLocators.FROM_CITY_INPUT)
        time.sleep(0.5)
        self.enter_text(FlightLocators.FROM_CITY_DROPDOWN_INPUT, city)

        self.click_element(FlightLocators.FIRST_SUGGESTION)

    def enter_destination_city(self, city):

        try:
            # If the dropdown input is NOT visible, click the To City box to open it
            element = self.driver.find_element(*FlightLocators.TO_CITY_DROPDOWN_INPUT)
            if not element.is_displayed():
                self.click_element(FlightLocators.TO_CITY_INPUT)
        except:
            self.click_element(FlightLocators.TO_CITY_INPUT)

        self.enter_text(FlightLocators.TO_CITY_DROPDOWN_INPUT, city)
        time.sleep(0.5) 
        self.click_element(FlightLocators.FIRST_SUGGESTION)


    def clear_destination_city(self):
        self.click_element(FlightLocators.TO_CITY_INPUT)
        time.sleep(1) # Just click it to keep it blank


    def click_search(self):
        time.sleep(1)
        # Use the new JS click to bypass the destination dropdown blocking the button
        self.click_element_js(FlightLocators.SEARCH_BUTTON)

    def open_traveller_modal(self):
        self.click_element(FlightLocators.TRAVELLERS_INPUT)

    def select_two_adults(self):
        self.click_element(FlightLocators.ADULT_2_OPTION)

    def click_apply_travellers(self):
        self.click_element(FlightLocators.APPLY_BTN)

    def get_traveller_count(self):
        # Grab text from the whole container instead of the specific child span
        return self.get_text(FlightLocators.TRAVELLERS_INPUT)

    def get_same_city_error(self):
        return self.get_text(FlightLocators.SAME_CITY_ERROR)

    def select_invalid_infant_count(self):
        """Attempts to select 1 Adult and 2 Infants to trigger a validation error"""
        self.click_element(FlightLocators.ADULTS_1)
        self.click_element(FlightLocators.INFANTS_2)
        time.sleep(2)  # Brief pause to allow the error text to render in the DOM

    def is_infant_error_displayed(self):
        return self.is_element_visible(FlightLocators.INFANT_ERROR)