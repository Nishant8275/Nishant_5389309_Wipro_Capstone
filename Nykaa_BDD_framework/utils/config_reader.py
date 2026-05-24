import os
import sys

# Ensure project root is in path (important for behave)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config.config import Config


class ConfigReader:

    @staticmethod
    def get_base_url():
        return Config.BASE_URL

    @staticmethod
    def get_browser():
        return Config.BROWSER

    @staticmethod
    def get_implicit_wait():
        return Config.IMPLICIT_WAIT

    @staticmethod
    def get_explicit_wait():
        return Config.EXPLICIT_WAIT