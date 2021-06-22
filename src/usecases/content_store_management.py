from typing import List
import uuid

from src.adapters.output_adapters.search_output_adapter import SearchResultOutputAdapter
from src.lib.cloud_storage_providers.cloud_storage_provider import get_cloud_storage_provider
from src.models import File, FileContentMapping
from src.models.files_content import FileContent


class ContentStoreManagement():
    def __init__(self):
        pass

    def update_content_store(self, file: File, content: str):
        content_mappings = file.file_content_mappings
        content_store_id = content_mappings[0].content_store_id if content_mappings is not None and len(content_mappings) > 0 else None

        if content_store_id is None:
            file_content_object = FileContent(file_id=file.id, content=content, user_id=file.user_id)
            file_content_object.meta.id = str(uuid.uuid4())
            file_content_object.save()
            FileContentMapping(file.id, file_content_object.meta.id, file.user_id).save()
        else:
            file_content_object = FileContent.get(id=content_store_id)
            file_content_object.content = content
            file_content_object.user_id = file.user_id
            file_content_object.save()

        return True

    def search(self, user, query) -> List[SearchResultOutputAdapter]:
        search_results = FileContent().search_content(user.id, query)
        results = []
        for result in search_results:
            file = File.get_by_id(result.file_id)
            file_url = get_cloud_storage_provider(file.provider)().get_file_url(file.filepath)
            results.append(SearchResultOutputAdapter(file.id, file.filepath, file.provider_file_id, file.provider, file_url))

        return results


