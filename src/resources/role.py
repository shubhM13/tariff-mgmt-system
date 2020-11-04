from models.role import RoleModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Role(Resource):

    #@jwt_required()
    def get(self, rid):
        role = RoleModel.find_by_id(rid)
        if role:
            return {'role': role.jsonify()}, 200
        return {'message': 'Role not found!'}, 404

class RoleList(Resource):

    def get(self):
        roles = RoleModel.find_all()
        if roles:
            return {'roles': [role.jsonify() for role in roles]}, 200
        return {'message': 'No roles found!'}, 404



        



