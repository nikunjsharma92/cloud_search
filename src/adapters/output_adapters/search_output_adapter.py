from src.models import File


class SearchResultOutputAdapter:
    def __init__(self, id, title, provider_id, provider, file_url):
        self.id = id
        self.title = title
        self.provider_file_id = provider_id
        self.provider = provider
        self.file_url = file_url

    def to_dict(self):
        return {
            'file_id': self.id,
            'title': self.title,
            'provider_file_id': self.provider_file_id,
            'provider': self.provider,
            'file_url': self.file_url
        }
