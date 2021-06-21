from typing import List
import os
import uuid
from datetime import datetime

from src.lib.cloud_storage_providers.adapters.provider_file_response_adapter import ProviderFileResponse
from src.lib.cloud_storage_providers.cloud_storage_provider import get_cloud_storage_provider
from src.background_jobs.celery_background_tasks_wrapper import add_background_job
from src.lib.content_extractor.adapters.content_extractor_response_adapter import ContentExtractorResponse
from src.lib.content_extractor.content_extractor import get_content_extractor
from src.models import File, FileContentMapping
from src.models.files_content import FileContent


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
        for provider_file in provider_files:
            file_record, synced = self.create_or_update_file_record(user_id, provider_file)
            if not synced:
                add_background_job('extract_and_index_content', user_id, self.provider, file_record.id, access_token)
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

    def extract_and_index_content(self, user_id, provider, file_id, access_token):
        file = File.get_by_id(file_id)
        if not file:
            raise Exception("FileNotFound")

        local_filepath, content_fetched_on = self.download_file(file, access_token)

        extraction_response: ContentExtractorResponse = self.extract_content(local_filepath)
        file.mark_sync_status_pending()

        try:
            self.update_content_store(file, extraction_response.content)
        except Exception as e:
            print("Exception: ", e)
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

    def update_content_store(self, file: File, content: str):
        content_mappings = file.file_content_mappings
        content_store_id = content_mappings[0].content_store_id if content_mappings is not None and len(content_mappings) > 0 else None

        print("Contentt Mappings: ", content_mappings)
        if content_store_id is None:
            file_content_object = FileContent(file_id=file.id, content=content)
            file_content_object.meta.id = str(uuid.uuid4())
            file_content_object.save()
            FileContentMapping(file.id, file_content_object.meta.id).save()
        else:
            file_content_object = FileContent.get(id=content_store_id)
            file_content_object.content = content
            file_content_object.save()

        return True

    @staticmethod
    def is_file_synced(file_record, provider_file_response):
        return file_record and file_record.sync_status == 'COMPLETED' and \
               provider_file_response.last_modified_on <= file_record.last_synced_on

