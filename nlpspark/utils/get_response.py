"""
Function to get json files from NewsAPI
"""
import requests
from datetime import datetime, timedelta
from .logger import get_logger


log = get_logger(__name__)


def get_response(query_params: dict):
    """
    Function to get info from News API
    """
    url = 'https://newsapi.org/v2/everything'
    try:
        response = requests.get(url, params=query_params, timeout=10)
        response.raise_for_status()
        log.debug("Getting information from NewsAPI...")
        return response
    except requests.exceptions.HTTPError as errh:
        log.error(errh)
    except requests.exceptions.ConnectionError as errc:
        log.error(errc)
    except requests.exceptions.Timeout as errt:
        log.error(errt)
    except requests.exceptions.RequestException as err:
        log.error(err)