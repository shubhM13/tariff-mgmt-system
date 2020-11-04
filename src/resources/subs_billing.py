from models.subscription import SubscriptionModel, CustomerSubscriptionModel, SubscriptionBillModel
from models.bill import BillModel
import time
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Subscription(Resource):

    #@jwt_required()
    def get(self, sid):
        subscription = SubscriptionModel.find_by_id(sid)
        if subscription:
            return {'subscription': subscription.jsonify()}, 200
        return {'message': 'Subscription not found!'}, 404
    
    def delete(self, sid):
        subscription = SubscriptionModel.delete_subscription(sid)
        bill = BillModel.delete_bill_sid(sid)
        if subscription and bill:
            return {'message': 'Subscription {0} was successfully deleted from database!'.format(sid)}, 200
        return {'message': 'Error in deleting the subscription!'}, 500

#unused
class SubscriptionList(Resource):

    def get(self):
        subscriptions = SubscriptionModel.find_all()
        if subscriptions:
            return {'subscriptions': [subscription.jsonify() for subscription in subscriptions]}, 200
        return {'message': 'No subscriptions found!'}, 404

class SubscriptionRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid',
                            type=str,
                            required=True,
                            help='This field is required!')

        parser.add_argument('pid',
                            type=str,
                            required=True,
                            help='This field is required!')        
        data_payload = parser.parse_args()
        sid = data_payload['cid'] + data_payload['pid']  # Generate sid by appedig cid
        status = SubscriptionModel.insert_into_table(sid
                                                    ,data_payload['cid']
                                                    ,data_payload['pid']
                                                    ,time.strftime('%Y-%m-%d %H:%M:%S')
                                                    ,time.strftime('%Y-%m-%d %H:%M:%S'))  #insert current datetime for subs_date and last_billed 
        if status:
            return {'message': 'Subscription successfully added to the database succesfully!'}, 201
        else:
            return {'message': 'Error inserting the subscription!'}, 500

# unused
class SubscriptionUpdate(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sid',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('cid',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('pid',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('subs_date',
                            type=str,
                            required=True,
                            help='This field is required!') 
        parser.add_argument('last_billed',
                            type=str,
                            required=True,
                            help='This field is required!')         
        data_payload = parser.parse_args()
        status = SubscriptionModel.update_subscription(data_payload['cid']
                                                       ,data_payload['pid']
                                                       ,data_payload['subs_date']
                                                       ,data_payload['last_billed']
                                                       ,data_payload['sid'])
        if status:
            return {'message': 'Subscription successfully updated in the database succesfully!'}, 201
        else:
            return {'message': 'Error updating the subscription!'}, 500

# To generate bill - by operator : 1) Inserts in customer_bill table 2) Updates the last_billed date in Subscription table
class GenerateBill(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sid',
                            type=str,
                            required=True,
                            help='This is required!')
        data_payload = parser.parse_args()
        sid = data_payload['sid']
        current_billing_date = time.strftime('%Y-%m-%d %H:%M:%S')        
        bill = SubscriptionBillModel.find_subs_by_sid(sid)
        if bill:
            is_defaulter = BillModel.is_defaulter(sid)
            if is_defaulter:
                due_amount = BillModel.get_total_due(sid)
                bill_insert_status = BillModel.update_bill_sid(bill.cid
                                                               ,bill.pid
                                                               ,bill.name
                                                               ,bill.tarrif_call
                                                               ,bill.tarrif_data
                                                               ,bill.validity
                                                               ,bill.rental
                                                               ,bill.subscribed_on
                                                               ,current_billing_date
                                                               ,bill.voice_usage
                                                               ,bill.data_usage
                                                               ,bill.call_cost
                                                               ,bill.data_cost
                                                               ,bill.total_cost
                                                               ,bill.billing_cycle
                                                               ,due_amount
                                                               ,sid)
                billing_date_update_status = SubscriptionModel.update_last_billed(sid, current_billing_date)
            else:
                due_amount = 0
                bill_insert_status = BillModel.insert_into_table(sid
                                                               ,bill.cid
                                                               ,bill.pid
                                                               ,bill.name
                                                               ,bill.tarrif_call
                                                               ,bill.tarrif_data
                                                               ,bill.validity
                                                               ,bill.rental
                                                               ,bill.subscribed_on
                                                               ,current_billing_date
                                                               ,bill.voice_usage
                                                               ,bill.data_usage
                                                               ,bill.call_cost
                                                               ,bill.data_cost
                                                               ,bill.total_cost
                                                               ,bill.billing_cycle
                                                               ,due_amount)
            if bill_insert_status and billing_date_update_status:
                return {'message': 'Bill generated successfully!'}, 201
            else:
                return {'message': 'Error generating the bill!'}, 500
        else:
            return {'message': 'Billing details for the subscription could not be found!'}, 404
    
