import sqlite3 as db
import time
import traceback
import sys
from db.scripts import DML,DQL

db_path = './db/dispur_wireless.db'

class UserModel():

    def __init__(self, uid, pswd, datetime, role_id):
        self.uid = uid
        self. pswd = pswd
        self.datetime = datetime
        self.role_id = role_id
    
    #1) Select one
    @classmethod
    def find_by_id(cls, uid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_user_by_id
        result = cursor.execute(query, (uid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                user = UserModel(row[0], row[1], row[2], row[3])
            connection.close()
            return user

    #2) Select all
    @classmethod
    def find_all(cls):
        users = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_users
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                users.append(UserModel(row[0], row[1], row[2], row[3]))
            return users
        connection.close()

    #3) Insert
    @classmethod
    def insert_into_table(cls, uid, pswd, role_id):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')  # sql datetime format
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.insert_user
        try:
            result = cursor.execute(query, (uid, pswd, datetime, role_id))
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
    def update_user(cls, uid, pswd, role_id):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')  # sql datetime format
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.update_user_by_id
        try:
            result = cursor.execute(query, (pswd, datetime, role_id, uid))
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
    def delete_user(self, uid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.delete_user_by_id
        try:
            result = cursor.execute(query, (uid,))
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
    
    #6) Login
    @classmethod
    def login(self, uid, pswd):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.login
        result = cursor.execute(query, (uid, pswd))
        role = result.fetchall()
        connection.close()
        if role:
            return role

    #7) jsonify the model
    def jsonify(self):
        return{
            'id': self.uid,
            'password': self.pswd,
            'lastUpdated': self.datetime,
            'roleID': self.role_id
        }


