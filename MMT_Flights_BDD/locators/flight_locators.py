from selenium.webdriver.common.by import By


class FlightLocators:
    # Navigation & Popups
    POPUP_CLOSE_BTN = (By.XPATH, "//span[@data-cy='closeModal']")
    FLIGHTS_MENU_ICON = (By.XPATH, "//li[@data-cy='menu_Flights']")

    # Search Elements
    ONE_WAY_RADIO = (By.XPATH, "//li[@data-cy='oneWayTrip']")
    ROUND_TRIP_RADIO = (By.XPATH, "//li[@data-cy='roundTrip']")

    FROM_CITY_INPUT = (By.ID, "fromCity")
    FROM_CITY_DROPDOWN_INPUT = (By.XPATH, "//input[@placeholder='From']")

    TO_CITY_INPUT = (By.ID, "toCity")
    TO_CITY_DROPDOWN_INPUT = (By.XPATH, "//input[@placeholder='To']")

    # NEW: Selects the very first item in the dropdown suggestions
    FIRST_SUGGESTION = (By.XPATH, "//ul[@role='listbox']/li[1]")

    SEARCH_BUTTON = (By.XPATH, "//a[contains(text(), 'Search')]")

    # Passengers
    TRAVELLERS_INPUT = (By.XPATH, "//label[@for='travellers']")
    ADULT_2_OPTION = (By.XPATH, "//li[@data-cy='adults-2']")
    APPLY_BTN = (By.XPATH, "//button[@data-cy='travellerApplyBtn']")

    # Errors
    SAME_CITY_ERROR = (By.XPATH, "//span[@data-cy='sameCityError']")

    NON_STOP_FILTER = (By.XPATH, "//p[contains(text(), 'Non Stop') or contains(text(), 'Non stop')]")

    REVIEW_PAGE_HEADER = (By.XPATH, "//h2[contains(text(), 'Complete your booking')]")

    # Wait for the main flight list container to ensure the page loaded
    FLIGHT_LIST_CONTAINER = (By.XPATH, "//div[contains(@class, 'clusterContent')]")

    # First flight's "View Prices" or "View Fares" button
    FIRST_FLIGHT_VIEW_FARES = (By.XPATH,
                               "(//button[contains(@id, 'bookbutton') or contains(text(), 'View Prices')])[1]")

    # The actual "Book Now" button that appears AFTER clicking View Fares
    FIRST_FLIGHT_BOOK_NOW = (By.XPATH, "(//button[contains(text(), 'Book Now')])[1]")

    # For Scenario 6 (Infant Validation)
    ADULTS_1 = (By.XPATH, "//li[@data-cy='adults-1']")
    INFANTS_2 = (By.XPATH, "//li[@data-cy='infants-2']")
    # MMT usually displays something like "Number of infants cannot be more than adults"
    INFANT_ERROR = (By.XPATH, "//p[contains(text(), 'infant') or contains(text(), 'Infant')]")

    # Sometimes an overlay appears on the search results page ("Okay, Got it!")
    OKAY_GOT_IT_BTN = (By.XPATH, "//button[contains(text(), 'OKAY, GOT IT!')]")


class BookingLocators:

    # Updated to match the screenshot text exactly
    INSURANCE_NO_RADIO = (By.XPATH, "//label[contains(., 'without trip secure') or contains(., 'not opted')]")
    ADD_ADULT_BTN = (By.XPATH, "//button[contains(., '+ ADD NEW ADULT')]")


    GENDER_MALE = (By.XPATH, "//label[@tabindex='0' and contains(., 'MALE')]")
    FIRST_NAME = (By.XPATH, "//input[@placeholder='First & Middle Name']")
    LAST_NAME = (By.XPATH, "//input[@placeholder='Last Name']")

    # Contact Details
    MOBILE_NUMBER = (By.XPATH, "//input[@placeholder='Mobile No']")
    EMAIL_ADDRESS = (By.XPATH, "//input[@placeholder='Email']")

    # Continue Flow
    CONTINUE_BTN = (By.XPATH, "//button[contains(text(), 'Continue')]")
    CONFIRM_DETAILS_BTN = (By.XPATH, "//button[contains(text(), 'CONFIRM')]")
    SKIP_ADDONS_BTN = (By.XPATH, "//button[contains(text(), 'Skip') or contains(text(), 'Proceed to pay')]")

    # Final Validation
    PAYMENT_PAGE_HEADER = (By.XPATH,
                           "//span[contains(text(), 'Payment options') or contains(text(), 'Complete your Payment')]")

    # --- REVIEW PAGE POPUPS ---
    LOGIN_MODAL_CLOSE = (By.XPATH, "//span[contains(@class, 'overlayCrossIcon')] | //span[contains(@class, 'close')]")
    CONFIRM_NO_INSURANCE_BTN = (By.XPATH,
                                 "//button[contains(text(), 'Yes, Please') or contains(text(), 'proceed without')]")

    # Updated to target the clickable label next to the checkbox
    BILLING_CHECKBOX = (By.XPATH, "//label[contains(., 'Confirm and save billing details')]")

    # Matches the button in your second screenshot
    CONFIRM_AND_CONTINUE_MODAL_BTN = (By.XPATH, "//button[contains(., 'Confirm & continue')]")

    # Matches the 'Continue' button on the Add-ons/Seat page (often at the very bottom)
    SEAT_PAGE_CONTINUE_BTN = (By.XPATH,
                              "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'skip')]")