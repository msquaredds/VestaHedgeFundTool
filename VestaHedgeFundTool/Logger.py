"""
Define class for logging.

:class: Logger: Set up the logger to use in the project.
"""

import logging
import time


class Logger(object):
    """Set up the logger to use in the project."""

    def __init__(self) -> None:
        # Upon instantiation, set logging level first as this isn't
        # working later on and create custom logger
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('main_logger')

        # Create handlers and set level to info
        date_suffix = time.strftime("%Y%m%d-%H%M%S")
        log_file_name = "VestaHedgeFundTool/Logs/log_file_" + date_suffix + \
                        ".log"
        f_handler = logging.FileHandler(log_file_name)
        f_handler.setLevel(logging.INFO)

        # Create formatters
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s '
                                     '- %(message)s')
        f_handler.setFormatter(f_format)

        # Add to logger
        self.logger.addHandler(f_handler)
