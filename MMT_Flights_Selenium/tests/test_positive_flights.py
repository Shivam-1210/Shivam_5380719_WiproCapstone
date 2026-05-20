import pytest
import allure

from pages.home_page import HomePage
from pages.flight_search_page import FlightSearchPage
from utils.config_reader import get_base_url
from utils.excel_reader import read_excel_data

test_data = read_excel_data("PositiveFlights")


@allure.feature("Flights")
@allure.story("Positive flight search")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "from_city,to_city,trip_type,departure_offset_days,expected_result",
    test_data
)
def test_search_flights_positive(
    setup,
    from_city,
    to_city,
    trip_type,
    departure_offset_days,
    expected_result
):
    driver = setup
    home = HomePage(driver)
    results = FlightSearchPage(driver)

    home.load(get_base_url())


    if trip_type.lower() == "oneway":
        home.select_one_way()

    home.select_from_city(from_city)
    home.select_to_city(to_city)


    home.select_departure_date(departure_offset_days)

    home.take_screenshot("before_search")
    home.click_search()


    home.take_screenshot("after_search")

    assert "/flight/search" in driver.current_url.lower(), f"Search did not navigate correctly: {driver.current_url}"
    assert results.is_results_loaded(), f"Results not loaded for {from_city} to {to_city}"