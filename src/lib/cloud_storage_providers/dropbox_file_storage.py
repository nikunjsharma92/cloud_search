from typing import Union

from dropbox import Dropbox
from dropbox.files import FileMetadata
from tika import parser
from dropbox import DropboxOAuth2FlowNoRedirect
import os


class DropboxFileStorage:
    __client: Union[Dropbox, None]
    __access_token: str

    def __init__(self):
        self.__client = None

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

    def get_file_list(self):
        response = self.__client.files_list_folder(
            path='',
            recursive=True,
            include_media_info=False,
            include_deleted=True,
            limit=2,
            include_non_downloadable_files=True)

        while True:
            for entry in response.entries:
                if type(entry) == FileMetadata:
                    yield {'name': entry.name, 'path': entry.path_lower, 'size': entry.size,
                           'is_downloadable': entry.is_downloadable}

            if not response.has_more:
                break

            response = self.__client.files_list_folder_continue(cursor=response.cursor)

    def sync(self):
        files = self.get_file_list()
        for file in files:
            extracted_chunk = self.download_file(file['name'], file['path'])
            # write to ES

    def download_file(self, name: str, path: str):
        metadata, res = self.__client.files_download(path)
        for data_chunk in res.iter_content(chunk_size=1000):
            extracted_content = self.extract_content(data_chunk)
            if extracted_content['content'] is not None:
                yield extracted_content['content']

        # since dropbox utilizes stream to make requests, connections need to be closed
        # more information
        # <https://github.com/dropbox/dropbox-sdk-python/blob/13bf19853a8e418dd2bba3e8857619c53206a3c1/dropbox/dropbox_client.py#L568>
        self.__client.close()

    def extract_content(self, data_chunk):
        return parser.from_buffer(data_chunk)