from flask_restful import Resource

from src.adapters.input_adapters.search_input_adapter import SearchInputAdapter
from src.usecases.content_store_management import ContentStoreManagement


class Search(Resource):
    # TODO: pagination
    def get(self):
        parsed_request = SearchInputAdapter().parse_get_request()
        results = ContentStoreManagement().search(parsed_request[SearchInputAdapter.QUERY])
        return {
            "status": "success",
            "count": len(results),
            "results": [result.to_dict() for result in results],
        }
