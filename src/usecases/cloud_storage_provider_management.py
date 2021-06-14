from src.lib.cloud_storage_providers.cloud_storage_provider import CloudStorageProvider
from src.lib.cloud_storage_providers.dropbox_file_storage import DropboxFileStorage
from src.background_jobs.celery_background_tasks_wrapper import add_background_job


class CloudStorageProviderManagement:
    def authorize(self, user, provider):
        if provider == 'dropbox':
            return CloudStorageProvider(DropboxFileStorage()).authorize(
                consumer_key='5q28gt6qyndwadq',
                consumer_secret='nt7vu3ycirob5db',
                token_access_type='online',
                locale='en'
            )
        else:
            raise Exception("InvalidProvider")

    def authenticate(self, user, provider, code):
        if provider == 'dropbox':
            return CloudStorageProvider(DropboxFileStorage()).authenticate(code)
        else:
            raise Exception("InvalidProvider")

    def start_synchronization(self, user, provider, access_token):
        if provider != 'dropbox':
            raise Exception("InvalidProvider")

        add_background_job('synchronize_files', user.id, provider, access_token)
        return True


    def synchronize_files(self, user_id, provider, access_token):
        csp = CloudStorageProvider(DropboxFileStorage())
        csp.init_client(access_token)
        csp.sync()
        return True
