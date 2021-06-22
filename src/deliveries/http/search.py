from flask_restful import Resource

from src.adapters.input_adapters.search_input_adapter import SearchInputAdapter
from src.usecases.content_store_management import ContentStoreManagement
from src.utils.authorize import authorize


class Search(Resource):
    # TODO: pagination
    @staticmethod
    @authorize
    def get(user):
        parsed_request = SearchInputAdapter().parse_get_request()
        results = ContentStoreManagement().search(user, parsed_request[SearchInputAdapter.QUERY])
        return {
            "status": "success",
            "count": len(results),
            "results": [result.to_dict() for result in results],
        }
