
import allure
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage
from pages.flight_search_page import FlightSearchPage
from pages.booking_page import BookingPage

# Commented out to prevent crash shown in logs
# from utils.screenshot_util import ScreenshotUtil
from utils.excel_reader import read_excel_data
from utils.logger import LogGen

logger = LogGen.loggen()

booking_data = read_excel_data("BookingData")
passenger_data = read_excel_data("PassengerData")

@allure.feature("E2E Flight Booking")
def test_complete_flight_booking_flow(driver):
    booking = booking_data[0]
    passenger = passenger_data[0]

    logger.info("STARTING E2E FLIGHT BOOKING FLOW")

    home = HomePage(driver)
    flight = FlightSearchPage(driver)
    booking_page = BookingPage(driver)

    # --- Search Flow ---
    home.load("https://www.makemytrip.com")
    home.close_popup()
    home.select_flight_cities(booking["from_city"], booking["to_city"])
    home.select_date(booking["travel_date"])
    home.click_search()

    # --- Results Flow ---
    assert flight.is_results_loaded(), "Flight search results were not displayed"
    flight.apply_non_stop_filter()
    flight.click_view_prices()
    flight.click_book_now()

    # --- Tab Handling ---
    logger.info("Switching driver focus to the newly opened Booking Tab...")
    wait = WebDriverWait(driver, 15)
    wait.until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])

    # --- Booking Page Flow ---
    # 1. Verify Page Load
    assert booking_page.is_loaded(), "Booking page did not load after clicking 'Book Now'"

    # 2. Prepare Data
    passenger_name = passenger.get("passenger_name") #or "Shivam Maurya"
    passenger_email = passenger.get("email") #or "shivam@test.com"
    passenger_mobile = passenger.get("mobile") #or "9876543210"
    first_name, last_name = passenger_name.split(" ", 1) if " " in passenger_name else (passenger_name, "")


    booking_page.click_add_adult()

    # 4. Fill Details
    booking_page.enter_first_name(first_name)
    if last_name:
        booking_page.enter_last_name(last_name)

    booking_page.enter_email(passenger_email)
    booking_page.enter_mobile(passenger_mobile)

    # 5. Final Verification
    assert booking_page.is_contact_section_completed(), "Contact details section was not completed successfully"

    logger.info("E2E FLIGHT BOOKING FLOW COMPLETED SUCCESSFULLY")
