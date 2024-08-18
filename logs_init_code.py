import logging
import sys
import datetime
import os
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "%(message)s "
    green = "\x1b[32;20m"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: green + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def logging_backend_init():
    """Initialize logging with custom formatter."""
    logger = logging.getLogger('backend')
    # ch_ = logging.StreamHandler()
    # ch_.setFormatter(CustomFormatter())
    # logger.addHandler(ch_)
    #current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #fh = logging.FileHandler(f'logs/{current_time}.log')
    logs_name_file = 'logs.log'
    logs_name_dir = 'logs'
    logs_dir_path = f'{os.environ["STATS_DIR"]}scripts/move_send_notebooks/{logs_name_dir}'
    logs_file_path = f'{logs_dir_path}/{logs_name_file}'
    if not os.path.exists(logs_file_path):
        if not os.path.exists(logs_dir_path):
            os.makedirs(logs_dir_path)

        with open(logs_file_path, 'w') as file:
            file.write('')

    fh = logging.FileHandler(logs_file_path)
    fh.setFormatter(CustomFormatter())
    logger.addHandler(fh)
    return logger, fh






backend_logger, ch = logging_backend_init()
