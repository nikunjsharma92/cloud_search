from flask_restful import reqparse


class SyncInputAdapter:
    ACCESS_TOKEN: str = 'access_token'

    def parse_post_request(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.ACCESS_TOKEN, type=str, required=True)
        return parser.parse_args()