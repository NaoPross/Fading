import logging
import sys

formatter = logging.Formatter("[%(name)s] %(levelname)s: %(message)s")
stdout_handler = logging.StreamHandler(sys.stdout)

def get_logger(module):
    log = logging.getLogger(module)

    log.addHandler(stdout_handler)
    stdout_handler.setFormatter(formatter)

    log.setLevel(logging.DEBUG)
    return log
