import logging
import os


class Logger:

    @staticmethod
    def get_logger():

        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger("NykaaLogger")
        logger.setLevel(logging.INFO)

        if logger.hasHandlers():
            logger.handlers.clear()

        file_handler = logging.FileHandler("logs/automation.log", mode="a")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger