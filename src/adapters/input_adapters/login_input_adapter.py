from flask_restful import reqparse


class LoginInputAdapter:
    EMAIL: str = 'email'
    PASSWORD: str = 'password'

    def parse_post_request(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.EMAIL, type=str, required=True)
        parser.add_argument(self.PASSWORD, type=str, required=True)
        return parser.parse_args()