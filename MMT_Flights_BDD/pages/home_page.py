from pages.base_page import BasePage
from locators.flight_locators import HomePageLocators
import time


class HomePage(BasePage):
    def navigate_to(self, url):
        self.driver.get(url)

    def close_popups(self):
        # MMT has aggressive popups. We use a try-except block here.
        try:
            self.click_element(HomePageLocators.POPUP_CLOSE)
        except:
            pass  # No popup appeared

        try:
            # Handle Webklipper ad iframe
            iframe = self.driver.find_element(*HomePageLocators.AD_IFRAME)
            self.driver.switch_to.frame(iframe)
            self.click_element(HomePageLocators.AD_CLOSE)
            self.driver.switch_to.default_content()
        except:
            self.driver.switch_to.default_content()

    def select_trip_type(self, type):
        if type.lower() == "round trip":
            self.click_element(HomePageLocators.ROUND_TRIP_RADIO)
        else:
            self.click_element(HomePageLocators.ONE_WAY_RADIO)

    def enter_source(self, city):
        self.click_element(HomePageLocators.FROM_CITY_INPUT_CLICK)
        self.enter_text(HomePageLocators.FROM_CITY_INPUT_FIELD, city)
        time.sleep(1)  # Wait for dropdown population
        self.click_element(HomePageLocators.FIRST_CITY_SUGGESTION)

    def enter_destination(self, city):
        self.click_element(HomePageLocators.TO_CITY_INPUT_CLICK)
        self.enter_text(HomePageLocators.TO_CITY_INPUT_FIELD, city)
        time.sleep(1)
        self.click_element(HomePageLocators.FIRST_CITY_SUGGESTION)

    def select_tomorrow_date(self):
        self.click_element(HomePageLocators.DEPARTURE_DATE)

    def click_search(self):
        self.click_element(HomePageLocators.SEARCH_BTN)

    def check_same_city_error(self):
        return self.is_element_visible(HomePageLocators.SAME_CITY_ERROR)

    def update_passengers(self):
        self.click_element(HomePageLocators.TRAVELLER_BOX)
        self.click_element(HomePageLocators.ADULTS_2)
        self.click_element(HomePageLocators.APPLY_BTN)