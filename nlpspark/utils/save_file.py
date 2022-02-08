"""
Various functions to save file
"""
import os
import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from .logger import get_logger

log = get_logger(__name__)

def save_locally(data: list, path: str, file_name="news_feed_"):
    """
    save files locally
    """
    full_path = path + os.path.sep + file_name +\
                str(round(datetime.now().timestamp())) + '.json'
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        with open(full_path, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        log.debug("File was sucessfully saved to {}".format(path))
    except Exception as err:
        log.error(err)
        log.info("File wasn't saved to local storage")


def save_azure(data: list, container: str, file_name="news_feed_"):
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = container
        blob_client = blob_service_client.get_blob_client(
                    container=container_name,
                    blob=file_name + str(round(datetime.now().timestamp())) + '.json'
                    )
        output = json.dumps(data, ensure_ascii=False, indent=4).encode('utf8')
        blob_client.upload_blob(output, blob_type="BlockBlob")
        log.debug("File was sucessfully saved to {}".format(container_name))
    except Exception as err:
        log.error(err)
        log.info("File wasn't saved to Azure")
    