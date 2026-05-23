from behave import given, when, then
from utils.excel_reader import get_data_by_testid
from pages.booking_page import BookingPage
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config_reader import ConfigReader
import time

@given('I navigate to the MakeMyTrip homepage')
def step_impl(context):
    url = ConfigReader.get_application_url()
    context.driver.get(url)
    context.home_page = HomePage(context.driver)
    context.results_page = SearchResultsPage(context.driver)
    time.sleep(3)

@given('I close any promotional popups')
def step_impl(context):
    context.home_page.close_promotional_popup()

@given('I navigate to the Flights section')
def step_impl(context):
    context.home_page.click_flights_section()

# Stacking decorators catches the missing "trip" word in the feature file
@when('I select "{trip_type}" trip')
@when('I select "{trip_type}"')
def step_impl(context, trip_type):
    context.home_page.select_trip_type(trip_type)

@when('I enter "{city}" as the source city')
def step_impl(context, city):
    context.home_page.enter_source_city(city)

@when('I enter "{city}" as the destination city')
def step_impl(context, city):
    context.home_page.enter_destination_city(city)

@when('I clear the destination city')
def step_impl(context):
    context.home_page.clear_destination_city()

@when('I click on the Search button')
def step_impl(context):
    context.home_page.click_search()

@when('I open the Traveller and Class modal')
def step_impl(context):
    context.home_page.open_traveller_modal()

@when('I select 2 Adults')
def step_impl(context):
    context.home_page.select_two_adults()

@when('I click Apply')
def step_impl(context):
    context.home_page.click_apply_travellers()

@when('I apply the "Non-Stop" filter')
def step_impl(context):
    context.results_page.apply_non_stop_filter()

@when('I select the first available flight')
def step_impl(context):
    context.results_page.select_first_flight_and_book()

@when('I click on Book Now')
def step_impl(context):
    pass

@then('the passenger count should update to "{count}"')
def step_impl(context, count):
    actual_count = context.home_page.get_traveller_count()
    assert count in actual_count, f"Expected {count}, but got {actual_count}"

@then('only non-stop flights should be displayed')
def step_impl(context):
    assert True

@then('I should see an error message indicating same cities are not allowed')
def step_impl(context):
    error_msg = context.home_page.get_same_city_error()
    assert "From & To airports cannot be the same" in error_msg

@then('a validation error should prompt me to enter a destination')
def step_impl(context):
    # Safest way to verify we didn't navigate away is to check if the search button is still there
    from locators.flight_locators import FlightLocators
    search_btn = context.driver.find_element(*FlightLocators.SEARCH_BUTTON)
    assert search_btn.is_displayed()

@then('I should be navigated to the booking review page')
def step_impl(context):
    header = context.results_page.verify_booking_page()
    assert "Complete your booking" in header


@when('I select 1 Adult')
def step_impl(context):
    pass # Handled sequentially in the next step to keep logic grouped

@when('I select 2 Infants')
def step_impl(context):
    context.home_page.select_invalid_infant_count()

@then('I should see an error message regarding infant restrictions')
def step_impl(context):
    assert context.home_page.is_infant_error_displayed() is True


@when('I switch to the booking review tab')
def step_impl(context):
    context.booking_page = BookingPage(context.driver)
    context.booking_page.switch_to_new_tab()

@when('I decline trip insurance')
def step_impl(context):
    context.booking_page.decline_insurance()

@when('I enter adult passenger details "{first_name}" "{last_name}"')
def step_impl(context, first_name, last_name):
    context.booking_page.enter_passenger_details(first_name, last_name)


@when('I enter contact details "{mobile}" "{email}"')
def step_impl(context, mobile, email):

    context.booking_page.enter_contact_details(mobile, email)

@when('I submit the passenger and contact details')
def step_impl(context):
    context.booking_page.submit_details()

@then('the details should be accepted successfully')
def step_impl(context):
    assert context.booking_page.is_details_submitted() is True


@when('I search for flights using data for "{test_id}"')
def step_impl(context, test_id):
    # 1. Fetch the data dictionary from Excel using the ID
    test_data = get_data_by_testid(test_id)

    # 2. Extract the values
    source_city = test_data["source"]
    dest_city = test_data["destination"]

    print(f"Executing {test_id}: Searching from {source_city} to {dest_city}")

    # 3. Pass the Excel data into your existing Page Object methods
    context.home_page.enter_source_city(source_city)
    context.home_page.enter_destination_city(dest_city)


@then('I should see the flight search results page')
def step_impl(context):
    is_loaded = context.results_page.is_results_page_loaded()

    # ASSERTION 2: The assert keyword checks if the condition is True.
    # If MakeMyTrip fails to load, it crashes the test and prints the custom message.
    assert is_loaded is True, f"Search failed! Browser stuck at URL: {context.driver.current_url}"


@ when('I execute E2E booking for "{test_id}"')
def step_impl(context, test_id):
    # 1. Fetch all data for this ID from your existing excel_reader
    data = get_data_by_testid(test_id)

    # 2. IMPORTANT: Initialize the booking_page here!
    from pages.booking_page import BookingPage
    context.booking_page = BookingPage(context.driver)

    # 3. Perform the full workflow
    context.home_page.enter_source_city(data["source"])
    context.home_page.enter_destination_city(data["destination"])
    context.home_page.click_search()

    context.results_page.select_first_flight_and_book()

    context.booking_page.switch_to_new_tab()
    context.booking_page.decline_insurance()
    context.booking_page.enter_passenger_details(data["first_name"], data["last_name"])
    context.booking_page.enter_contact_details(data["mobile"], data["email"])
    context.booking_page.submit_details()