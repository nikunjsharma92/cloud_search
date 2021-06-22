class ProviderFileResponse:
    def __init__(self, provider, provider_id, filename, filepath, size_bytes, last_modified_on):
        self.provider = provider
        self.provider_id = provider_id
        self.filename = filename
        self.filepath = filepath
        self.size_bytes = size_bytes
        self.last_modified_on = last_modified_on

