from flask_restful import reqparse
from werkzeug.exceptions import BadRequest


class SearchInputAdapter:
    QUERY: str = 'q'

    def parse_get_request(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.QUERY, type=str, required=True)
        args = parser.parse_args()
        if len(args[self.QUERY]) < 3:
            raise BadRequest("Please specify a query of length 3")
        return args
