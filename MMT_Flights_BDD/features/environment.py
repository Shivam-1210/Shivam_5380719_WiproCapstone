import configparser
import undetected_chromedriver as uc
import os


def before_scenario(context, scenario):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
    config.read(config_path)

    context.base_url = config.get('Environment', 'base_url')

    # Setup Undetected ChromeDriver
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    # Initialize the undetected driver
    context.driver = uc.Chrome(options=options)
    context.driver.implicitly_wait(config.getint('Environment', 'implicit_wait'))


def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        context.driver.quit()