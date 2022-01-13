import sys
sys.path.insert(0, 'E:/Project/ML_and_DL/CBD/ChatBot/~/ParlAI/')

from parlai_internal.agents.laptopbot.Configuration.parameter_constants import *
from parlai_internal.agents.laptopbot.Configuration.notification import *
from mysql.connector import Error
import mysql.connector as msql
import pandas as pd


""" Import data from csv """
order_rec = pd.read_csv("./parlai_internal/agents/laptopbot/Data/auto_record_order.csv",
                        index_col=False, delimiter=',')
""" Create database on local """
try:
    db = msql.connect(host=SERVER, user=USER,
                      password=PASSWORD)
    if db.is_connected():
        cursor = db.cursor()
        cursor.execute("DROP DATABASE IF EXISTS auto_record_order")
        print("Creating database for 'Auto record order' data........")
        cursor.execute("CREATE DATABASE auto_record_order")
        noti_db_create()
        # Create table
        db = msql.connect(host=SERVER, database=DATABASE_AUTO_RECORD_ORDER,
                          user=USER, password=PASSWORD)
        cursor = db.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS auto_record_order_data')
        print("Creating table for 'Auto record order' data........")
        cursor.execute(
            "CREATE TABLE auto_record_order_data(Product varchar(60),Information varchar(150),Price varchar(10),Quantity varchar(20),Customer varchar(50),Time varchar(11))")
        noti_table_create()
        print("Start adding data into table........")
        for i, row in order_rec.iterrows():
            sql = "INSERT INTO auto_record_order.auto_record_order_data VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Added {0} rows into the 'auto_record_order' Database".format(i))
            db.commit()
        noti_add_data()
except Error as e:
    print("Error while connecting to MySQL", e)
