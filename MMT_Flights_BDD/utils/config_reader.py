import configparser
import os


class ConfigReader:
    config = configparser.ConfigParser()
    # Correctly locates the config.ini file regardless of where you run 'behave' from
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
    config.read(config_path)

    @staticmethod
    def get_application_url():

        return ConfigReader.config.get("basic info", "url")

    @staticmethod
    def get_implicit_wait():

        return int(ConfigReader.config.get("basic info", "implicit_wait"))

    @staticmethod
    def get_explicit_wait():

        return int(ConfigReader.config.get("basic info", "explicit_wait"))