import allure
from pages.home_page import HomePage
from utils.config_reader import get_base_url


@allure.feature("Smoke")
@allure.story("Homepage opens")
@allure.severity(allure.severity_level.CRITICAL)
def test_homepage_loads(setup):
    driver = setup
    home = HomePage(driver)

    home.load(get_base_url())
    home.take_screenshot("homepage_loaded")

    assert "MakeMyTrip" in driver.title