import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_logger(name):
    return logging.getLogger(name)