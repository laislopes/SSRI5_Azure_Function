import datetime
import logging

import azure.functions as func
from azure.storage.blob import BlobServiceClient

connection_string = "DefaultEndpointsProtocol=https;AccountName=ifsp;AccountKey=T1tm+hcqmaFWXru/JdvczmqSq1Hb4ru/Ozplj8ZC9xwivGPIkdx7KDcEYHGeBoffmDutnQcBZjJC3UVG8HU4ZQ==;EndpointSuffix=core.windows.net"
account_name="ifsp"

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    logging.info('Função backup executada às %s', utc_timestamp)
    copy_azure_files()

def copy_azure_files():

    blob_service = BlobServiceClient.from_connection_string(conn_str=connection_string)

    copy_from_container = 'prod'
    copy_to_container = 'bkp'

    print("\nList blobs in the container")
    container = blob_service.get_container_client(copy_from_container)
 
    list = container.list_blobs()

    for blob in list:
        source_blob = (f"https://{account_name}.blob.core.windows.net/{copy_from_container}/{blob.name}")
        copied_blob = blob_service.get_blob_client(copy_to_container, blob.name)
        copied_blob.start_copy_from_url(source_blob)
        print(blob.name)