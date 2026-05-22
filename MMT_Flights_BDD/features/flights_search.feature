Feature: MakeMyTrip Flight Search and Booking Module

  Background:
    Given I navigate to the MakeMyTrip homepage
    And I close any promotional popups

  # --- POSITIVE TESTS (4) ---

  Scenario: 1. Positive - Valid One-Way Flight Search
    When I select "One Way" trip
    And I enter "Delhi" as the source city
    And I enter "Mumbai" as the destination city
    And I select tomorrow's date for departure
    And I click on the Search button
    Then I should see the flight search results page

  Scenario: 2. Positive - Valid Round-Trip Flight Search
    When I select "Round Trip"
    And I enter "Delhi" as the source city
    And I enter "Bangalore" as the destination city
    And I select tomorrow's date for departure
    And I select a return date 5 days from now
    And I click on the Search button
    Then I should see the flight search results page

  Scenario: 3. Positive - Change Passenger Count
    When I select "One Way" trip
    And I open the Traveller and Class modal
    And I select 2 Adults
    And I click Apply
    Then the passenger count should update to 2

  Scenario: 4. Positive - Filter flights by Non-Stop
    When I enter "Delhi" as the source city
    And I enter "Mumbai" as the destination city
    And I select tomorrow's date for departure
    And I click on the Search button
    And I apply the "Non-Stop" filter
    Then only non-stop flights should be displayed

  # --- NEGATIVE TESTS (2) ---

  Scenario: 5. Negative - Search with same origin and destination
    When I select "One Way" trip
    And I enter "Delhi" as the source city
    And I enter "Delhi" as the destination city
    Then I should see an error message indicating same cities are not allowed

  Scenario: 6. Negative - Search without destination
    When I select "One Way" trip
    And I clear the destination city
    And I click on the Search button
    Then a validation error should prompt me to enter a destination

  # --- END TO END TEST (1) ---

  Scenario: 7. E2E - Complete flight search and proceed to booking
    When I enter "Delhi" as the source city
    And I enter "Mumbai" as the destination city
    And I select tomorrow's date for departure
    And I click on the Search button
    And I select the first available flight
    And I click on Book Now
    Then I should be navigated to the booking review page