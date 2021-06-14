from flask_restful import Resource
from src.adapters.input_adapters.sync_input_adapter import SyncInputAdapter



class Sync(Resource):
    def post(self, provider):
        parsed_request = SyncInputAdapter().parse_post_request()
        synchronize.delay()

        pass