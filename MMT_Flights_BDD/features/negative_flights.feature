@negative
Feature: MakeMyTrip Flight Search - Negative Scenarios

  Background:
    Given I navigate to the MakeMyTrip homepage
    And I close any promotional popups
    And I navigate to the Flights section

  Scenario: 5. Negative - Search with same origin and destination
    When I select "One Way" trip
    And I enter "Delhi" as the source city
    And I enter "Delhi" as the destination city
    Then I should see an error message indicating same cities are not allowed

  Scenario: 6. Negative - Select more infants than adults
    When I open the Traveller and Class modal
    And I select 1 Adult
    And I select 2 Infants
    Then I should see an error message regarding infant restrictions