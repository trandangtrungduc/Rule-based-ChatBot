"""    Define server connection parameters   """

SERVER = 'localhost'
USER = 'root'
PASSWORD = 'abc'
DATABASE_LAPTOP = 'laptop_price'
DATABASE_ORDER = 'order_record'
DATABASE_AUTO_RECORD_ORDER = 'auto_record_order'

"""    Define A4 Size  """
WIDTH = 210
HEIGHT = 297

# 2 in 1 CONVERTIBLE
def w_2in1_D_inc(inches):
    switcher = {"1": "11.6", "2": "12.5",
                  "3": "13.3", "4": "15.0", "5": "15.6", "6": "17.3"}
    return switcher.get(inches)

def w_2in1_Ac_inc(inches):
    switcher = {"1": "11.6", "2": "13.3", "3": "14.0"}
    return switcher.get(inches)

def w_2in1_As_inc(inches):
    switcher = {"1": "11.6", "2": "13.3", "3": "15.6"}
    return switcher.get(inches)

def w_2in1_HP_inc(inches):
    switcher = {"1": "11.6", "2": "13.3", "3": "14.0", "4": "15.6"}
    return switcher.get(inches)

def w_2in1_Le_inc(inches):
    switcher = {"1": "10.1", "2": "11.3", "3": "13.3", 
                  "4": "13.9", "5": "14.0", "6": "15.6"}
    return switcher.get(inches)

# GAMING
def w_gaming_D_A_HP_Le_inc(inches):
    switcher = {"1": "15.6", "2": "17.3"}
    return switcher.get(inches)

def w_gaming_MSI_inc(inches):
    switcher = {"1": "14.0", "2": "15.6", "3": "17.3", "4": "18.4"}
    return switcher.get(inches)

def w_gaming_Razer_inc(inches):
    switcher = {"1": "14.0", "2": "17.3"}
    return switcher.get(inches)

# NOTEBOOK
def w_notebook_D_inc(inches):
    switcher = {"1": "13.3", "2": "14.0", "3": "15.6", "4": "17.3"}
    return switcher.get(inches)

def w_notebook_Ac_Le_inc(inches):
    switcher = {"1": "11.6", "2": "13.3", "3": "14.0", "4": "15.6", "5": "17.3"}
    return switcher.get(inches)

def w_notebook_As_inc(inches):
    switcher = {"1": "13.3", "2": "14.0", "3": "14.1", "4": "15.6", "5": "17.3"}
    return switcher.get(inches)

def w_notebook_HP_inc(inches):
    switcher = {"1": "13.3", "2": "14.0", "3": "15.7", "4": "17.0", "5": "17.3"}
    return switcher.get(inches)

def w_notebook_Chu_inc(inches):
    switcher = {"1": "12.3", "2": "15.6"}
    return switcher.get(inches)

def w_notebook_Tos_inc(inches):
    switcher = {"1": "13.3", "2": "14.0", "3": "15.6"}
    return switcher.get(inches)

def w_notebook_Med_Ve_inc(inches):
    switcher = {"1": "13.3", "2": "14.0"}
    return switcher.get(inches)

# ULTRABOOK
def w_ultrabook_D_inc(inches):
    switcher = {"1": "12.5", "2": "13.3", "3": "14.0", "4": "15.6"}
    return switcher.get(inches)

def w_ultrabook_Ac_inc(inches):
    switcher = {"1": "13.3", "2": "14.0"}
    return switcher.get(inches)

def w_ultrabook_As_HP_inc(inches):
    switcher = {"1": "12.5", "2": "13.3", "3": "14.0", "4": "15.6"}
    return switcher.get(inches)

def w_ultrabook_Le_inc(inches):
    switcher = {"1": "12.5", "2": "14.0", "3": "15.6"}
    return switcher.get(inches)

def w_ultrabook_LG_inc(inches):
    switcher = {"1": "14.0", "2": "15.6"}
    return switcher.get(inches)

def w_ultrabook_Tos_inc(inches):
    switcher = {"1": "12.5", "2": "13.3", "3": "14.0"}
    return switcher.get(inches)

def w_ultrabook_Sam_inc(inches):
    switcher = {"1": "13.3", "2": "15.0"}
    return switcher.get(inches)

# NETBOOK
def w_netbook_HP_Le_inc(inches):
    switcher = {"1": "11.6", "2": "12.5"}
    return switcher.get(inches)

# WORKSTATION
def w_workstation_D_HP_inc(inches):
    switcher = {"1": "15.6", "2": "17.3"}
    return switcher.get(inches)

# NOTEBOOK
def w7_notebook_HP_inc(inches):
    switcher = {"1": "14.0", "2": "15.6"}
    return switcher.get(inches)

def w7_notebook_Le_inc(inches):
    switcher = {"1": "14.0", "2": "15.6", "3": "17.3"}
    return switcher.get(inches)

# NOTEBOOK
def nOS_workstation_Le_inc(inches):
    switcher = {"1": "15.6", "2": "17.3"}
    return switcher.get(inches)

# NOTEBOOK
def Li_notebook_Le_inc(inches):
    switcher = {"1": "14.0", "2": "15.6", "3": "17.3"}
    return switcher.get(inches)
