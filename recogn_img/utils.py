import logging
import os
import time
from typing import List

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


def get_file_paths_from(dir_path: str) -> List[str]:
    return [os.path.join(dir_path, p) for p in os.listdir(dir_path)
            if os.path.isfile(p)]


def read_classes(classes_file: str) -> List[str]:
    with open(classes_file) as f_:
        class_names = f_.readlines()
    return [c.strip() for c in class_names]
