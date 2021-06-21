from src.lib.cloud_storage_providers.dropbox_file_storage import DropboxCloudStorage


def get_cloud_storage_provider(provider):
    if provider == 'dropbox':
        return DropboxCloudStorage
    else:
        raise Exception("NotImplemented")