import sys
sys.path.insert(0, 'E:/Project/ML_and_DL/CBD/Chatbot/')

from Configuration.parameter_constants import *
from Configuration.notification import *
from mysql.connector import Error
import mysql.connector as msql
import pandas as pd



""" Import data from csv """
laptop_data = pd.read_csv('./Data/laptop_price.csv',
                          index_col=False, delimiter=',')

""" Create database on local """
try:
    db = msql.connect(host=SERVER, user=USER,
                      password=PASSWORD)
    if db.is_connected():
        cursor = db.cursor()
        cursor.execute("DROP DATABASE IF EXISTS laptop_price")
        print("Creating database for 'Laptop price' data........")
        cursor.execute("CREATE DATABASE laptop_price")
        noti_db_create()
        # Create table
        print("Start creating table................")
        db = msql.connect(host=SERVER, database=DATABASE_LAPTOP,
                          user=USER, password=PASSWORD)
        cursor = db.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS laptop_price_data')
        print("Creating table for 'Laptop price' data........")
        cursor.execute("CREATE TABLE laptop_price_data(laptop_ID varchar(5),Company varchar(10),Product varchar(100),TypeName varchar(25),Inches varchar(5),ScreenResolution varchar(100),Cpu varchar(100),Ram varchar(5),Memory varchar(50),GPU varchar(50),OpSys varchar(15),Weight varchar(10),Price_euros varchar(8))")
        noti_table_create()
        print("Start adding data into table........")
        for i, row in laptop_data.iterrows():
            sql = "INSERT INTO laptop_price.laptop_price_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Added {0} rows into the 'laptop_price' Database".format(i))
            db.commit()
        noti_add_data()
except Error as e:
    print("Error while connecting to MySQL", e)
