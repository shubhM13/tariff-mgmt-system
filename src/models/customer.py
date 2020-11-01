import sqlite3 as db
import time
import traceback
import sys
from db.scripts import DML,DQL

db_path = './db/dispur_wireless.db'


class CustomerModel():

    def __init__(self, cid, first_name, last_name, address, city, state, pincode, email, contact):
        self.cid = cid
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.pincode = pincode
        self.email = email
        self.contact = contact
               
    
    #1) Select one
    @classmethod
    def find_by_id(cls, cid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_cust_by_id
        result = cursor.execute(query, (cid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                customer = CustomerModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            connection.close()
            return customer

    #2) Select all
    @classmethod
    def find_all(cls):
        customers = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_cust
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                customers.append(CustomerModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            return customers
        connection.close()

    #3) Insert
    @classmethod
    def insert_into_table(cls, cid, first_name, last_name, address, city, state, pincode, email, contact):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.insert_cust
        try:
            result = cursor.execute(query, (cid, first_name, last_name, address, city, state, pincode, email, contact))
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
    def delete_customer(self, cid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.delete_cust_by_id
        try:
            result = cursor.execute(query, (cid,))
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
    def update_customer(cls, cid, first_name, last_name, address, city, state, pincode, email, contact):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.update_cust_by_id
        try:
            result = cursor.execute(query, (cid, first_name, last_name, address, city, state, pincode, email, contact))
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
            'customerID': self.cid,
            'customerFirstName': self.first_name,
            'customerLastName': self.last_name,
            'customerAdress': self.address,
            'customerCity': self.city,
            'customerState': self.state,
            'customerPin': self.pincode,
            'customerEmail': self.email,
            'customerContact': self.contact
        }


