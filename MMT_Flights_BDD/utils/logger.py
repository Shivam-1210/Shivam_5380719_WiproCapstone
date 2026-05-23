import logging
import os


class LogGen:
    @staticmethod
    def loggen():
        # Ensures the 'logs' directory exists
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)

        log_path = os.path.join(log_dir, 'automation.log')

        logging.basicConfig(
            filename=log_path,
            filemode='w',
            format='%(asctime)s: %(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            level=logging.INFO,
            force=True
        )

        return logging.getLogger()
