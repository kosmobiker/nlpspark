"""
Function to get json files from NewsAPI
"""
import requests
from datetime import datetime, timedelta
from .logger import get_logger


log = get_logger(__name__)


def get_raw_json(
            querry: str,
            periodicity: int,
            newsapi_key: str,
            ) -> dict:
    """
    Function to get info from News API
    """
    from_period = (datetime.now() - timedelta(minutes=periodicity)).strftime("%Y-%m-%YT%H:%M:%S")
    url = ('https://newsapi.org/v2/everything?'
         'q={}&'
         'from={}&'
         'sortBy=popularity&'
         'apiKey={}'.format(querry, from_period, newsapi_key))
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        log.debug("Getting information from NewsAPI...")
        return response.json()
    except requests.exceptions.HTTPError as errh:
        log.error(errh)
    except requests.exceptions.ConnectionError as errc:
        log.error(errc)
    except requests.exceptions.Timeout as errt:
        log.error(errt)
    except requests.exceptions.RequestException as err:
        log.error(err)