from models.usage import UsageModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Usage(Resource):

    #@jwt_required()
    def get(self, sid):
        usage = UsageModel.find_by_id(sid)
        if usage:
            return {'usage': usage.jsonify()}, 200
        return {'message': 'Usage not found!'}, 404
    
    def delete(self, sid):
        usage = UsageModel.delete_usage(sid)
        if usage:
            return {'message': 'Usage {0} was successfully deleted from database!'.format(sid)}, 200
        return {'message': 'Error in deleting the usage!'}, 500

class UsageList(Resource):

    def get(self):
        usages = UsageModel.find_all()
        if usages:
            return {'usageList': [usage.jsonify() for usage in usages]}, 200
        return {'message': 'No usages found!'}, 404

class UsageRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sid',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('voice',
                            type=int,
                            required=True,
                            help='This field is required!')

        parser.add_argument('data',
                            type=int,
                            required=True,
                            help='This field is required!')      

        data_payload = parser.parse_args()
        status = UsageModel.insert_into_table(data_payload['sid'],
                                    data_payload['voice'],
                                    data_payload['data'])
        if status:
            return {'message': 'Usage successfully added to the database!'}, 201
        else:
            return {'message': 'Error inserting the usage!'}, 500


        



