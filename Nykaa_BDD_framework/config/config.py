import os
import configparser


class Config:

    # Get project root path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Path to config.ini
    CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.ini")

    # Read config file
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    # DEFAULT values (from config.ini)
    BASE_URL = config.get("DEFAULT", "BASE_URL", fallback="https://www.nykaa.com")
    BROWSER = config.get("DEFAULT", "BROWSER", fallback="chrome")

    # Convert string → int safely
    IMPLICIT_WAIT = config.getint("DEFAULT", "IMPLICIT_WAIT", fallback=10)
    EXPLICIT_WAIT = config.getint("DEFAULT", "EXPLICIT_WAIT", fallback=20)