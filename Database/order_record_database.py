import sys
sys.path.insert(0, 'E:/Project/ML_and_DL/CBD/Chatbot/')

from Configuration.parameter_constants import *
from Configuration.notification import *
from mysql.connector import Error
import mysql.connector as msql
import pandas as pd
import time



""" Import data from csv """
order_rec = pd.read_csv("./data/order_record.csv",
                        index_col=False, delimiter=',')

""" Create database on local """
try:
    db = msql.connect(host=SERVER, user=USER,
                      password=PASSWORD)
    if db.is_connected():
        cursor = db.cursor()
        cursor.execute("DROP DATABASE IF EXISTS order_record")
        print("Creating database for 'Order record' data........")
        cursor.execute("CREATE DATABASE order_record")
        noti_db_create()
        # Create table
        db = msql.connect(host=SERVER, database=DATABASE_ORDER,
                          user=USER, password=PASSWORD)
        cursor = db.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS order_record_data')
        print("Creating table for 'Order record' data........")
        cursor.execute(
            "CREATE TABLE order_record_data(laptop_ID varchar(5),Quantity varchar(6),Month varchar(3),user_ID varchar(5))")
        noti_table_create()
        print("Start adding data into table........")
        for i, row in order_rec.iterrows():
            sql = "INSERT INTO order_record.order_record_data VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Added {0} rows into the order_record Database".format(i))
            db.commit()
        noti_add_data()
except Error as e:
    print("Error while connecting to MySQL", e)
