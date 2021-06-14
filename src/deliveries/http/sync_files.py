from flask_restful import Resource
from src.adapters.input_adapters.sync_input_adapter import SyncInputAdapter
from src.usecases.cloud_storage_provider_management import CloudStorageProviderManagement
from src.utils.authorize import authorize


class Sync(Resource):
    @staticmethod
    @authorize
    def post(user, provider):
        parsed_request = SyncInputAdapter().parse_post_request()
        CloudStorageProviderManagement().start_synchronization(user, provider, parsed_request[SyncInputAdapter.ACCESS_TOKEN])
        return {
            "status": "success",
            "message": "Sync successfully started"
        }
