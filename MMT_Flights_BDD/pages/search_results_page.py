from pages.base_page import BasePage
from locators.flight_locators import SearchResultsLocators

class SearchResultsPage(BasePage):
    def is_page_loaded(self):
        return self.is_element_visible(SearchResultsLocators.FLIGHT_LIST)

    def apply_non_stop_filter(self):
        self.click_element(SearchResultsLocators.NON_STOP_FILTER)

    def select_first_flight(self):
        self.click_element(SearchResultsLocators.FIRST_FLIGHT_VIEW_FARES)
        self.click_element(SearchResultsLocators.FIRST_FLIGHT_BOOK_NOW)

    def is_review_page_displayed(self):
        # When booking, MMT opens a new tab. We need to switch to it.
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])
        return self.is_element_visible(SearchResultsLocators.REVIEW_PAGE_HEADER)