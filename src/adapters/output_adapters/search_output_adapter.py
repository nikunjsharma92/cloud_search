class SearchResultOutputAdapter:
    def __init__(self, id, title, provider_id, provider, fileurl):
        self.id = id
        self.title = title
        self.provider_file_id = provider_id
        self.provider = provider
        self.fileurl = fileurl

    def to_dict(self):
        return {
            'file_id': self.id,
            'title': self.title,
            'provider_file_id': self.provider_file_id,
            'provider': self.provider,
            'fileurl': self.fileurl
        }
