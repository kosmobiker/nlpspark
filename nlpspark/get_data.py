"""
this script is used to get the data from NewsAPI
and save it ti specific location
Can be either local storage or S3
"""
import os
from datetime import datetime
from unittest.mock import DEFAULT
from utils.logger import setup_applevel_logger
from utils.config_reader import get_conf
from utils.get_raw_json import get_raw_json
from utils.save_file import save_locally


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_CONFIG_FILE = os.path.abspath(os.path.join(ROOT_DIR, "configuration.toml"))
NOW  = datetime.now().timestamp()

log = setup_applevel_logger(file_name = 'logs/test.log')

conf = get_conf(PATH_TO_CONFIG_FILE)
querry = conf['default']['QUERRY']
periods = conf['default']['PERIODS']
news_api_key = conf['default']['NEWS_API_KEY']
path_to_datalake = os.path.abspath(os.path.join(ROOT_DIR , "..", "datalake"))

def get_data(
        querry: str,
        periods: int,
        news_api_key: str,
        path_to_datalake: str,
        ):
    try:
        news_feed = get_raw_json(querry, periods, news_api_key)
        save_locally(news_feed, path_to_datalake, "newsfeed_" + str(round(NOW)))
        return True
    except Exception as err:
        log.error(err)

   







