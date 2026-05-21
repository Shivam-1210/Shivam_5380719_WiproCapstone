import pytest
import time
import allure
import logging
from pages.home_page import HomePage
from utils.config_reader import get_base_url

logger = logging.getLogger("MMT_Flights")


@allure.feature("Negative Flight Searches")
@pytest.mark.parametrize("from_city, to_city, adults, infants, expected_error", [
    ('Mumbai', 'Mumbai', 1, 0, 'cannot be the same'),
    ('Delhi', 'Bangalore', 1, 2, 'Number of infants cannot be more than adults')
])
def test_negative_scenarios(driver, from_city, to_city, adults, infants, expected_error):
    home = HomePage(driver)

    logger.info(f"--- Starting Negative Test: {from_city} to {to_city} ---")
    driver.get(get_base_url())
    home.dismiss_modal_if_any()  # Ensure this is robust as shown above

    home.select_flight()
    #home.select_flight_mode()
    home.select_one_way()

    home.select_flight_cities(from_city, to_city)

    # 2. Enter Passengers
    home.select_passengers(adults, infants)


    time.sleep(2)
    actual_error = home.get_ui_error_message()

    # Cleaning for logs
    safe_log_error = actual_error.replace('\n', ' ').encode('ascii', 'ignore').decode('ascii')
    logger.info(f"Captured UI Text: {safe_log_error}")

    # 4. Assert
    assert expected_error.lower() in actual_error.lower(), \
        f"Expected '{expected_error}' but found: {safe_log_error}"

    logger.info("========== TEST PASSED ==========")