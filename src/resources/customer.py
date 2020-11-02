from models.customer import CustomerModel
from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from resources import id_generator

class Customer(Resource):

    #@jwt_required()
    def get(self, cid):
        customer = CustomerModel.find_by_id(cid)
        if customer:
            return {'customer': customer.jsonify()}, 200
        return {'message': 'Customer not found!'}, 404
    
    def delete(self, cid):
        customer = CustomerModel.delete_customer(cid)
        user = UserModel.delete_user(cid)
        if customer and user:
            return {'message': 'customer {0} was successfully deleted from database!'.format(cid)}, 200
        return {'message': 'Error in deleting the customer!'}, 500

class CustomerList(Resource):

    def get(self):
        customers = CustomerModel.find_all()
        if customers:
            return {'message': [customer.jsonify() for customer in customers]}, 200
        return {'message': 'No customers found!'}, 404

class CustomerRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        cid = id_generator.generate("C")
        parser.add_argument('first_name',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('last_name',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('address',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('city',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('state',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('pincode',
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

        if CustomerModel.find_by_id(data_payload['cid']):
            return {'message': 'Customer with the same customer id already exists in database'}, 400
        else:
            status_user_insert = UserModel.insert_into_table(cid,
                                        data_payload['pswd'],
                                        6)                              # role_id : 6 -- Customer
            status_customer_insert = CustomerModel.insert_into_table(cid,
                                        data_payload['first_name'],
                                        data_payload['last_name'],
                                        data_payload['address'],
                                        data_payload['address'],
                                        data_payload['state'],
                                        data_payload['pincode'],
                                        data_payload['email'],
                                        data_payload['contact'])
            if status_user_insert and status_customer_insert:
                return {'message': 'Customer successfully added to the database!'}, 201
            else:
                return {'message': 'Error inserting the customer!'}, 500

class CustomerUpdate(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid',
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
        parser.add_argument('address',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('city',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('state',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('pincode',
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

        status = CustomerModel.update_customer(data_payload['cid'],
                                    data_payload['first_name'],
                                    data_payload['last_name'],
                                    data_payload['address'],
                                    data_payload['city'],
                                    data_payload['state'],
                                    data_payload['pincode'],
                                    data_payload['email'],
                                    data_payload['contact'])
        if status:
            return {'message': 'Customer data successfully updated in the database!'}, 201
        else:
            return {'message': 'Error updating the customer data!'}, 500


        



