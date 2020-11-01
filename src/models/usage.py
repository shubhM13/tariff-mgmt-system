import sqlite3 as db
import time
import traceback
import sys
from db.scripts import DML,DQL

db_path = './db/dispur_wireless.db'


class UsageModel():

    def __init__(self, sid, voice, data, datetime):
        self.sid = sid
        self.voice = voice
        self.data = data
        self.datetime = datetime
                     
    
    #1) Select one
    @classmethod
    def find_by_id(cls, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_usage_by_id
        result = cursor.execute(query, (sid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                usage = UsageModel(row[0], row[1], row[2], row[3])
            connection.close()
            return usage

    #2) Select all
    @classmethod
    def find_all(cls):
        usages = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_usage
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                usages.append(UsageModel(row[0], row[1], row[2], row[3]))
            return usages
        connection.close()

    #3) Insert
    @classmethod
    def insert_into_table(cls, sid, voice, data):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.insert_usage
        try:
            result = cursor.execute(query, (sid, voice, data, datetime))
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
    def delete_usage(self, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.delete_usage_by_id
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
    
    #5) Update
    @classmethod
    def update_usage(cls, sid, voice, data):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.update_usage_by_id
        try:
            result = cursor.execute(query, (sid, voice, data, datetime))
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
            'subsciprtionID': self.sid,
            'voice': self.voice,
            'data': self.data,
            'datetime': self.datetime
        }


