
import logging
import os


class LogGen:
    @staticmethod
    def loggen():
        # Ensure the logs directory exists
        if not os.path.exists("logs"):
            os.makedirs("logs")

        logger = logging.getLogger("MMT_Flights")

        # If the logger already has handlers, don't add more (prevents duplicate lines)
        if not logger.handlers:
            # Set this to a static name, and use filemode='w' to overwrite it every run
            fileHandler = logging.FileHandler('logs/automation.log', mode='w')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
            logger.setLevel(logging.INFO)

        return logger