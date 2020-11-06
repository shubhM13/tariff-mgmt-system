# Todo Digaant
import sqlite3 as db
import traceback
import sys
from db.scripts import DML,DQL

db_path = './db/dispur_wireless.db'

class SubscriptionModel():

    def __init__(self, sid, cid, pid, subs_date, last_billed):
        self.sid = sid
        self. cid = cid
        self.pid = pid
        self.subs_date = subs_date
        self.last_billed = last_billed
          
    #1) Select one
    @classmethod
    def find_by_id(cls, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_subs_by_id
        result = cursor.execute(query, (sid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                subscription = SubscriptionModel(row[0], row[1], row[2], row[3], row[4])
            connection.close()
            return subscription

    #2) Select all
    @classmethod
    def find_all(cls):
        subscriptions = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_subs
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                subscriptions.append(SubscriptionModel(row[0], row[1], row[2], row[3], row[4]))
            return subscriptions
        connection.close()

    #3) Insert
    @classmethod
    def insert_into_table(cls, sid, cid, pid, subs_date, last_billed):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.insert_subs
        try:
            result = cursor.execute(query, (sid, cid, pid, subs_date, last_billed))
            connection.commit()
            connection.close()
            return True
        except db.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            connection.close()
            return False
    
    #4) Update
    @classmethod
    def update_subscription(cls, sid, cid, pid, subs_date, last_billed):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.update_subs_by_id
        try:
            result = cursor.execute(query, (cid, pid, subs_date, last_billed, sid))
            connection.commit()
            connection.close()
            return True
        except db.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            connection.close()
            return False


    #5) Delete
    @classmethod
    def delete_subscription(self, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.delete_subs_by_id
        try:
            result = cursor.execute(query, (sid,))
            connection.commit()
            return True
        except db.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            connection.close()
            return False
    
    #6) Update last Billed
    @classmethod
    def update_last_billed(cls, sid, last_billed):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.update_last_billed_date
        try:
            result = cursor.execute(query, (last_billed, sid))
            connection.commit()
            connection.close()
            return True
        except db.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            connection.close()
            return False

    
    #7) jsonify the model
    def jsonify(self):
        return{
            'subID': self.sid,
            'customerID': self.cid,
            'planID': self.pid,
            'subsDate': self.subs_date,
            'lastBilled': self.last_billed
        }

class CustomerSubscriptionModel:
    def __init__(self, sid, subscribed_on, cid, pid, name, tarrif_call, tarrif_data, validity, rental):
        self.sid = sid
        self.subscribed_on = subscribed_on
        self.cid = cid
        self.pid = pid
        self.name = name
        self.tarrif_call = tarrif_call
        self.tarrif_data = tarrif_data
        self.validity = validity
        self.rental = rental
    
    #1) Select All
    @classmethod
    def find_all(cls):
        subscriptions_details_list = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_subs_details
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                subscriptions_details_list.append(CustomerSubscriptionModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            connection.close()
            return subscriptions_details_list
        
    
    #2) Select by sid
    @classmethod
    def find_subs_by_sid(cls, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_subs_details_by_sid
        result = cursor.execute(query, (sid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                subscription_details = CustomerSubscriptionModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            connection.close()
            return subscription_details
    
    #3) Select by cid
    @classmethod
    def find_subs_by_cid(cls, cid):
        subscriptions_details_list = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_subs_details_by_cid
        result = cursor.execute(query, (cid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                subscriptions_details_list.append(CustomerSubscriptionModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            connection.close()
            return subscriptions_details_list
    
    #4) jsonify the model
    def jsonify(self):
        return{
            'subID': self.sid,
            'subscribedOn': self.subscribed_on,
            'customerID': self.cid,
            'planID': self.pid,
            'name': self.name,
            'callTarrif': self.tarrif_call,
            'dataTarrif': self.tarrif_data,
            'validity': self.validity,
            'rental': self.rental
        }


        

class SubscriptionBillModel():
    def __init__(self, sid, cid, pid, name, tarrif_call, tarrif_data, validity, rental, subscribed_on, last_billed, voice_usage, data_usage, call_cost, data_cost, total_cost, billing_cycle, not_billed):
        self.sid = sid
        self.cid  = cid
        self.pid = pid
        self.name = name
        self.tarrif_call = tarrif_call
        self.tarrif_data = tarrif_data
        self.validity = validity
        self.rental = rental
        self.subscribed_on = subscribed_on
        self.last_billed = last_billed
        self.voice_usage = voice_usage
        self.data_usage = data_usage
        self.call_cost = call_cost
        self.data_cost = data_cost
        self.total_cost = total_cost
        self.billing_cycle = billing_cycle
        self.not_billed = not_billed
    

    #1) Select All
    @classmethod
    def find_all(cls):
        subscriptions_bill_details_list = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_usage_details
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                subscriptions_bill_details_list.append(SubscriptionBillModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16]))
            connection.close()
            return subscriptions_bill_details_list
    
    #2) Select by sid
    @classmethod
    def find_subs_by_sid(cls, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_usage_details_by_sid
        result = cursor.execute(query, (sid,))
        rows = result.fetchall()            
        if rows:
            for row in rows:
                subscription_details_sid = SubscriptionBillModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16])
            connection.close()
            return subscription_details_sid 
    
    #3) Select by cid
    @classmethod
    def find_subs_by_cid(cls, cid):
        subscription_details_list = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_usage_details_by_cid
        result = cursor.execute(query, (cid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                subscription_details_list.append(SubscriptionBillModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16]))
        else:
            print("No Data Fetched for given cid")
        connection.close()
        return subscription_details_list
    
    #4) jsonify the model
    def jsonify(self):
        return{
            'subID': self.sid,
            'customerID': self.cid,
            'planID': self.pid,
            'name': self.name,
            'callTarrif': self.tarrif_call,
            'dataTarrif': self.tarrif_data,
            'validity': self.validity,
            'rental': self.rental,
            'subscribedOn': self.subscribed_on,
            'lastBilled': self.last_billed,
            'voiceUsage': self.voice_usage,
            'dataUsage': self.data_usage,
            'callCost': self.call_cost,
            'dataCost': self.data_cost,
            'totalCost': self.total_cost,
            'billingCycle': self.billing_cycle,
            'notBilled': self.not_billed
        }
