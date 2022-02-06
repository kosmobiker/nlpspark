"""
this is a config reader
It read toml files
"""
import toml
from .logger import get_logger

log = get_logger(__name__)

def get_conf(path: str) -> dict:
    """
    Function to read config files
    Arguments:
        path (str): path to configuration file in toml format
    Returns:
        dictionary with parameters
    """
    try:
        log.info('Reading of configuration file')
        return toml.load(path)
    except FileNotFoundError:
        log.error('Configuration file has not been read')
