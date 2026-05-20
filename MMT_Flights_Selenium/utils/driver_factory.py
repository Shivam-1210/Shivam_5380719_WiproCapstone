from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from utils.config_reader import get_implicit_wait


def get_driver(browser_name: str = "chrome"):
    browser_name = browser_name.strip().lower()

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )
    elif browser_name == "edge":
        options = EdgeOptions()
        options.add_argument("start-maximized")
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options,
        )
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.implicitly_wait(get_implicit_wait())
    return driver