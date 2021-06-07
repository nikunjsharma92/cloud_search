from typing import Union
from dropbox import Dropbox
from dropbox.files import FileMetadata


class DropboxFileStorage:
    client: Dropbox

    def __init__(self, access_token: str):
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
            self.download_file(file['name'], file['path'])

    def download_file(self, name: str, path: str):
        with open('/tmp/dropbox/' + name, "wb") as f:
            metadata, res = self.__client.files_download(path)
            f.write(res.content)

