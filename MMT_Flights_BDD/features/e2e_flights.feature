@e2e
Feature: MakeMyTrip Flight Search - End-to-End Scenarios

  Background:
    Given I navigate to the MakeMyTrip homepage
    And I close any promotional popups
    And I navigate to the Flights section

  Scenario: 7. E2E - Complete flight booking flow up to payment
    When I select "One Way" trip
    And I execute E2E booking for "TC_E2E_01"
    Then the details should be accepted successfully