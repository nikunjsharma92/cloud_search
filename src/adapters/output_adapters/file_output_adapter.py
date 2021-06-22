from src.models import File


class FileOutputAdapter:
    def __init__(self, file: File, fileurl: str):
        self.id = file.id
        self.filename = file.filename
        self.filepath = file.filepath
        self.fileurl = fileurl
        self.user_id = file.user_id
        self.provider = file.provider
        self.provider_file_id = file.provider_file_id
        self.last_sync_status = file.last_sync_status
        self.last_synced_on = file.last_synced_on
        self.created_on = file.created_on
        self.updated_on = file.updated_on

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'filepath': self.filepath,
            'fileurl': self.fileurl,
            'user_id': self.user_id,
            'provider': self.provider,
            'provider_file_id': self.provider_file_id,
            'last_sync_status': self.last_sync_status,
            'last_synced_on': self.last_synced_on.isoformat(),
            'created_on': self.created_on.isoformat(),
            'updated_on': self.updated_on.isoformat(),
        }
