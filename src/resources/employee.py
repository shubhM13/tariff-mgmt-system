from models.employee import EmployeeModel
from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from resources import id_generator

class Employee(Resource):

    #@jwt_required()
    def get(self, eid):
        employee = EmployeeModel.find_by_id(eid)
        if employee:
            return {'employee': employee.jsonify()}, 200
        return {'message': 'Employee not found!'}, 404
    
    def delete(self, eid):
        employee = EmployeeModel.delete_employee(eid)
        user = UserModel.delete_user(eid)
        if employee and user:
            return {'message': 'Employee {0} was successfully deleted from database!'.format(eid)}, 200
        return {'message': 'Error in deleting the employee!'}, 500

class EmployeeList(Resource):

    def get(self):
        employees = EmployeeModel.find_all()
        if employees:
            return {'employees': [employee.jsonify() for employee in employees]}, 200
        return {'message': 'No employees found!'}, 404

class EmployeeRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        eid = id_generator.generate("E")
        parser.add_argument('first_name',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('last_name',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('role_id',
                            type=int,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('contact',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('pswd',
                            type=str,
                            required=True,
                            help='This field is required!') 

        data_payload = parser.parse_args()
        status_user_insert = UserModel.insert_into_table(eid,
                                    data_payload['pswd'],
                                    data_payload['role_id'])                              # role_id : 6 -- Employee
        status_employee_insert = EmployeeModel.insert_into_table(eid,
                                    data_payload['first_name'],
                                    data_payload['last_name'],
                                    data_payload['role_id'],
                                    data_payload['email'],
                                    data_payload['contact'])
        if status_user_insert and status_employee_insert:
            return {'message': 'Employee successfully added to the database!'}, 201
        else:
            return {'message': 'Error inserting the employee!'}, 500

class EmployeeUpdate(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('eid',
                            type=str,
                            required=True,
                            help='This field is required!')        
        parser.add_argument('first_name',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('last_name',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('role_id',
                            type=int,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('contact',
                            type=str,
                            required=True,
                            help='This field is required!') 

        data_payload = parser.parse_args()

        status = EmployeeModel.update_employee(data_payload['first_name'],
                                    data_payload['last_name'],
                                    data_payload['role_id'],
                                    data_payload['email'],
                                    data_payload['contact']
                                    ,data_payload['eid'])
        if status:
            return {'message': 'Employee data successfully updated in the database!'}, 201
        else:
            return {'message': 'Error updating the employee data!'}, 500


        



