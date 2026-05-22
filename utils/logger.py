import logging
import os


class Logger:

    @staticmethod
    def get_logger():

        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger("nykaa_automation")
        logger.setLevel(logging.INFO)

        # IMPORTANT: prevent duplicate handlers (pytest runs multiple times)
        if not logger.handlers:

            file_handler = logging.FileHandler("logs/automation.log")
            console_handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger