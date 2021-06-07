from flask_restful import Resource


class Search(Resource):
    # return list of files matching the query terms
    def get(self):
        return {'hello': 'world'}

    def post(self):
        pass

    def put(self):
        pass
