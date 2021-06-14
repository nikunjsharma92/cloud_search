from functools import wraps
from flask import abort, request
from src.models.users import User

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'Authorization' not in request.headers:
            abort(401)
        auth_token = request.headers['Authorization'].split("Bearer ")[1]
        user_id = None
        try:
            user_id = User.decode_auth_token(auth_token)
        except Exception as e:
            abort(401)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(401)
        return f(user, *args, **kws)

    return decorated_function
