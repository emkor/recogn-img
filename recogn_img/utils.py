import logging
import time

LOG_NAME = "recogn-img"
TENSORFLOW_LOG_NAME = "tensorflow"


def setup_log(verbose: bool = False):
    log_format = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.INFO if not verbose else logging.DEBUG,
                        format=log_format)
    logging.Formatter.converter = time.gmtime
    tf_log = logging.getLogger(TENSORFLOW_LOG_NAME)
    tf_log.setLevel(logging.ERROR if not verbose else logging.INFO)


def get_log():
    return logging.getLogger(LOG_NAME)
