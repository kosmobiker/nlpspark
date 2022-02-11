"""
this script is used to get the data from NewsAPI
and save it ti specific location
Can be either local storage or S3
"""
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import DEFAULT
from utils.logger import setup_applevel_logger
from utils.config_reader import get_conf
from utils.save_file import save_locally, save_azure


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_CONFIG_FILE = os.path.abspath(os.path.join(ROOT_DIR, "configuration.toml"))

if not os.path.exists('nlpspark/logs'):
    os.makedirs('nlpspark/logs')
date_log_file = (datetime.now()).strftime("%Y-%m-%d")
log = setup_applevel_logger(file_name = f'nlpspark/logs/log_{date_log_file}.log')

conf = get_conf(PATH_TO_CONFIG_FILE)
topic = conf['default']['TOPIC']
periods = conf['default']['PERIODS']
language = conf['default']['LANGUAGE']
news_api_key = conf['default']['NEWS_API_KEY']
querry_params = {'q' : topic, 'apiKey' : news_api_key, 'language': language}
path_to_datalake = os.path.abspath(os.path.join(ROOT_DIR , "..", "datalake"))
container_name = conf['default']['CONTAINER_NAME']

def get_news(p: int, params: dict) -> list:
    """
    p - periodicity - hours
    params - parameters of the GET request

    return list with dictionaries 
    """
    temp = []
    now = (datetime.now() - timedelta(hours=p)).strftime("%Y-%m-%dT%H:%M:%S")
    params['from'] = now
    url = 'https://newsapi.org/v2/everything'
    temp = []
    try:
        response = requests.get(url, params, timeout=10)
        response.raise_for_status()
        log.debug("Getting information from NewsAPI...")
        r = response.json()
        log.info(f"status is {r['status']}")
        if r['status'] == 'ok':
            num_of_pages = r['totalResults'] // 20
            log.debug(f'number of pages is {num_of_pages}')
            for page in range(1, num_of_pages + 1):
                params['page'] = page
                response = requests.get(url, params, timeout=10)
                response.raise_for_status()
                r_data = response.json()
                if len(r_data['articles']) > 0:
                     temp += r_data['articles']
    except requests.exceptions.HTTPError as errh:
        log.error(errh)
    except requests.exceptions.ConnectionError as errc:
        log.error(errc)
    except requests.exceptions.Timeout as errt:
        log.error(errt)
    except requests.exceptions.RequestException as err:
        log.error(err)
    return temp

if __name__ == '__main__':
    data = get_news(periods, querry_params)
    # save_locally(data, path_to_datalake)
    if len(data) > 0:
        save_azure(data, container_name)

