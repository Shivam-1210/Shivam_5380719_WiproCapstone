from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.logger import LogGen

logger = LogGen.loggen()


class LoginPage(BasePage):
    LOGIN_BUTTON = (
        By.XPATH,
        "//p[@data-cy='LoginHeaderText']"
    )

    MOBILE_INPUT = (
        By.XPATH,
        "//input[@placeholder='Enter Mobile Number']"
    )

    CONTINUE_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Continue')]"
    )

    PROFILE_ICON = (
        By.XPATH,
        "//div[contains(@class,'loginModal')]"
    )

    def open_website(self, url):

        logger.info("Opening website")

        self.driver.get(url)

        self.driver.maximize_window()

    def close_popup(self):

        try:

            self.driver.find_element(
                By.TAG_NAME,
                "body"
            ).click()

        except:
            pass
    def click_login(self):

        logger.info("Clicking login")

        login_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            login_btn
        )

    def enter_mobile_number(self, mobile):

        logger.info("Entering mobile number")

        mobile_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.MOBILE_INPUT)
        )

        mobile_input.clear()

        mobile_input.send_keys(str(mobile))

    def click_continue(self):

        logger.info("Clicking continue")

        continue_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        )

        continue_btn.click()

    def wait_for_login_success(self):

        logger.info("Waiting for OTP")

        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located(
                self.PROFILE_ICON
            )
        )