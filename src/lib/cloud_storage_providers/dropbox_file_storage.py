from dropbox import Dropbox
from dropbox.files import FileMetadata
from tika import parser



class DropboxFileStorage:
    __client: Dropbox
    __access_token: str

    def __init__(self, access_token: str):
        self.__client = Dropbox(access_token)
        self.__access_token = access_token

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
            local_filename = self.download_file(file['name'], file['path'])
            extracted_data = self.extract_content(local_filename)
            print("Content: ", extracted_data["content"])
            print("Metadata: ", extracted_data["metadata"])
            print("Status: ", extracted_data["status"])


    def download_file(self, name: str, path: str):
        local_filename = '/tmp/dropbox/' + name
        with open(local_filename, "wb") as f:
            metadata, res = self.__client.files_download(path)
            f.write(res.content)
        return local_filename

    def extract_content(self, filename):
        return parser.from_file(filename)