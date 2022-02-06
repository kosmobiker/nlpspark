"""
Various functions to save file
"""
import os
import json
from .logger import get_logger

log = get_logger(__name__)

def save_locally(raw_json: dict, path: str, file_name: str):
    """
    save files locally
    """
    full_path = path + file_name + ".json"
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        with open(full_path, 'w') as f:
            json.dump(raw_json, f)
        log.debug("File sucessfully saved to {}".format(path))
    except:
        log.info("File {} wasn't saved to local storage".format(file_name))