# Bill : sid - customer portal
class GetBillForSubscription(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sid',
                             type=str,
                             required=True,
                             help='This is required!')
        data_payload = parser.parse_args()
        sid = data_payload['sid']
        bill = BillModel.find_by_sid(sid)
        if bill:
            return {'bill': bill.jsonify()}, 200
        return {'message': 'The bill for '+sid+' has not been generated by the operator yet. Please check after the billing cycle!'}, 404

# Bill : cid - customer portal
class GetBillForCustomer(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid',
                             type=str,
                             required=True,
                             help='This is required!')
        data_payload = parser.parse_args()
        cid = data_payload['cid']
        bills = BillModel.find_by_cid(cid)
        if bills:
            return {'bills': [bill.jsonify() for bill in bills]}, 200
        return {'message': 'The operator has not genereated any bills for you yet. Please check after billing cycle completion'}, 404
# Usage Details : sid - cusrotmer portal
class MySubscriptionUsageDetails(Resource):
    def post(self):
        parser = reqparse.RequestParser
        parser.add_argument('sid',
                             type=str,
                             required=True,
                             help='This is required!')
        data_payload = parser.parse_args()
        sid = data_payload['sid']
        subscription = SubscriptionBillModel.find_subs_by_sid(sid, for_customer=True)
        if subscription:
            return {'subscription': subscription.jsonify()}, 200
        return {'message': 'No subscription found with id '+sid}, 404
# Usage Details : cid - customer portal
class MyAllSubscriptionUsageDetails(Resource):
    def post(self):
        parser = reqparse.RequestParser
        parser.add_argument('cid',
                             type=str,
                             required=True,
                             help='This is required!')
        data_payload = parser.parse_args()
        cid = data_payload['cid']
        subs = SubscriptionBillModel.find_subs_by_cid(cid, for_customer=True)
        if subs:
            return {'subscriptions': [sub.jsonify() for sub in subs]}, 200
        return {'message': 'No subscriptions found for customer '+cid+'. Please subscribe to new plans!'}, 404
# Usage Details : sid - operator portal
class GetSubscriptionUsageDetails(Resource):
    def post(self):
        parser = reqparse.RequestParser
        parser.add_argument('sid',
                             type=str,
                             required=True,
                             help='This is required!')
        data_payload = parser.parse_args()
        sid = data_payload['sid']
        subscription = SubscriptionBillModel.find_subs_by_sid(sid, for_customer=False)
        if subscription:
            return {'subscriptions': subscription.jsonify()}, 200
        return {'message': 'No subscriptions found with id '+sid}, 404 
# Usage Details : cid - operator portal
class GetAllSubscriptionUsageDetailsForCustomer(Resource):
    def post(self):
        parser = reqparse.RequestParser
        parser.add_argument('cid',
                             type=str,
                             required=True,
                             help='This is required!')
        data_payload = parser.parse_args()
        cid = data_payload['cid']
        subs = SubscriptionBillModel.find_subs_by_cid(cid, for_customer=False)
        if subs:
            return {'subscriptions': [sub.jsonify() for sub in subs]}, 200
        return {'message': 'No subscriptions found for customer '+cid}, 404   
# Subscription Details : sid
class GetSubscriptionDetails(Resource):
    def post(self):
        parser = reqparse.RequestParser
        parser.add_argument('sid',
                             type=str,
                             required=True,
                             help='This is required!')
        data_payload = parser.parse_args()
        sid = data_payload['sid']
        subscription = CustomerSubscriptionModel.find_subs_by_sid(sid)
        if subscription:
            return {'subscription': subscription.jsonify()}, 200
        return {'message': 'No subscriptions found with id '+sid}, 404     

# Subscription Details : cid
class MySubscriptionsDetailsList(Resource):      
    def post(self):
        parser = reqparse.RequestParser
        parser.add_argument('cid',
                             type=str,
                             required=True,
                             help='This is required!')
        data_payload = parser.parse_args()
        cid = data_payload['cid']
        subs = CustomerSubscriptionModel.find_subs_by_cid(cid)
        if subs:
            return {'subscriptions': [sub.jsonify() for sub in subs]}, 200
        return {'message': 'No subscriptions found. Please subscribe to new plans!'}, 404     

# Pay Bill : sid
class PayBill(Resource):
    def post(self):
        parser = reqparse.RequestParser
        parser.add_argument('sid',
                             type=str,
                             required=True,
                             help='This is required!')
        data_payload = parser.parse_args()
        sid = data_payload['sid']
        bill_paid = BillModel.pay_bill(sid)
        if bill_paid:
            return {'message': 'Transaction Succesful ! You have paid the bill for sid '+sid+' on '+str(time.strftime('%d-%m-%Y %H:%M:%S'))+'!'}, 200
        
        return {'message': 'Error ! Transaction failed'}, 500






        



