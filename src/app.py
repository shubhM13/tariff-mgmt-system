from flask import Flask, jsonify
from flask_restful import Api
from security import authenticate, identity
from flask_jwt import JWT, jwt_required, JWTError

from resources.user import User, UserList, UserRegister, UserLogin
from resources.customer import Customer, CustomerList, CustomerRegister, CustomerUpdate
from resources.employee import Employee, EmployeeList, EmployeeRegister, EmployeeUpdate
from resources.plan import Plan, PlanList, PlanRegister
from resources.role import Role, RoleList
from resources.usage import UsageRegister
from resources.subs_billing import Subscription, SubscriptionList, SubscriptionRegister, SubscriptionUpdate, GenerateBill, GetBillForSubscription, GetBillForCustomer, MyAllSubscriptionUsageDetails, MySubscriptionsDetailsList, MySubscriptionUsageDetails, GetAllSubscriptionUsageDetailsForCustomer, GetSubscriptionDetails, GetSubscriptionDetails, My

app = Flask(__name__)
api = Api(app)
app.secret_key = 'test'
jwt = JWT(app, authenticate, identity)


api.add_resource(User, '/user/<string:uid>')
api.add_resource(UserList, '/users')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')


api.add_resource(Customer, '/customer/<string:cid>')
api.add_resource(CustomerList, '/customers')
api.add_resource(CustomerRegister, '/cregister')
api.add_resource(CustomerUpdate, '/cupdate')


api.add_resource(Employee, '/employee/<string:eid>')
api.add_resource(EmployeeList, '/employees')
api.add_resource(EmployeeRegister, '/eregister')
api.add_resource(EmployeeUpdate, '/eupdate')


api.add_resource(Plan, '/plan/<string:pid>')
api.add_resource(PlanList, '/plans')
api.add_resource(PlanRegister, '/pregister')


api.add_resource(Role, '/role/<string:rid>')
api.add_resource(RoleList, '/roles')


api.add_resource(UsageRegister, '/usage')


#Post
api.add_resource(SubscriptionRegister, '/subscribe')
#Delete
api.add_resource(Subscription, '/unsubscribe/<string:sid>')


#Post
api.add_resource(GenerateBill, '/generateBill')
#Post
api.add_resource(GetBillForSubscription, '/getBill')
#Post
api.add_resource(GetBillForCustomer, '/getBillList')
#Post
api.add_resource(MySubscriptionUsageDetails, '/getUsage')
#Post
api.add_resource(MyAllSubscriptionUsageDetails, '/getUsageList')
#Post






@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message': 'Could not authorize user.'}), 400

if __name__ == '__main__':
    app.run()
