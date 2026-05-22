Feature: MakeMyTrip Flight Search and Booking Module

  Background:
    Given I navigate to the MakeMyTrip homepage
    And I close any promotional popups
    And I navigate to the Flights section

  # --- POSITIVE SCENARIOS (4) ---

  Scenario: 1. Positive - Valid One-Way Flight Search
    When I select "One Way" trip
    And I enter "Delhi" as the source city
    And I enter "Mumbai" as the destination city
    And I click on the Search button
    Then I should see the flight search results page

  Scenario: 2. Positive - Valid Round-Trip Flight Search
    When I select "Round Trip"
    And I enter "Delhi" as the source city
    And I enter "Bangalore" as the destination city
    And I click on the Search button
    Then I should see the flight search results page

  Scenario: 3. Positive - Change Passenger Count
    When I open the Traveller and Class modal
    And I select 2 Adults
    And I click Apply
    Then the passenger count should update to "2"

  Scenario: 4. Positive - Filter flights by Non-Stop
    When I enter "Delhi" as the source city
    And I enter "Mumbai" as the destination city
    And I click on the Search button
    And I apply the "Non-Stop" filter
    Then only non-stop flights should be displayed

  # --- NEGATIVE SCENARIOS (2) ---

  Scenario: 5. Negative - Search with same origin and destination
    When I select "One Way" trip
    And I enter "Delhi" as the source city
    And I enter "Delhi" as the destination city
    Then I should see an error message indicating same cities are not allowed

  Scenario: 6. Negative - Select more infants than adults
    Given I navigate to the MakeMyTrip homepage
    And I close any promotional popups
    And I navigate to the Flights section
    When I open the Traveller and Class modal
    And I select 1 Adult
    And I select 2 Infants
    Then I should see an error message regarding infant restrictions

  # --- END-TO-END SCENARIO (1) ---

  Scenario: 7. E2E - Complete flight booking flow up to payment
    Given I navigate to the MakeMyTrip homepage
    And I close any promotional popups
    And I navigate to the Flights section
    When I enter "Delhi" as the source city
    And I enter "Mumbai" as the destination city
    And I click on the Search button
    And I select the first available flight
    And I click on Book Now
    And I switch to the booking review tab
    And I decline trip insurance
    And I enter adult passenger details "Shivam" "Maurya"
    And I enter contact details "9876543216" "testbdd@gmail.com"
    And I click continue and skip all add-ons
    Then I should reach the final payment page