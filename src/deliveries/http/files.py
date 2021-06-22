from flask_restful import Resource

from src.usecases.file_management import FileManagement
from src.utils.authorize import authorize


class Files(Resource):
    @staticmethod
    @authorize
    def get(user):
        files = FileManagement().get_files(user)
        return {
            'status': 'success',
            'results': [file.to_dict() for file in files],
            'count': len(files),
        }




