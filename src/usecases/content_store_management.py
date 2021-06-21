from typing import List

from src.adapters.output_adapters.search_output_adapter import SearchResultOutputAdapter
from src.lib.cloud_storage_providers.cloud_storage_provider import get_cloud_storage_provider
from src.models import File
from src.models.files_content import FileContent


class ContentStoreManagement():
    def __init__(self):
        pass

    def search(self, query) -> List[SearchResultOutputAdapter]:
        search_results = FileContent().search_content(query)
        results = []
        for result in search_results:
            file = File.get_by_id(result.file_id)
            file_url = get_cloud_storage_provider(file.provider)().get_file_url(file.filepath)
            results.append(SearchResultOutputAdapter(file.id, file.filepath, file.provider_file_id, file.provider, file_url))

        return results
