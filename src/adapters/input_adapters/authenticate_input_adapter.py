from flask_restful import reqparse


class AuthenticateInputAdapter:
    CODE: str = 'code'

    def parse_post_request(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.CODE, type=str, required=True)
        return parser.parse_args()
