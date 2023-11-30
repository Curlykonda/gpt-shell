import logging

from shell_handler import RestrictedShellHandler


def config_logger():
    # Define a custom log format
    log_format = "%(asctime)s | %(levelname)s | %(message)s"
    date_format = "%d/%m/%y-%H:%M"

    logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=date_format)


def main():

    shell = RestrictedShellHandler(model="gpt-4")
    shell.run()


if __name__ == "__main__":

    config_logger()
    main()
