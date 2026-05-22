import pytest
import allure
import pandas as pd
from pages.home_page import HomePage
from pages.flight_search_page import FlightSearchPage
from utils.config_reader import get_base_url
from utils.excel_reader import read_excel_data
from utils.logger import LogGen

logger = LogGen.loggen()

# --- Data loading ---
# We keep the raw data from Excel. Pandas/ExcelReader usually returns
# 'travel_date' as a Timestamp object.
raw_data = read_excel_data("PositiveFlights")
test_params = []
for d in raw_data:
    test_params.append((d['from_city'], d['to_city'], d['travel_date'], d['filter_type']))


@allure.feature("Positive Flight Searches")
@pytest.mark.parametrize("from_city, to_city, travel_date, filter_type", test_params)
def test_positive_search_scenarios(driver, from_city, to_city, travel_date, filter_type):
    home = HomePage(driver)
    results = FlightSearchPage(driver)

    # 1. Navigation & Setup
    home.load(get_base_url())

    # Handle the inconsistent popup naming across versions
    if hasattr(home, 'close_popup'):
        home.close_popup()
    else:
        home.dismiss_modal_if_any()

    home.select_flight()
    home.select_one_way()

    # 2. Search Execution
    logger.info(f"Testing Scenario: {filter_type} for {from_city} to {to_city}")
    home.select_flight_cities(from_city, to_city)

    if hasattr(travel_date, 'strftime'):
        formatted_date = travel_date.strftime("%a %b %d %Y").replace(" 0", " ")
    else:
        formatted_date = str(travel_date)

    logger.info(f"Formatted date for locator: {formatted_date}")
    home.select_date(formatted_date)

    home.click_search()

    # 3. Verification & Dynamic Filtering
    assert results.is_results_loaded(), f"Results did not load for {from_city}"

    # Route to the correct filter method based on the 'filter_type' column in Excel
    filter_val = str(filter_type).strip().lower()

    if filter_val == "non_stop":
        logger.info("Applying filter: non_stop")
        results.apply_non_stop_filter()
    elif filter_val == "cheapest":
        logger.info("Applying filter: cheapest")
        results.sort_by_cheapest()
    elif filter_val == "morning":
        logger.info("Applying filter: morning")
        results.apply_morning_filter()
    else:
        # If the Excel value isn't one of the above, treat it as an Airline Name!
        # (e.g., if you wrote "Air India" in Excel, it will pass "Air India" here)
        logger.info(f"Applying airline filter for: {filter_type}")
        results.filter_by_airline(filter_type)

    # 4. Final Assertion
    assert results.verify_results_present(), f"No results visible after applying {filter_type} filter"
    logger.info(f"SUCCESS: Scenario {filter_type} for {from_city} to {to_city} passed.")