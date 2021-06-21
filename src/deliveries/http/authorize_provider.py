from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from src.usecases.cloud_storage_provider_management import CloudStorageProviderManagement
from src.utils.authorize import authorize


class AuthorizeProvider(Resource):
    # get and save tokens from services like drropbox and google drive
    @authorize
    def get(self, user, provider):
        try:
            authorization_url = CloudStorageProviderManagement(provider).authorize()
        except Exception as e:
            raise BadRequest("Invalid Provider")

        return {
            'status': 'success',
            'authorization_url': authorization_url,
            'message': 'Please visit the authorization url and login to '+provider
        }, 200
