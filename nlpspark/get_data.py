"""
this script is used to get the data from NewsAPI
and save it ti specific location
Can be either local storage or S3
"""
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import DEFAULT
from utils.logger import setup_applevel_logger
from utils.config_reader import get_conf
from utils.get_raw_json import get_raw_json
from utils.save_file import save_locally, save_azure


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_CONFIG_FILE = os.path.abspath(os.path.join(ROOT_DIR, "configuration.toml"))

log = setup_applevel_logger(file_name = 'logs/test.log')

conf = get_conf(PATH_TO_CONFIG_FILE)
topic = conf['default']['TOPIC']
periods = conf['default']['PERIODS']
language = conf['default']['LANGUAGE']
pages = conf['default']['PAGES']
news_api_key = conf['default']['NEWS_API_KEY']
querry_params = {'q' : topic, 'apiKey' : news_api_key, 'language': language}
path_to_datalake = os.path.abspath(os.path.join(ROOT_DIR , "..", "datalake"))
container_name = conf['default']['CONTAINER_NAME']

def get_news(
        n: int,
        p: int,
        params: dict
        ) -> list:
    """
    n - number of pages
    p - periodicity - hours
    params - parameters of the GET request

    return Pandas Dataframe 
    """
    temp = []
    now = (datetime.now() - timedelta(hours=p)).strftime("%Y-%m-%dT%H:%M:%S")
    params['from'] = now
    try:
        for i in range(1, n + 1):
            params['page'] = i
            r = get_raw_json(params).json()['articles']
            temp += r
    except Exception as err:
        log.error(err)
    finally:
        return temp

if __name__ == '__main__':
    data = get_news(pages, periods, querry_params)
    save_locally(data, path_to_datalake)
    save_azure(data, container_name)
    


   







