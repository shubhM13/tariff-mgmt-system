from models.plan import PlanModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from resources import id_generator

class Plan(Resource):

    #@jwt_required()
    def get(self, pid):
        plan = PlanModel.find_by_id(pid)
        if plan:
            return {'plan': plan.jsonify()}, 200
        return {'message': 'Plan not found!'}, 404
    
    def delete(self, pid):
        plan = PlanModel.delete_plan(pid)
        if plan:
            return {'message': 'Tarrif Plan {0} was successfully deleted from database!'.format(pid)}, 200
        return {'message': 'Error in deleting the tarrif plan!'}, 500

class PlanList(Resource):
    def get(self, cid):
        plans = PlanModel.find_all_not_subscribed(cid)
        if plans:
            return {'plans': [plan.jsonify() for plan in plans]}, 200
        return {'message': 'No tarrif plans found!'}, 404

class PlanListAll(Resource):
    def get(self):
        plans = PlanModel.find_all()
        if plans:
            return {'plans': [plan.jsonify() for plan in plans]}, 200
        return {'plans': None}, 200


class PlanRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        pid = id_generator.generate("P")
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('tarrif_call',
                            type=float,
                            required=True,
                            help='This field is required!')
        parser.add_argument('tarrif_data',
                            type=float,
                            required=True,
                            help='This field is required!')     
        parser.add_argument('validity',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('rental',
                            type=str,
                            required=False)

        data_payload = parser.parse_args()

        if PlanModel.find_by_id(pid):
            return {'message': 'Plan with the same plan-id already exists in database'}, 400
        else:
            status = PlanModel.insert_into_table(pid,
                                        data_payload['name'],
                                        data_payload['tarrif_call'],
                                        data_payload['tarrif_data'],
                                        data_payload['validity'],
                                        data_payload['rental'])
            if status:
                return {'message': 'Tarrif Plan successfully added to the database!'}, 201
            else:
                return {'message': 'Error inserting the tarrif plan!'}, 500

class PlanUpdate(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pid',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('tarrif_call',
                            type=float,
                            required=True,
                            help='This field is required!')
        parser.add_argument('tarrif_data',
                            type=float,
                            required=True,
                            help='This field is required!')     
        parser.add_argument('validity',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('rental',
                            type=str,
                            required=False)

        data_payload = parser.parse_args()

        status = PlanModel.insert_into_table(
                                    data_payload['name'],
                                    data_payload['tarrif_call'],
                                    data_payload['tarrif_data'],
                                    data_payload['validity'],
                                    data_payload['rental'],
                                    data_payload['pid'])
        if status:
            return {'message': 'Tarrif Plan successfully added to the database!'}, 201
        else:
            return {'message': 'Error inserting the tarrif plan!'}, 500


        



