import logging
import os
from datetime import datetime

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(
    log_dir, f"test_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
)

class LogGen:
    @staticmethod
    def loggen(name: str = "MMT_Flights"):
        logger = logging.getLogger(name)
        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)
        logger.propagate = False
        return logger