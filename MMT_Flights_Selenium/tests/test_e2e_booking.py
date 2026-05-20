# import allure
#
# from pages.home_page import HomePage
# from pages.flight_search_page import FlightSearchPage
# from pages.booking_page import BookingPage
#
# #from utils.screenshot_util import ScreenshotUtil
# from utils.excel_reader import ExcelReader
# from utils.logger import LogGen
#
# logger = LogGen.loggen()
#
# booking_data = ExcelReader.read_excel("test_data/passenger_data.xlsx", "BookingData")
# passenger_data = ExcelReader.read_excel("test_data/passenger_data.xlsx", "PassengerData")
#
#
# @allure.feature("E2E Flight Booking")
# def test_complete_flight_booking_flow(driver):
#     booking = booking_data[0]
#     passenger = passenger_data[0]
#
#     logger.info("STARTING E2E FLIGHT BOOKING FLOW")
#
#     home = HomePage(driver)
#     flight = FlightSearchPage(driver)
#     booking_page = BookingPage(driver)
#
#     home.load("https://www.makemytrip.com")
#     home.close_popup()
#     home.select_flight()
#     home.select_one_way()
#
#     assert "MakeMyTrip" in driver.title, f"Homepage title did not contain expected text; title was: {driver.title}"
#
#
#     home.select_flight_cities(booking["from_city"], booking["to_city"])
#
#     # Pass the travel date from your Excel data
#     home.select_date(booking["travel_date"])
#
#     home.click_search()
#
#     assert flight.is_results_loaded(), "Flight search results were not displayed after clicking search"
#
#     flight.apply_non_stop_filter()
#
#     flight.click_view_prices()
#
#     assert flight.is_results_loaded(), "Flight booking page were not displayed after clicking view prices"
#
#     flight.click_book_now()
#
#     assert booking_page.is_loaded(), "Booking page did not load after clicking 'Book Now'"
#
#     passenger_name = passenger.get("passenger_name") or "Shivam Maurya"
#     passenger_email = passenger.get("email") or "shivam@test.com"
#     passenger_mobile = passenger.get("mobile") or "9876543210"
#
#     first_name, last_name = passenger_name.split(" ", 1) if " " in passenger_name else (passenger_name, "")
#
#     booking_page.enter_first_name(first_name)
#     if last_name:
#         booking_page.enter_last_name(last_name)
#     booking_page.enter_email(passenger_email)
#     booking_page.enter_mobile(passenger_mobile)
#
#     assert booking_page.is_contact_section_completed(), "Contact details were not accepted or next section did not appear"
#
#     logger.info("E2E FLIGHT BOOKING FLOW COMPLETED UP TO FINAL CONFIRMATION STEP")

#----------------------------------------------------------------------------------------------------------


import allure
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage
from pages.flight_search_page import FlightSearchPage
from pages.booking_page import BookingPage

# Commented out to prevent crash shown in logs
# from utils.screenshot_util import ScreenshotUtil
from utils.excel_reader import ExcelReader
from utils.logger import LogGen

logger = LogGen.loggen()

booking_data = ExcelReader.read_excel("test_data/passenger_data.xlsx", "BookingData")
passenger_data = ExcelReader.read_excel("test_data/passenger_data.xlsx", "PassengerData")

@allure.feature("E2E Flight Booking")
def test_complete_flight_booking_flow(driver):
    booking = booking_data[0]
    passenger = passenger_data[0]

    logger.info("STARTING E2E FLIGHT BOOKING FLOW")

    home = HomePage(driver)
    flight = FlightSearchPage(driver)
    booking_page = BookingPage(driver)

    home.load("https://www.makemytrip.com")
    home.close_popup()
    home.select_flight()
    home.select_one_way()

    assert "MakeMyTrip" in driver.title, f"Homepage title did not contain expected text; title was: {driver.title}"

    home.select_flight_cities(booking["from_city"], booking["to_city"])

    # Pass the travel date from your Excel data
    home.select_date(booking["travel_date"])

    home.click_search()

    assert flight.is_results_loaded(), "Flight search results were not displayed after clicking search"

    flight.apply_non_stop_filter()
    flight.click_view_prices()
    flight.click_book_now()

    # ---------------------------------------------------------
    # NEW TAB HANDLING: MMT opens the booking page in a new tab
    # ---------------------------------------------------------
    logger.info("Switching driver focus to the newly opened Booking Tab...")
    wait = WebDriverWait(driver, 15)
    wait.until(lambda d: len(d.window_handles) > 1)  # Wait for the 2nd tab to exist

    handles = driver.window_handles
    driver.switch_to.window(handles[-1])  # Switch to the most recently opened tab
    logger.info(f"Switched successfully. Current URL: {driver.current_url}")
    # ---------------------------------------------------------

    assert booking_page.is_loaded(), "Booking page did not load after clicking 'Book Now'"

    passenger_name = passenger.get("passenger_name") or "Shivam Maurya"
    passenger_email = passenger.get("email") or "shivam@test.com"
    passenger_mobile = passenger.get("mobile") or "9876543210"

    first_name, last_name = passenger_name.split(" ", 1) if " " in passenger_name else (passenger_name, "")

    booking_page.enter_first_name(first_name)
    if last_name:
        booking_page.enter_last_name(last_name)
    booking_page.enter_email(passenger_email)
    booking_page.enter_mobile(passenger_mobile)

    assert booking_page.is_contact_section_completed(), "Contact details were not accepted or next section did not appear"

    logger.info("E2E FLIGHT BOOKING FLOW COMPLETED UP TO FINAL CONFIRMATION STEP")