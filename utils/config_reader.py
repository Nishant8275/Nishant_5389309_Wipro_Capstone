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