import configparser
import os

config = configparser.ConfigParser()
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(root_dir, "configurations", "config.ini")
config.read(config_path)


def get_base_url():
    return config.get("default", "base_url").strip()


def get_implicit_wait():
    return config.getint("default", "implicit_wait")


def get_explicit_wait():
    return config.getint("default", "explicit_wait")


def get_default_browser():
    return config.get("browser", "browser").strip().lower()


def get_test_data_file():
    return os.path.join(root_dir, config.get("paths", "test_data_file").strip())