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
    full_path = path + os.path.sep + file_name + ".json"
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        with open(full_path, 'w') as f:
            json.dump(raw_json, f, indent=4)
        log.debug("File {} sucessfully saved to {}".format(file_name, path))
    except Exception as err:
        log.error(err)
        log.info("File {} wasn't saved to local storage".format(file_name))

def save_to_s3(raw_json: dict, path: str, file_name: str):
    """
    save files to AWS S3 Bucket
    """
    