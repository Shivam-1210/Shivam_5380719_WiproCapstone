
import logging
import os


class LogGen:
    @staticmethod
    def loggen():
        logger = logging.getLogger()

        # Check if the logger is already set up for this execution run.
        # If it is, just return it so we don't wipe the file again!
        if logger.hasHandlers():
            return logger

        # If it is NOT set up, this is the first time it's being called
        # in the current test execution. Set it up and wipe the old file ('w').
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)

        log_path = os.path.join(log_dir, 'automation.log')

        logging.basicConfig(
            filename=log_path,
            filemode='w',  # Safely wipes the file ONCE at the start of execution
            format='%(asctime)s: %(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            level=logging.INFO,
            force=True
        )

        return logger
