from src.deliveries.http.authenticate_provider import AuthenticateProvider
from src.deliveries.http.authorize_provider import AuthorizeProvider
from src.deliveries.http.files import Files
from src.deliveries.http.login import Login
from src.deliveries.http.logout import Logout
from src.deliveries.http.register import Register
from src.deliveries.http.sync_files import Sync
from src.deliveries.http.search import Search


def initialize_routes(api):
    api.add_resource(AuthorizeProvider, '/<provider>/authorize')
    api.add_resource(AuthenticateProvider, '/<provider>/authenticate')
    api.add_resource(Sync, '/<provider>/sync')
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(Search, '/search')
    api.add_resource(Files, '/files')
