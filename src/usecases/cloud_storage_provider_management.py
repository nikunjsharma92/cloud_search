from typing import List
from datetime import datetime

from src.lib.cloud_storage_providers.adapters.provider_file_response_adapter import ProviderFileResponse
from src.lib.cloud_storage_providers.cloud_storage_provider import get_cloud_storage_provider
from src.background_jobs.celery_background_tasks_wrapper import add_background_job
from src.lib.content_extractor.adapters.content_extractor_response_adapter import ContentExtractorResponse
from src.lib.content_extractor.content_extractor import get_content_extractor
from src.models import File
from src.usecases.content_store_management import ContentStoreManagement


class CloudStorageProviderManagement:
    def __init__(self, provider):
        self.cloud_storage_provider = get_cloud_storage_provider(provider)()
        self.provider = provider

    def authorize(self):
        return self.cloud_storage_provider.authorize()

    def authenticate(self, code):
        return self.cloud_storage_provider.authenticate(code)

    def start_synchronization(self, user, provider, access_token):
        add_background_job('synchronize_files', user.id, provider, access_token)
        return True

    def synchronize_files(self, user_id, access_token):
        self.cloud_storage_provider.init_client(access_token)
        provider_files: List[ProviderFileResponse] = self.cloud_storage_provider.get_file_list()
        # TODO: get deleted file list and mark them inactive, remove content
        for provider_file in provider_files:
            add_background_job('extract_and_index_content', user_id, self.provider, provider_file.__dict__, access_token)
        return True

    def create_or_update_file_record(self, user_id: int, provider_file_response: ProviderFileResponse):
        file = File.get_by_provider_id(provider_file_response.provider_id)
        if file and self.is_file_synced(file, provider_file_response):
            return file, True

        if not file:
            file = File.create_file_record(user_id, provider_file_response)
        else:
            file.update_file_record(provider_file_response)

        return file, False

    def extract_and_index_content(self, user_id, provider, provider_file_response, access_token):
        provider_file = ProviderFileResponse(**provider_file_response)

        file, synced = self.create_or_update_file_record(user_id, provider_file)

        if synced:
            return True

        if file.size_bytes >= 200 * 1000:  # allows 10k parallel ops on 2GB free mem
            file.mark_sync_status_failed()
            return False

        local_filepath, content_fetched_on = self.download_file(file, access_token)
        try:
            # TODO: split file on disk into pages to allow more parallelization
            extraction_response: ContentExtractorResponse = self.extract_content(local_filepath)
            file.mark_sync_status_pending()
            ContentStoreManagement().update_content_store(file, extraction_response.content)
        except Exception as e:
            print("Exception:", e)
            file.mark_sync_status_failed()
            return False

        file.mark_sync_status_completed(content_fetched_on)
        return True

    def download_file(self, file: File, access_token):
        self.cloud_storage_provider.init_client(access_token)
        content_fetched_on = datetime.utcnow()
        downloaded_file_path = self.cloud_storage_provider.download_file_content(file.filepath)
        return downloaded_file_path, content_fetched_on

    def extract_content(self, filepath) -> ContentExtractorResponse:
        return get_content_extractor()().extract_from_file(filepath)

    @staticmethod
    def is_file_synced(file_record, provider_file_response):
        return file_record and file_record.last_sync_status == 'COMPLETED' and \
               provider_file_response.last_modified_on <= file_record.last_synced_on

