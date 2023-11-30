import logging


def config_logger():
    # Define a custom log format
    log_format = "%(asctime)s | %(levelname)s | %(message)s"
    date_format = "%d/%m/%y-%H:%M"

    logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=date_format)
