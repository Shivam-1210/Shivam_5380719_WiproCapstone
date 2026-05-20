import time
import pytest

from pages.home_page import HomePage


class TestNegativeFlights:

    def test_negative_scenarios(self, setup):

        driver = setup

        home = HomePage(driver)

        driver.get("https://www.makemytrip.com")

        time.sleep(5)

       # driver.find_element("tag name", "body").click()

        # Negative Test 1
        # Search without selecting cities

        home.click_search()

        time.sleep(3)

        assert "makemytrip" in driver.current_url

        # Negative Test 2
        # Invalid city

        with pytest.raises(Exception):

            home.select_from_city("XYZINVALIDCITY")