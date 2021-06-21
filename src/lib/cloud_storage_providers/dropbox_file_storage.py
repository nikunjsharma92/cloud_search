from typing import Union
import uuid
from dropbox import Dropbox
from dropbox.files import FileMetadata
from dropbox import DropboxOAuth2FlowNoRedirect
import os
import urllib.parse

from src.lib.cloud_storage_providers.adapters.provider_file_response_adapter import ProviderFileResponse
from src.lib.cloud_storage_providers.cloud_storage_provider_interface import CloudStorageProviderInterface


class DropboxCloudStorage(CloudStorageProviderInterface):
    __client: Union[Dropbox, None]
    __access_token: str

    def __init__(self):
        self.__client = None
        self.__storage_client = None

    def authorize_no_redirect(self):
        pass

    def authorize_redirect(self):
        pass

    def authorize(self, **args):
        return DropboxOAuth2FlowNoRedirect(consumer_key=os.getenv('DROPBOX_KEY'), consumer_secret=os.getenv('DROPBOX_SECRET'),
                                           token_access_type='online', locale='en').start()

    def authenticate(self, code):
        return DropboxOAuth2FlowNoRedirect(consumer_key=os.getenv('DROPBOX_KEY'), consumer_secret=os.getenv('DROPBOX_SECRET'),
                                           token_access_type='online', locale='en').finish(code)

    def init_client(self, access_token):
        self.__client = Dropbox(access_token)

    def init_storage(self, storage_client):
        self.__storage_client = storage_client

    def get_file_list(self):
        response = self.__client.files_list_folder(
            path='',
            recursive=True,
            include_media_info=False,
            include_deleted=False,
            limit=2,
            include_non_downloadable_files=False)
        #TODO: filter out non-pdf/docx files
        while True:
            for entry in response.entries:
                if type(entry) == FileMetadata:
                    yield ProviderFileResponse('dropbox', entry.id, entry.name, entry.path_lower, entry.size, entry.server_modified)

            if not response.has_more:
                break

            response = self.__client.files_list_folder_continue(cursor=response.cursor)

    def get_file_content(self, path: str):
        metadata, res = self.__client.files_download(path)
        return res

    def download_file_content(self, dropbox_file_path):
        extension = dropbox_file_path.split(".")[-1]
        local_file_path = '/tmp/'+str(uuid.uuid4()) + "." + extension
        res = self.get_file_content(dropbox_file_path)
        with open(local_file_path, 'wb') as f:
            for content in res.iter_content(chunk_size=64000):
                f.write(content)

        return local_file_path

    def get_file_url(self, filepath: str):
        directory = filepath.split("/")
        directory_str = "/".join(directory[:-1])
        return 'https://www.dropbox.com/home'+directory_str+"?"+urllib.parse.urlencode({"preview": directory[-1]})
