import sqlite3 as db
import time
import traceback
import sys
from db.scripts import DML,DQL

db_path = './db/dispur_wireless.db'


class SubscriptionModel():

    def __init__(self, sid, cid, pid):
        self.sid = sid
        self. cid = cid
        self.pid = pid
       
    
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
                subscription = SubscriptionModel(row[0], row[1], row[2])
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
                subscriptions.append(SubscriptionModel(row[0], row[1], row[2]))
            return subscriptions
        connection.close()

    #3) Insert
    @classmethod
    def insert_into_table(cls, sid, cid, pid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.insert_subs
        try:
            result = cursor.execute(query, (sid, cid, pid))
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
    
    #6) jsonify the model
    def jsonify(self):
        return{
            'subID': self.sid,
            'customerID': self.cid,
            'planID': self.pid
        }


