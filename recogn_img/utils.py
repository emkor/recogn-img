import json
import logging
import os
import time
from typing import List, Dict, Any

LOG_NAME = "recogn-img"
TENSORFLOW_LOG_NAME = "tensorflow"


def setup_log(verbose: bool = False):
    logging.basicConfig(level=logging.INFO if not verbose else logging.DEBUG,
                        format="%(asctime)s.%(msecs)03d|%(levelname)-7s| %(message)s",
                        datefmt="%Y-%m-%dT%H:%M:%S")
    logging.Formatter.converter = time.gmtime
    tf_log = logging.getLogger(TENSORFLOW_LOG_NAME)
    tf_log.setLevel(logging.ERROR if not verbose else logging.INFO)


def get_log():
    return logging.getLogger(LOG_NAME)


def get_file_paths_from(dir_path: str) -> List[str]:
    return [os.path.join(dir_path, p) for p in os.listdir(dir_path)
            if os.path.isfile(os.path.join(dir_path, p))]


def read_classes(classes_file: str) -> List[str]:
    with open(classes_file) as f_:
        class_names = f_.readlines()
    return [c.strip() for c in class_names]


def read_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as in_file:
        return json.load(in_file)


def write_json(content: Dict[str, Any], file_path: str) -> None:
    with open(file_path, "w") as out_file:
        json.dump(content, out_file)
