from src.deliveries.http.authenticate import Authenticate
from src.deliveries.http.authorize import Authorize
from src.deliveries.http.sync import Sync


def initialize_routes(api):
    api.add_resource(Authorize, '/<provider>/authorize')
    api.add_resource(Authenticate, '/<provider>/authenticate')
    api.add_resource(Sync, '/sync')