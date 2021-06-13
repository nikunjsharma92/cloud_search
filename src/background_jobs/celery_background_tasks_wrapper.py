from celery_app import celery_app
from src.lib.cloud_storage_providers.dropbox_file_storage import DropboxFileStorage


@celery_app.task
def synchronize(access_token):
    dbx = DropboxFileStorage(access_token)
    dbx.sync()
