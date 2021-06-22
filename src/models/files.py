from typing import List

from sqlalchemy.orm import relationship

from database import db
import datetime

from src.lib.cloud_storage_providers.adapters.provider_file_response_adapter import ProviderFileResponse


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer) #foreign key
    provider = db.Column(db.String(255), nullable=False) # key
    provider_file_id = db.Column(db.String(255), nullable=False) #key
    filename = db.Column(db.String(1023), nullable=False)
    filepath = db.Column(db.String(2047), nullable=False)
    content_store_id = db.Column(db.String(255), nullable=True)
    last_synced_on = db.Column(db.DateTime)
    last_sync_status = db.Column(db.String(63), default='PENDING')
    size_bytes = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    file_content_mappings = relationship('FileContentMapping', lazy='select')

    def __init__(self, user_id, provider, provider_file_id, filename, filepath, size_bytes, content_fetched_on=None):
        self.user_id = user_id
        self.provider = provider
        self.provider_file_id = provider_file_id
        self.filename = filename
        self.filepath = filepath
        self.size_bytes = size_bytes
        self.last_synced_on = content_fetched_on
        self.created_on = datetime.datetime.utcnow()
        self.updated_on = datetime.datetime.utcnow()

    @staticmethod
    def get_by_id(id):
        file = File.query.filter_by(id=id).first()
        return file

    @staticmethod
    def get_by_provider_id(provider_file_id):
        file = File.query.filter_by(provider_file_id=provider_file_id).first()
        return file

    @staticmethod
    def get_by_user_id(user_id):
        files: List[File] = File.query.filter_by(user_id=user_id).all()
        return files

    def get_by_details(self, user, provider, filename, filepath):
        pass

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def update(self):
        self.updated_on = datetime.datetime.utcnow()
        return db.session.commit()

    @staticmethod
    def create_file_record(user_id, file_response: ProviderFileResponse):
        file = File(
            user_id=user_id,
            provider=file_response.provider,
            provider_file_id=file_response.provider_id,
            filename=file_response.filename,
            filepath=file_response.filepath,
            size_bytes=file_response.size_bytes
        )
        file.save()
        return file

    def update_file_record(self, file_response):
        self.filename = file_response.filename
        self.filepath = file_response.filepath
        self.size_bytes = file_response.size_bytes
        self.update()

    def mark_sync_status_pending(self):
        self.last_sync_status = 'PENDING'
        self.update()

    def mark_sync_status_completed(self, synced_on):
        self.last_sync_status = 'COMPLETED'
        self.last_synced_on = synced_on
        self.update()

    def mark_sync_status_failed(self):
        self.last_sync_status = 'FAILED'
        self.update()
