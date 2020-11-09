from flask import Flask, jsonify
from flask_restful import Api
from security import authenticate, identity
from flask_jwt import JWT, jwt_required, JWTError
from flask_cors import CORS 

from resources.user import User, UserList, UserRegister, UserLogin
from resources.customer import Customer, CustomerList, CustomerRegister, CustomerUpdate
from resources.employee import Employee, EmployeeList, EmployeeRegister, EmployeeUpdate, RoleUpdate
from resources.plan import Plan, PlanList, PlanListAll, PlanRegister, PlanUpdate
from resources.role import Role, RoleList
from resources.usage import UsageRegister
from resources.subs_billing import Subscription, SubscriptionList, SubscriptionRegister, SubscriptionUpdate, GenerateBill, GetBillForSubscription, GetBillForCustomer, MySubscriptionsDetailsList, GetAllSubscriptionUsageDetails, GetSubscriptionDetails, GetSubscriptionDetails, GetSubscriptionUsageDetails, PayBill

app = Flask(__name__)
CORS(app)
api = Api(app)
app.secret_key = 'test'
jwt = JWT(app, authenticate, identity)


api.add_resource(User, '/user/<string:uid>')
api.add_resource(UserList, '/users')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')


api.add_resource(Customer, '/customer/<string:cid>')
api.add_resource(CustomerList, '/customers')
#works
api.add_resource(CustomerRegister, '/cregister')
#works - check non existent
api.add_resource(CustomerUpdate, '/cupdate')


api.add_resource(Employee, '/employee/<string:eid>')
api.add_resource(EmployeeList, '/employees')
#works
api.add_resource(EmployeeRegister, '/eregister')
#works 
api.add_resource(EmployeeUpdate, '/eupdate')
api.add_resource(RoleUpdate, '/rupdate')


api.add_resource(Plan, '/plan/<string:pid>')
api.add_resource(PlanList, '/plans/<string:cid>')
api.add_resource(PlanListAll, '/plans')
api.add_resource(PlanRegister, '/pregister')
api.add_resource(PlanUpdate, '/pupdate')


api.add_resource(Role, '/role/<string:rid>')
api.add_resource(RoleList, '/roles')


api.add_resource(UsageRegister, '/usage')


#Post - works
api.add_resource(SubscriptionRegister, '/subscribe')
#Delete - works
api.add_resource(Subscription, '/unsubscribe/<string:sid>')


#Get - works
api.add_resource(GetBillForSubscription, '/getBill/<string:sid>')
#Get - works
api.add_resource(GetBillForCustomer, '/getBillList/<string:cid>')
#Get - works
api.add_resource(GetSubscriptionDetails, '/getSubscription/<string:sid>')
#Get - works
api.add_resource(MySubscriptionsDetailsList, '/getSubscriptionList/<string:cid>')
#Get - works
api.add_resource(PayBill, '/payBill/<string:sid>')



#Get - works
api.add_resource(GetSubscriptionUsageDetails, '/getUsage/<string:sid>')
#Get - works
api.add_resource(GetAllSubscriptionUsageDetails, '/getUsageList/<string:cid>')
#Get - works
api.add_resource(GenerateBill, '/generateBill/<string:sid>')



@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message': 'Could not authorize user.'}), 400

if __name__ == '__main__':
    app.run()
