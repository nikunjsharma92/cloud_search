from flask_restful import Resource


class Connect(Resource):
    # get and save tokens from services like drropbox and google drive
    def get(self):
        return {'hello': 'world'}

    def post(self):
        pass

    def put(self):
        pass
