# import logging
# import os
# from datetime import datetime
#
# root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# log_dir = os.path.join(root_dir, "logs")
# os.makedirs(log_dir, exist_ok=True)
#
# log_file = os.path.join(
#     log_dir, f"test_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
# )
#
# class LogGen:
#     @staticmethod
#     def loggen(name: str = "MMT_Flights"):
#         logger = logging.getLogger(name)
#         if logger.handlers:
#             return logger
#
#         logger.setLevel(logging.INFO)
#
#         formatter = logging.Formatter(
#             "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#         )
#
#         ch = logging.StreamHandler()
#         ch.setLevel(logging.INFO)
#         ch.setFormatter(formatter)
#
#         fh = logging.FileHandler(log_file)
#         fh.setLevel(logging.INFO)
#         fh.setFormatter(formatter)
#
#         logger.addHandler(ch)
#         logger.addHandler(fh)
#         logger.propagate = False
#         return logger

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