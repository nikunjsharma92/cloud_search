from flask_restful import reqparse


class LogoutInputAdapter:
    AUTHORIZATION_HEADER: str = 'Authorization'
    AUTH_TOKEN: str = 'auth_token'

    def parse_post_request(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.AUTHORIZATION_HEADER, type=str, required=True, location='headers')
        parsed_args = parser.parse_args()
        parsed_args[self.AUTH_TOKEN] = parsed_args[self.AUTHORIZATION_HEADER].split('Bearer ')[1]
        return parsed_args
