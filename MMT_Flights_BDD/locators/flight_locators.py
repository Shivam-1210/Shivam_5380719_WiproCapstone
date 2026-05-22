from selenium.webdriver.common.by import By


class HomePageLocators:
    POPUP_CLOSE = (By.XPATH, "//span[@data-cy='closeModal']")
    AD_IFRAME = (By.XPATH, "//iframe[contains(@id, 'webklipper')]")
    AD_CLOSE = (By.XPATH, "//a[@class='close']")

    ONE_WAY_RADIO = (By.XPATH, "//li[@data-cy='oneWayTrip']")
    ROUND_TRIP_RADIO = (By.XPATH, "//li[@data-cy='roundTrip']")

    FROM_CITY_INPUT_CLICK = (By.XPATH, "//input[@id='fromCity']")
    FROM_CITY_INPUT_FIELD = (By.XPATH, "//input[@placeholder='From']")
    FIRST_CITY_SUGGESTION = (By.XPATH, "//li[contains(@id,'react-autowhatever-1-section-0-item-0')]")

    TO_CITY_INPUT_CLICK = (By.XPATH, "//input[@id='toCity']")
    TO_CITY_INPUT_FIELD = (By.XPATH, "//input[@placeholder='To']")

    DEPARTURE_DATE = (By.XPATH, "//div[contains(@class, 'DayPicker-Day--today')]/following-sibling::div[1]")  # Tomorrow

    TRAVELLER_BOX = (By.XPATH, "//label[@for='travellers']")
    ADULTS_2 = (By.XPATH, "//li[@data-cy='adults-2']")
    APPLY_BTN = (By.XPATH, "//button[@data-cy='travellerApplyBtn']")

    SEARCH_BTN = (By.XPATH, "//a[contains(@class, 'widgetSearchBtn')]")
    SAME_CITY_ERROR = (By.XPATH, "//span[contains(@class, 'sameCityError')]")


class SearchResultsLocators:
    NON_STOP_FILTER = (By.XPATH, "//p[text()='Non Stop']/ancestor::label//input")
    FLIGHT_LIST = (By.XPATH, "//div[contains(@class, 'listingCard')]")
    FIRST_FLIGHT_VIEW_FARES = (By.XPATH, "(//button[contains(@id, 'bookbutton')])[1]")
    FIRST_FLIGHT_BOOK_NOW = (By.XPATH, "(//button[text()='Book Now'])[1]")
    REVIEW_PAGE_HEADER = (By.XPATH, "//h2[contains(text(), 'Review your booking')]")