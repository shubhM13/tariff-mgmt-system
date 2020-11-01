import sqlite3 as db
import time
import traceback
import sys
from db.scripts import DML,DQL

db_path = './db/dispur_wireless.db'

class RoleModel():

    def __init__(self, rid, role):
        self.rid = rid
        self.role = role
    
    #1) Select one
    @classmethod
    def find_by_id(cls, rid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_role_by_id
        result = cursor.execute(query, (rid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                role = RoleModel(row[0], row[1])
            connection.close()
            return role

    #2) Select all
    @classmethod
    def find_all(cls):
        roles = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_role
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                roles.append(RoleModel(row[0], row[1]))
            return roles
        connection.close()

    #3) Insert
    @classmethod
    def insert_into_table(cls, rid, role):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.insert_role
        try:
            result = cursor.execute(query, (rid, role))
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
    def delete_role(self, rid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.delete_role_by_id
        try:
            result = cursor.execute(query, (rid,))
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
            'roleID': self.rid,
            'role': self.role
        }


