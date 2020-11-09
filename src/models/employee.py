import sqlite3 as db
import time
import traceback
import sys
from db.scripts import DML,DQL

db_path = './db/dispur_wireless.db'


class EmployeeModel():

    def __init__(self, eid, first_name, last_name, role_id, email, contact):
        self.eid = eid
        self.first_name = first_name
        self.last_name = last_name
        self.role_id = role_id
        self.email = email
        self.contact = contact
       
    
    #1) Select one
    @classmethod
    def find_by_id(cls, eid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_emp_by_id
        result = cursor.execute(query, (eid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                employee = EmployeeModel(row[0], row[1], row[2], row[3], row[4], row[5])
            connection.close()
            return employee

    #2) Select all
    @classmethod
    def find_all(cls):
        employees = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_emp
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                employees.append(EmployeeModel(row[0], row[1], row[2], row[3], row[4], row[5]))
            return employees
        connection.close()

    #3) Insert
    @classmethod
    def insert_into_table(cls, eid, first_name, last_name, role_id, email, contact):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.insert_emp
        try:
            result = cursor.execute(query, (eid, first_name, last_name, role_id, email, contact))
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
    def delete_employee(self, eid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.delete_emp_by_id
        try:
            result = cursor.execute(query, (eid,))
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
    def update_employee(cls, first_name, last_name, email, contact, eid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.update_emp_by_id
        try:
            result = cursor.execute(query, (first_name, last_name, email, contact, eid))
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
    
    #6) Update Role
    @classmethod
    def update_role(cls, eid, role_id):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.update_emp_role
        try:
            result = cursor.execute(query, (role_id, eid))
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
            'empID': self.eid,
            'empFirstName': self.first_name,
            'empLastName': self.last_name,
            'empRoleID': self.role_id,
            'empEmail': self.email,
            'empContact': self.contact
        }