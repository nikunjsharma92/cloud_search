from typing import List

from sqlalchemy import ForeignKey
import datetime

from database import db


class FileContentMapping(db.Model):
    __tablename__ = 'file_content_mappings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    file_id = db.Column(db.Integer, ForeignKey('files.id'), nullable=False)
    content_store_id = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=1)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, file_id, content_store_id, user_id):
        self.file_id = file_id
        self.content_store_id = content_store_id
        self.user_id = user_id
        self.is_active = 1
        self.created_on = datetime.datetime.utcnow()
        self.updated_on = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        return db.session.commit()

    @staticmethod
    def get_mappings_by_user_id(user_id):
        mappings = FileContentMapping.query.filter_by(user_id=user_id).all()
        return mappings
