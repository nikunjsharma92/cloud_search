from src.adapters.output_adapters.file_output_adapter import FileOutputAdapter
from src.lib.cloud_storage_providers.cloud_storage_provider import get_cloud_storage_provider
from src.models import File


class FileManagement():
    def get_files(self, user):
        files = File.get_by_user_id(user.id)
        results = []
        for file in files:
            file_url = get_cloud_storage_provider(file.provider)().get_file_url(file.filepath)
            results.append(
                FileOutputAdapter(file, file_url))

        return results
