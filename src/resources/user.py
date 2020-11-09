from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class User(Resource):

    #@jwt_required()
    def get(self, uid):
        user = UserModel.find_by_id(uid)
        if user:
            return {'user': user.jsonify()}, 200
        return {'message': 'User not found!'}, 404
    
    def delete(self, uid):
        user = UserModel.delete_user(uid)
        if user:
            return {'message': 'User {0} was successfully deleted from database!'.format(uid)}, 200
        return {'message': 'Error in deleting the user!'}, 500
    

class UserList(Resource):

    def get(self):
        users = UserModel.find_all()
        if users:
            return {'users': [user.jsonify() for user in users]}, 200
        return {'message': 'No users found!'}, 404

class UserRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('pswd',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('role_id',
                            type=str,
                            required=True,
                            help='This field is required!')      

        data_payload = parser.parse_args()

        if UserModel.find_by_id(data_payload['uid']):
            return {'message': 'User with the same user id already exists in database'}, 400
        else:
            status = UserModel.insert_into_table(data_payload['uid'],
                                        data_payload['pswd'],
                                        data_payload['role_id'])
            if status:
                return {'message': 'User successfully added to the database!'}, 201
            else:
                return {'message': 'Error inserting the user!'}, 500

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('pswd',
                            type=str,
                            required=True,
                            help='This field is required!')
        data_payload = parser.parse_args()
        exists = UserModel.find_by_id(data_payload['uid']) 
        if exists:                  
            user = UserModel.login(data_payload['uid'], data_payload['pswd'])
            if user:
                return {'role': user['role'],
                        'name': user['name'],
                       'message':'login success'}, 200
            else:
                return {'role': None,
                        'name': None,
                        'message': 'login error'}, 200
        return {'message': 'login error'}, 500



