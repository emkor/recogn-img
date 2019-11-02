from os import path

PROJ_DIR_NAME = "recogn-img/"


def get_proj_file_path(rel_path: str) -> str:
    parent, proj_dir, _ = path.realpath(__file__).partition(PROJ_DIR_NAME)
    return path.abspath(path.join(parent, proj_dir, rel_path))
