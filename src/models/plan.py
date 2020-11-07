import sqlite3 as db
import time
import traceback
import sys
from db.scripts import DML,DQL

db_path = './db/dispur_wireless.db'

class PlanModel():

    def __init__(self, pid, name, tarrif_call, tarrif_data, validity, rental):
        self.pid = pid
        self.name = name
        self.tarrif_call = tarrif_call
        self.tarrif_data = tarrif_data
        self.validity = validity
        self.rental = rental
       
    #1) Select one
    @classmethod
    def find_by_id(cls, pid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_plan_by_id
        result = cursor.execute(query, (pid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                tarrifPlan = PlanModel(row[0], row[1], row[2], row[3], row[4], row[5])
            connection.close()
            return tarrifPlan

    #2) Select all
    @classmethod
    def find_all(cls):
        tarrifPlans = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_plan
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                tarrifPlans.append(PlanModel(row[0], row[1], row[2], row[3], row[4], row[5]))
            return tarrifPlans
        connection.close()

    @classmethod
    def find_all_not_subscribed(cls, cid):
        tarrifPlans = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_plan_cid
        result = cursor.execute(query, (cid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                tarrifPlans.append(PlanModel(row[0], row[1], row[2], row[3], row[4], row[5]))
            return tarrifPlans
        connection.close()   

    #3) Insert
    @classmethod
    def insert_into_table(cls, pid, name, tarrif_call, tarrif_data, validity, rental):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.insert_plan
        try:
            result = cursor.execute(query, (pid, name, tarrif_call, tarrif_data, validity, rental))
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

    #4) Delete
    @classmethod
    def delete_plan(self, pid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.delete_plan_by_id
        try:
            result = cursor.execute(query, (pid,))
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
    
    #5) Update
    @classmethod
    def update_plan(cls, pid, name, tarrif_call, tarrif_data, validity, rental):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.update_plan_by_id
        try:
            result = cursor.execute(query, (name, tarrif_call, tarrif_data, validity, rental, pid))
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
    
    #6) jsonify the model
    def jsonify(self):
        return{
            'planID': self.pid,
            'planName': self.name,
            'callTarrif': self.tarrif_call,
            'dataTarrif': self.tarrif_data,
            'validity': self.validity,
            'rental': self.rental
        }


