from datetime import datetime
import time



def noti_add_data():
    print("====================================")
    print("====================================")
    print("|                                  |")
    print("|                                  |")
    print("|          DATA IS ADDED           |")
    print("|                                  |")
    print("|                                  |")
    print("====================================")
    print("====================================")
    time.sleep(3)


def noti_table_create():
    print("====================================")
    print("====================================")
    print("|                                  |")
    print("|                                  |")
    print("|        TABLE IS CREATED          |")
    print("|                                  |")
    print("|                                  |")
    print("====================================")
    print("====================================")
    time.sleep(3)


def noti_db_create():
    print("====================================")
    print("====================================")
    print("|                                  |")
    print("|                                  |")
    print("|        DATABASE IS CREATED       |")
    print("|                                  |")
    print("|                                  |")
    print("====================================")
    print("====================================")
    time.sleep(3)


def noti_rp_gen():
    print("====================================")
    print("GENERATING ANALYTICAL REPORT......" +
          "(" + str(datetime.today().strftime("%m/%d/%Y")) + ")")


def noti_rp_complete():
    print("====================================")
    print("SUCCESS PROCESS.")
    time.sleep(1)
