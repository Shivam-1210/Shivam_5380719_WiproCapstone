@positive
Feature: MakeMyTrip Flight Search - Positive Scenarios

  Background:
    Given I navigate to the MakeMyTrip homepage
    And I close any promotional popups
    And I navigate to the Flights section

  Scenario: 1. Positive - Valid One-Way Flight Search
    When I select "One Way" trip
    And I search for flights using data for "TC_01"
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