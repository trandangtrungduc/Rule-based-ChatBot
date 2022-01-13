import sys

from numpy.core.numeric import False_
sys.path.insert(0, 'E:/Project/ML_and_DL/CBD/ChatBot/~/ParlAI/')
import re, json
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
from parlai_internal.agents.laptopbot.Configuration.parameter_constants import *
from parlai_internal.agents.laptopbot.Configuration.notification import *
from parlai_internal.agents.laptopbot.Report.generate_invoice import create_invoice
from datetime import datetime
from parlai_internal.agents.laptopbot.Chart.plot_invoice import create_plot_invoice
from parlai_internal.agents.laptopbot.Report.generate_invoice import create_invoice
from parlai.core.agents import register_agent, Agent

class Laptop():

    def __init__(self, laptop_ID, Company, Product, TypeName, Inches, ScreenResolution, Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros):
        self.laptop_ID = laptop_ID
        self.Company = Company
        self.Product = Product
        self.TypeName = TypeName
        self.Inches = Inches
        self.ScreenResolution = ScreenResolution
        self.Cpu = Cpu
        self.Ram = Ram
        self.Memory = Memory
        self.GPU = GPU
        self.OpSys = OpSys
        self.Weight = Weight
        self.Price_euros = Price_euros

    def info(self):

        return (f'- Laptop ID: {self.laptop_ID}\n'
                f'- Company: {self.Company}\n'
                f'- Product: {self.Product}\n'
                f'- Type Name: {self.TypeName}\n'
                f'- Inches: {self.Inches}\n'
                f'- Screen Resolution: {self.ScreenResolution}\n'
                f'- CPU: {self.Cpu}\n'
                f'- Ram: {self.Ram}\n'
                f'- Memory: {self.Memory}\n'
                f'- GPU: {self.GPU}\n'
                f'- Operation System: {self.OpSys}\n'
                f'- Weight: {self.Weight}\n'
                f'- Price: {self.Price_euros}\n')

class Query():

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.db = msql.connect(host=self.host, database=self.database,
                               user=self.user, password=self.password)
        self.count = 0

    def query_check_info(self, OS, typeLap, origin, inches):
        merge_result = ""
        cursor = self.db.cursor()
        query_check =  "SELECT * FROM laptop_price_data WHERE OpSys = '%s' AND TypeName = '%s' AND Company = '%s' AND Inches = '%s'" %(OS, typeLap, origin, inches)
        try: 
            cursor.execute(query_check)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                merge_result = merge_result + "\n" + laptop.info()
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            return merge_result
        
    def query_ID(self, id):
        cursor = self.db.cursor()
        query_id = "SELECT * FROM laptop_price_data WHERE laptop_ID = '%s'" % (
            id)
        try:
            cursor.execute(query_id)
            results = cursor.fetchall()
            if results == []:
                return "Not found"
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
        except:
            print("Error fetching data.")
             
        finally:
            return laptop.info()
    
    def query_auto_Invoice(self, laptop_id):
        restructure = []
        cursor = self.db.cursor()
        query_month = "SELECT Company, Product, Cpu, Ram, Memory, Price_euros FROM laptop_price_data WHERE laptop_ID = '%s' ORDER BY laptop_ID" % (
            laptop_id)
        try:
            cursor.execute(query_month)
            result = list(cursor.fetchall()[0])
            restructure.append(result[0] + " - " + result[1])
            if result[2][11] == 'i':
                if result[4][6] == "S":
                    restructure.append(result[2][11:19] + '\n' + result[3] + '/' + result[4])
                else:
                    restructure.append(result[2][11:19] + '\n' + result[3] + '/' + result[4][0:6])
            else:
                if result[4][6] == "S":
                    restructure.append(result[2][0:14] + '\n' + result[3] + '/' + result[4])
                else:
                    restructure.append(result[2][0:14]+ '\n' + result[3] + '/' + result[4][0:6])
            restructure.append(result[5])
        except:
            print("Error fetching data.")
        return restructure

class Intent():
    def __init__(self, data_rule_based = './parlai_internal/agents/laptopbot/Data/intents_rule-based.json', key="default", match_intent=None, user_quant=0):
        self.rule_based = data_rule_based
        # Opening JSON file
        f = open(self.rule_based)
        self.rule_based = json.load(f)
        for intent, keys in self.rule_based['intents'][0].items():
            for i in range(0, len(keys)):
                keys[i] = '.*' + keys[i] + '.*'
            self.rule_based['intents'][0][intent] = re.compile('|'.join(keys))
        self.intents = self.rule_based['intents'][0]
        self.responses = self.rule_based['responses'][0]
        self.key = key
        self.match_intent = match_intent
        self.user_quant = user_quant

    def _find_intent(self, message):
        for intent, pattern in self.intents.items():
            if re.search(pattern, message):
                self.match_intent = intent
        if self.match_intent in self.responses:
            self.key = self.match_intent
        else:
            self.key = "default"
        return self.key

class CheckIn_Database():
    def __init__(self, host, database, user, password):
        self.host_checkIn = host
        self.database_checkIn = database
        self.user_checkIn = user
        self.password_checkIn = password
        self.db_checkIn = msql.connect(host=self.host_checkIn, database=self.database_checkIn,
                               user=self.user_checkIn, password=self.password_checkIn)
                               
    def _save_to_database(self, invoice_db):
        cursor = self.db_checkIn.cursor()
        insert_sql = "INSERT INTO auto_record_order.auto_record_order_data VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert_sql, tuple(invoice_db))
        self.db_checkIn.commit()

@register_agent("laptopbot")
class LaptopbotAgent(Agent, Intent, Query, CheckIn_Database):

    @classmethod
    def add_cmdline_args(cls, parser, partial_opt):
        parser.add_argument('--name', type=str, default='laptopbot', help="The agent's name.")
        return parser
        
    def __init__(self, opt, shared=None, Respond=None):
        # similar to the teacher, we have the Opt and the shared memory objects!
        super().__init__(opt, shared)
        Intent.__init__(self)
        Query.__init__(self, SERVER, DATABASE_LAPTOP, USER, PASSWORD)
        CheckIn_Database.__init__(self, SERVER, DATABASE_AUTO_RECORD_ORDER, USER, PASSWORD)
        self.decision = ""
        self.id = 'Laptopbot'
        self.name = opt['name']
        self.Respond = Respond
        # Help check information
        self.name_state = False
        self.user_name = "temp"
        self.welcome_state = False
        self.Osystem_key = False
        self.typeLab_key = False
        self.origin_key = False
        self.inches_key = False
        self.user_os = ""
        self.user_typeLab = ""
        self.user_origin = ""
        self.user_inches = ""
        # Help create an invoice
        self.user_laptopid = None
        self.quant = 0
        self.primary_invoice = False
        self.other_1 = False
        self.other_2 = False
        self.other_3 = False
        self.other_4 = False
        self.other_5 = False
        self.other_6 = False
        self.other_7 = False
        self.other_8 = False
        self.quantity_0 = False
        self.quantity_1 = False
        self.quantity_2 = False
        self.quantity_3 = False
        self.quantity_4 = False
        self.quantity_5 = False
        self.quantity_6 = False
        self.state_order = False
        # Store transcript
        self.transcript = []
        self.invoice = pd.DataFrame(columns=['Product', 'Information', 'Price', 'Quantity'])
        self.invoice_db = pd.DataFrame(columns=['Product', 'Information', 'Price', 'Quantity', 'Customer', "Time"])
        self.now = datetime.now()
        self.today = datetime.today().strftime("%d_%m_%Y")
        self.current_time = self.now.strftime("%Hh")
        
    def save_as_txt(self, content, who, user_name):
        with open("./parlai_internal/agents/laptopbot/Record/transcript_" + self.current_time + "_" + self.today + "_" + user_name +".txt", "a+") as file_object:
                file_object.seek(0)
                data = file_object.read(100)
                if len(data) > 0 :
                    file_object.write("\n")
                file_object.write(who + content)
    
    def _invoice(self, id_laptop, quantity):
        invoice_query = Query.query_auto_Invoice(self, id_laptop)
        invoice_query.append(quantity)
        self.invoice.loc[str(self.invoice.shape[0])] = invoice_query
        invoice_db = invoice_query
        invoice_db.append(self.user_name)
        invoice_db.append(self.today)
        CheckIn_Database._save_to_database(self, invoice_db)
        self.invoice_db.loc[str(self.invoice_db.shape[0])] = invoice_db
        self.invoice_db.to_csv("./Data/auto_record_order.csv", mode="a", index=False, header=False)
        
        
    def observe(self, observation):
        Query.__init__(self, SERVER, DATABASE_LAPTOP, USER, PASSWORD)
        message = observation.get('text', '')
        self.save_as_txt(message, "User: ", self.user_name)
        if self.name_state == True and self.welcome_state == True:
            Intent._find_intent(self,message)
            if self.key == "help":
                # Windows 10, 2 in 1 Convertible, Dell 
                if message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Dell" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "11.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Dell" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.5"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Dell" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Dell" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Dell" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "6" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Dell" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Dell"
                    self.Respond = "How many inches do you want the screen to be? (11.6, 12.5, 13.3, 15, 15.6, 17.3 inches)\n Please press key 1 to 6 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, 2 in 1 Convertible, Acer 
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Acer" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "11.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Acer" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Acer" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Acer"
                    self.Respond = "How many inches do you want the screen to be? (11.6, 13.3, 14 inches)\n Please press key 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Windows 10, 2 in 1 Convertible, Asus 
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "11.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Asus"
                    self.Respond = "How many inches do you want the screen to be? (11.6, 13.3, 15.6 inches)\n Please press key 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Windows 10, 2 in 1 Convertible, HP 
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "11.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "HP"
                    self.Respond = "How many inches do you want the screen to be? (11.6, 13.3, 14, 15.6 inches)\n Please press key 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, 2 in 1 Convertible, Lenovo 
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "10.1"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "11.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.9"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "6" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Lenovo"
                    self.Respond = "How many inches do you want the screen to be? (10.1, 11.3, 13.3, 13.9, 14, 15.6 inches)\n Please press key 1 to 6 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, 2 in 1 Convertible, Samsung 
                elif message == "6" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Samsung"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.0")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, 2 in 1 Convertible, Mediacom 
                elif message == "7" and self.user_os == "Windows 10" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Mediacom"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, 2 in 1 Convertible          
                elif message == "1" and self.user_os == "Windows 10" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "2 in 1 Convertible"
                    self.Respond = "With origin of laptop, we have the following 7 categories: Dell, Acer, Asus, HP, Lenovo, Samsung, Mediacom\n Please press from 1 to 7 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Gaming, Dell
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Dell"
                    self.Respond = "How many inches do you want the screen to be? (15.6, 17.3 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Gaming, Acer
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Acer"
                    self.Respond = "How many inches do you want the screen to be? (15.6, 17.3 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Gaming, Asus
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Asus"
                    self.Respond = "How many inches do you want the screen to be? (15.6, 17.3 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Gaming, HP
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "HP"
                    self.Respond = "How many inches do you want the screen to be? (15.6, 17.3 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Gaming, Lenovo
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Lenovo"
                    self.Respond = "How many inches do you want the screen to be? (15.6, 17.3 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Gaming, MSI
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "MSI"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "MSI"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "MSI"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "MSI"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "18.4"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "6" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "MSI"
                    self.Respond = "How many inches do you want the screen to be? (14, 15.6, 17.3, 18.4)?\n Please press key 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Gaming, Razer
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "Razer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.user_origin == "Razer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "7" and self.user_os == "Windows 10" and self.user_typeLab == "Gaming" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Razer"
                    self.Respond = "How many inches do you want the screen to be? (14, 17.3 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Gaming 
                elif message == "2" and self.user_os == "Windows 10" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Gaming"
                    self.Respond = "With origin of laptop, we have the following 11 categories: Dell, Acer, Asus, HP, Lenovo, MSI, Razer\n Please press from 1 to 7 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Notebook, Dell
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Dell"
                    self.Respond = "How many inches do you want the screen to be? (13.3, 14, 15.6, 17.3 inches)?\n Please press key 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Notebook, Acer
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "11.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Acer"
                    self.Respond = "How many inches do you want the screen to be? (11.6, 13.3, 14, 15.6, 17.3 inches)?\n Please press key 1 to 5 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Notebook, Asus
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.1"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Asus"
                    self.Respond = "How many inches do you want the screen to be? (13.3, 14, 14.1, 15.6, 17.3 inches)?\n Please press key 1 to 5 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Notebook, HP
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "HP"
                    self.Respond = "How many inches do you want the screen to be? (13.3, 14, 15.6, 17, 17.3 inches)?\n Please press key 1 to 5 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Notebook, Lenovo
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "11.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Lenovo"
                    self.Respond = "How many inches do you want the screen to be? (11.6, 13.3, 14, 15.6, 17.3 inches)?\n Please press key 1 to 5 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Notebook, Chuwi
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Chuwi"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Chuwi"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "6" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Chuwi"
                    self.Respond = "How many inches do you want the screen to be? (12.3, 15.6 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
            
                # Windows 10, Notebook, Fujitsu
                elif message == "7" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key == True and self.inches_key == False and self.origin_key == True:
                    self.typeLab_key, self.Osystem_key, self.origin_key = False, False, False
                    self.user_origin = "Fujitsu"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Notebook, Toshiba
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Toshiba"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Toshiba"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Toshiba"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "8" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Toshiba"
                    self.Respond = "How many inches do you want the screen to be? (13.3, 14.0, 15.6 inches)?\n Please press key 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Notebook, Samsung
                elif message == "9" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key == True and self.inches_key == False and self.origin_key == True:
                    self.typeLab_key, self.Osystem_key, self.origin_key = False, False, False
                    self.user_origin = "Samsung"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Notebook, Mediacom
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Mediacom"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Mediacom"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "10" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Mediacom"
                    self.Respond = "How many inches do you want the screen to be? (13.3, 14.0 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Notebook, Vero
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Vero"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.user_origin == "Vero"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "11" and self.user_os == "Windows 10" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Vero"
                    self.Respond = "How many inches do you want the screen to be? (13.3, 14.0 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
            
                # Windows 10, Notebook 
                elif message == "3" and self.user_os == "Windows 10" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Notebook"
                    self.Respond = "With origin of laptop, we have the following 11 categories: Dell, Acer, Asus, HP, Lenovo, Chuwi, Fujitsu, Toshiba, Samsung, Mediacom, Vero\n Please press from 1 to 11 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, Dell
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.5"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Dell"
                    self.Respond = "How many inches do you want the screen to be? (12.5, 13.3, 14, 15.6 inches)?\n Please press key 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, Acer
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Acer"
                    self.Respond = "How many inches do you want the screen to be? (13.3, 14 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, Asus
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.5"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Asus"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Asus"
                    self.Respond = "How many inches do you want the screen to be? (12.5, 13.3, 14.0, 15.6 inches)?\n Please press key 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, HP
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.5"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "HP"
                    self.Respond = "How many inches do you want the screen to be? (12.5, 13.3, 14.0, 15.6 inches)?\n Please press key 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, Lenovo
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.5"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Lenovo"
                    self.Respond = "How many inches do you want the screen to be? (12.5, 14.0, 15.6 inches)?\n Please press key 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, Huawei
                elif message == "6" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Huawei"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "13.0")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, LG
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "LG"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "LG"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "7" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "LG"
                    self.Respond = "How many inches do you want the screen to be? (14.0, 15.6 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, Toshiba
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Toshiba"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.5"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Toshiba"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Toshiba"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "8" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Toshiba"
                    self.Respond = "How many inches do you want the screen to be? (12.5, 13.3, 14 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, Samsung
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Samsung"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.user_origin == "Samsung"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "9" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Samsung"
                    self.Respond = "How many inches do you want the screen to be? (13.3, 15.0 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, Xiaomi
                elif message == "10" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Xiaomi"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "13.3")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Ultrabook, Razer
                elif message == "11" and self.user_os == "Windows 10" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Razer"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "12.5")   
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Windows 10, Ultrabook 
                elif message == "4" and self.user_os == "Windows 10" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Ultrabook"
                    self.Respond = "With origin of laptop, we have the following 11 categories: Dell, Acer, Asus, HP, Lenovo, Huawei, LG, Toshiba, Samsung, Xiaomi, Razer\n Please press from 1 to 11 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Netbook, Dell
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Dell"
                    self.Respond =  Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Netbook, Acer
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Acer"
                    self.Respond =  Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Netbook, Asus
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Asus"
                    self.Respond =  Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Netbook, HP
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Netbook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "11.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Netbook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.5"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Windows 10" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "HP"
                    self.Respond = "How many inches do you want the screen to be? (11.6, 12.5 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Netbook, Lenovo
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Netbook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "11.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Netbook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.5"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "5" and self.user_os == "Windows 10" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Lenovo"
                    self.Respond = "How many inches do you want the screen to be? (11.6, 12.5 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Netbook 
                elif message == "5" and self.user_os == "Windows 10" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Netbook"
                    self.Respond = "With origin of laptop, we have the following 5 categories: Dell, Acer, Asus, HP, Lenovo\n Please press from 1 to 5 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Workstation, Dell
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Workstation" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Workstation" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Workstation" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Dell"
                    self.Respond = "How many inches do you want the screen to be? (15.6, 17.3 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Workstation, HP
                elif message == "1" and self.user_os == "Windows 10" and self.user_typeLab == "Workstation" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Workstation" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 10" and self.user_typeLab == "Workstation" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "HP"
                    self.Respond = "How many inches do you want the screen to be? (15.6, 17.3 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Workstation, Lenovo
                elif message == "3" and self.user_os == "Windows 10" and self.user_typeLab == "Workstation" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Lenovo"
                    self.Respond =  Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10, Workstation 
                elif message == "6" and self.user_os == "Windows 10" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Workstation"
                    self.Respond = "With origin of laptop, we have the following 3 categories: Dell, HP, Lenovo\n Please press from 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Windows 10
                elif message == '1' and self.Osystem_key == True and self.typeLab_key== False and self.inches_key == False and self.origin_key == False:
                    self.typeLab_key = True
                    self.user_os = "Windows 10"
                    self.Respond = "With type of laptop, we have the following 6 categories: 2 in 1 Convertible, Gaming, Notebook, Ultrabook, Netbook, Workstation.\n Please press from 1 to 6 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10 S, Notebook
                elif message == "1" and self.user_os == "Windows 10 S" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.Osystem_key, self.typeLab_key = False, False
                    self.user_typeLab = "Notebook"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, "Asus", "14.0")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10 S, Ultrabook
                elif message == "2" and self.user_os == "Windows 10 S" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.Osystem_key, self.typeLab_key = False, False
                    self.user_typeLab = "Ultrabook"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, "Microsoft", "13.5")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 10 S, Netbook
                elif message == "3" and self.user_os == "Windows 10 S" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.Osystem_key, self.typeLab_key = False, False
                    self.user_typeLab = "Netbook"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, "Asus", "11.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Windows 10 S
                elif message == '2' and self.Osystem_key == True and self.typeLab_key== False and self.inches_key == False and self.origin_key == False:
                    self.typeLab_key = True
                    self.user_os = "Windows 10 S"
                    self.Respond = "With type of laptop, we have the following 3 categories: Notebook, Ultrabook, Netbook.\n Please press from 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7, 2 in 1 Convertible
                elif message == "1" and self.user_os == "Windows 7" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.Osystem_key, self.typeLab_key= False, False
                    self.user_typeLab = "2 in 1 Convertible" 
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, "Lenovo", "14.0")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Windows 7, Notebook, Dell
                elif message == "1" and self.user_os == "Windows 7" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Dell"
                    self.Respond =  Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Windows 7, Notebook, HP
                elif message == "1" and self.user_os == "Windows 7" and self.user_typeLab == "Notebook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 7" and self.user_typeLab == "Notebook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 7" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "HP"
                    self.Respond = "How many inches do you want the screen to be? (14.0, 15.6 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7, Notebook, Lenovo
                elif message == "1" and self.user_os == "Windows 7" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 7" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 7" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 7" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Lenovo"
                    self.Respond = "How many inches do you want the screen to be? (14.0, 15.6, 17.3 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7, Notebook, Toshiba
                elif message == "4" and self.user_os == "Windows 7" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Toshiba"
                    self.Respond =  Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "13.3") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Windows 7, Notebook 
                elif message == "2" and self.user_os == "Windows 7" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Notebook"
                    self.Respond = "With origin of laptop, we have the following 4 categories: Dell, HP, Lenovo, Toshiba\n Please press from 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7, Netbook
                elif message == "3" and self.user_os == "Windows 7" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.Osystem_key, self.typeLab_key = False, False
                    self.user_typeLab = "Netbook"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, "HP", "12.5")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Windows 7, Ultrabook, Dell
                elif message == "1" and self.user_os == "Windows 7" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Dell"
                    self.Respond =  Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "12.5") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7, Ultrabook, HP
                elif message == "1" and self.user_os == "Windows 7" and self.user_typeLab == "Ultrabook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.5"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 7" and self.user_typeLab == "Ultrabook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Windows 7" and self.user_typeLab == "Ultrabook" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Windows 7" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "HP"
                    self.Respond = "How many inches do you want the screen to be? (12.5, 14.0, 15.6 inches)?\n Please press key 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7, Ultrabook, Lenovo
                elif message == "3" and self.user_os == "Windows 7" and self.user_typeLab == "Ultrabook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Lenovo"
                    self.Respond =  Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "14.0") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7, Ultrabook 
                elif message == "4" and self.user_os == "Windows 7" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Ultrabook"
                    self.Respond = "With origin of laptop, we have the following 3 categories: Dell, HP, Lenovo.\n Please press from 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7, Workstation, HP
                elif message == "1" and self.user_os == "Windows 7" and self.user_typeLab == "Workstation" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "1" and self.user_os == "Windows 7" and self.user_typeLab == "Workstation" and self.user_origin == "HP"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "1" and self.user_os == "Windows 7" and self.user_typeLab == "Workstation" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "HP"
                    self.Respond = "How many inches do you want the screen to be? (15.6, 17.3 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7, Workstation, Lenovo
                elif message == "2" and self.user_os == "Windows 7" and self.user_typeLab == "Workstation" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key= False, False, False
                    self.user_origin = "Lenovo"
                    self.Respond =  Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7, Workstation 
                elif message == "5" and self.user_os == "Windows 7" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Workstation"
                    self.Respond = "With origin of laptop, we have the following 2 categories: HP, Lenovo.\n Please press from 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Windows 7
                elif message == '3' and self.Osystem_key == True and self.typeLab_key== False and self.inches_key == False and self.origin_key == False:
                    self.typeLab_key = True
                    self.user_os = "Windows 7"
                    self.Respond = "With type of laptop, we have the following 5 categories: 2 in 1 Convertible, Notebook, Netbook, Ultrabook, Workstation.\n Please press from 1 to 5 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # macOS, Ultrabook, Apple
                elif message == "1" and self.user_os == "macOS" and self.user_typeLab == "Ultrabook" and self.user_origin == "Apple"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "macOS" and self.user_typeLab == "Ultrabook" and self.user_origin == "Apple"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.4"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # macOS
                elif message == '4' and self.Osystem_key == True and self.typeLab_key== False and self.inches_key == False and self.origin_key == False:
                    self.typeLab_key = True
                    self.origin_key = True
                    self.inches_key = True
                    self.user_os = "macOS"
                    self.user_typeLab = "Ultrabook"
                    self.user_origin = "Apple"
                    self.Respond = "With type of laptop, we have only 1 category: Ultrabook from Apple company.\nHow many inches do you want the screen to be? (13.3, 15.4 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Mac OS X, Ultrabook, Apple
                elif message == "1" and self.user_os == "Mac OS X" and self.user_typeLab == "Ultrabook" and self.user_origin == "Apple"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "11.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Mac OS X" and self.user_typeLab == "Ultrabook" and self.user_origin == "Apple"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "12.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Mac OS X" and self.user_typeLab == "Ultrabook" and self.user_origin == "Apple"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "13.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "4" and self.user_os == "Mac OS X" and self.user_typeLab == "Ultrabook" and self.user_origin == "Apple"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.4"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Mac OS X
                elif message == '5' and self.Osystem_key == True and self.typeLab_key== False and self.inches_key == False and self.origin_key == False:
                    self.typeLab_key = True
                    self.origin_key = True
                    self.inches_key = True
                    self.user_os = "Mac OS X"
                    self.user_typeLab = "Ultrabook"
                    self.user_origin = "Apple"
                    self.Respond = "With type of laptop, we have only 1 category: Ultrabook from Apple company.\nHow many inches do you want the screen to be? (11.6, 12.0, 13.3, 15.4 inches)?\n Please press key 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # No OS, Gaming, Lenovo 
                elif message == "1" and self.user_os == "No OS" and self.user_typeLab == "Gaming" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Lenovo"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                elif message == "2" and self.user_os == "No OS" and self.user_typeLab == "Gaming" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Asus"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6") + "\n" + Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "17.3")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # No OS, Gaming 
                elif message == "1" and self.user_os == "No OS" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Gaming"
                    self.Respond = "With origin of laptop, we have the following 2 categories: Lenovo, Asus\n Please press from 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # No OS, Notebook, Asus 
                elif message == "1" and self.user_os == "No OS" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Asus"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6") + "\n" + Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "17.3")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # No OS, Notebook, HP 
                elif message == "2" and self.user_os == "No OS" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "HP"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # No OS, Notebook, Lenovo 
                elif message == "1" and self.user_os == "No OS" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "No OS" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "No OS" and self.user_typeLab == "Notebook" and self.user_origin == "Lenovo"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "No OS" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Lenovo"
                    self.Respond = "How many inches do you want the screen to be? (14.0 15.6, 17.3 inches)?\n Please press key 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # No OS, Notebook, Xiaomi 
                elif message == "4" and self.user_os == "No OS" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Xiaomi"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # No OS, Notebook 
                elif message == "2" and self.user_os == "No OS" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Notebook"
                    self.Respond = "With origin of laptop, we have the following 4 categories: Asus, HP, Lenovo, Xiaomi\n Please press from 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # No OS, Ultrabook 
                elif message == "3" and self.user_os == "No OS" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.Osystem_key, self.typeLab_key = False, False
                    self.user_typeLab = "Ultrabook"
                    self.user_origin = "Xiaomi"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "13.3") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # No OS
                elif message == '6' and self.Osystem_key == True and self.typeLab_key== False and self.inches_key == False and self.origin_key == False:
                    self.typeLab_key = True
                    self.user_os = "No OS"
                    self.Respond = "With type of laptop, we have the following 3 categories: Gaming, Notebook, Ultrabook.\n Please press from 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Linux, Gaming 
                elif message == "1" and self.user_os == "Linux" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.Osystem_key, self.typeLab_key = False, False
                    self.user_typeLab = "Gaming"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, "Asus", "17.3") + "\n" + Query.query_check_info(self, self.user_os, self.user_typeLab, "Acer", "15.6") + Query.query_check_info(self, self.user_os, self.user_typeLab, "Dell", "15.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Linux, Notebook, Acer 
                elif message == "1" and self.user_os == "Linux" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Acer"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Linux, Notebook, Asus 
                elif message == "2" and self.user_os == "Linux" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Asus"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "15.6") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Linux, Notebook, Dell 
                elif message == "1" and self.user_os == "Linux" and self.user_typeLab == "Notebook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Linux" and self.user_typeLab == "Notebook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Linux" and self.user_typeLab == "Notebook" and self.user_origin == "Dell"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "17.3"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "3" and self.user_os == "Linux" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Dell"
                    self.Respond = "How many inches do you want the screen to be? (14.0 15.6, 17.3 inches)?\n Please press key 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Linux, Notebook 
                elif message == "2" and self.user_os == "Linux" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Notebook"
                    self.Respond = "With origin of laptop, we have the following 3 categories: Acer, Asus, Dell\n Please press from 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Linux, Ultrabook 
                elif message == "3" and self.user_os == "Linux" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.Osystem_key, self.typeLab_key = False, False
                    self.user_typeLab = "Ultrabook"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, "Dell", "13.3") + "\n" + Query.query_check_info(self, self.user_os, self.user_typeLab, "Dell", "14.0") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Linux
                elif message == '7' and self.Osystem_key == True and self.typeLab_key== False and self.inches_key == False and self.origin_key == False:
                    self.typeLab_key = True
                    self.user_os = "Linux"
                    self.Respond = "With type of laptop, we have the following 3 categories: Gaming, Notebook, Ultrabook.\n Please press from 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Android
                elif message == '8' and self.Osystem_key == True and self.typeLab_key== False and self.inches_key == False and self.origin_key == False:
                    self.Osystem_key = False
                    self.user_os = "Android"
                    self.user_typeLab = "2 in 1 Convertible"
                    self.user_origin = "Lenovo"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "10.1")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Chrome OS, 2 in 1 Convertible, Acer
                elif message == "1" and self.user_os == "Chrome OS" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Acer"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Chrome OS, 2 in 1 Convertible, Asus
                elif message == "2" and self.user_os == "Chrome OS" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Asus"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "12.5")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Chrome OS, 2 in 1 Convertible, HP
                elif message == "3" and self.user_os == "Chrome OS" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "HP"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Chrome OS, 2 in 1 Convertible, Samsung
                elif message == "4" and self.user_os == "Chrome OS" and self.user_typeLab == "2 in 1 Convertible" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Samsung"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "12.3")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Chrome OS, 2 in 1 Convertible
                elif message == "1" and self.user_os == "Chrome OS" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "2 in 1 Convertible"
                    self.Respond = "With origin of laptop, we have the following 4 categories: Acer, Asus, HP, Samung\n Please press from 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Chrome OS, Netbook, Acer
                elif message == "1" and self.user_os == "Chrome OS" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Acer"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Chrome OS, Netbook, Asus
                elif message == "2" and self.user_os == "Chrome OS" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Asus"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Chrome OS, Netbook, HP
                elif message == "3" and self.user_os == "Chrome OS" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "HP"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Chrome OS, Netbook, Samsung
                elif message == "4" and self.user_os == "Chrome OS" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Samsung"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Chrome OS, Netbook, Dell
                elif message == "5" and self.user_os == "Chrome OS" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Dell"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Chrome OS, Netbook, Lenovo
                elif message == "6" and self.user_os == "Chrome OS" and self.user_typeLab == "Netbook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Lenovo"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "11.6")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Chrome OS, Netbook
                elif message == "2" and self.user_os == "Chrome OS" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Netbook"
                    self.Respond = "With origin of laptop, we have the following 6 categories: Acer, Asus, HP, Samsung, Dell, Lenovo\n Please press from 1 to 6 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
            
                # Chrome OS, Notebook, Acer
                elif message == "1" and self.user_os == "Chrome OS" and self.user_typeLab == "Notebook" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "14.0"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "2" and self.user_os == "Chrome OS" and self.user_typeLab == "Notebook" and self.user_origin == "Acer"  and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == True and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key, self.inches_key = False, False, False, False
                    self.user_inches = "15.6"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, self.user_inches)
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "1" and self.user_os == "Chrome OS" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.inches_key = True
                    self.user_origin = "Acer"
                    self.Respond = "How many inches do you want the screen to be? (14.0 15.6 inches)?\n Please press key 1 to 2 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Chrome OS, Notebook, HP
                elif message == "2" and self.user_os == "Chrome OS" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "HP"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "13.3")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Chrome OS, Notebook, Lenovo
                elif message == "3" and self.user_os == "Chrome OS" and self.user_typeLab == "Notebook" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == True:
                    self.Osystem_key, self.typeLab_key, self.origin_key = False, False, False
                    self.user_origin = "Lenovo"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "13.3") + "\n" + Query.query_check_info(self, self.user_os, self.user_typeLab, self.user_origin, "14.0")
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                # Chrome OS, Notebook
                elif message == "3" and self.user_os == "Chrome OS" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.origin_key = True
                    self.user_typeLab = "Notebook"
                    self.Respond = "With origin of laptop, we have the following 3 categories: Acer, HP, Lenovo\n Please press from 1 to 3 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)

                # Chrome OS, Ultrabook 
                elif message == "4" and self.user_os == "Chrome OS" and self.Osystem_key == True and self.typeLab_key== True and self.inches_key == False and self.origin_key == False:
                    self.Osystem_key, self.typeLab_key = False, False
                    self.user_typeLab = "Ultrabook"
                    self.Respond = Query.query_check_info(self, self.user_os, self.user_typeLab, "Google", "12.3") 
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                    
                # Chrome OS
                elif message == '9' and self.Osystem_key == True and self.typeLab_key== False and self.inches_key == False and self.origin_key == False:
                    self.typeLab_key = True
                    self.user_os = "Chrome OS"
                    self.Respond = "With type of laptop, we have the following 4 categories: 2 in 1 Convertible, Netbook, Notebook, Ultrabook.\n Please press from 1 to 4 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                
                else:
                    self.Osystem_key = True
                    self.Respond = "We have the following 9 categories: Windows 10, Window 10 S, Window 7, macOS, Mac OS X, No OS, Linux, Android, or Chrome\n Please press from 1 to 9 for the respective categories above"
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
            
            elif self.key == "invoice":
                # Order four laptops
                # if self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == True and self.quantity_3 == True and self.quantity_4 == True and self.quantity_5 == False and self.other_1 == True and self.other_2 == True and self.other_3 == True and self.other_4 == True and self.other_5 == True and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == True:
                #     self.state_order = False
                #     self.other_6 = True
                #     self.Respond = "You have successfully ordered " + message + " laptops with the above ID. Do you want to order another laptop? Please type 'Yes' or 'No'."
                # elif self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == True and self.quantity_3 == True and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == True and self.other_2 == True and self.other_3 == True and self.other_4 == True and self.other_5 == True and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == True:
                #     self.quantity_4 = True
                #     self.Respond = Query.query_ID(self, message) + "\n" + "Please enter quantity for this laptop (limit from 1 to 100)."
                # elif message == "Yes" and self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == True and self.quantity_3 == True and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == True and self.other_2 == True and self.other_3 == True and self.other_4 == True and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == False:
                #     self.state_order = True
                #     self.other_5 = True
                #     self.Respond = "Please enter the ID of the laptop (limit from 1 to 1320) you want to create an invoice."
                if message == "No" and self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == True and self.quantity_3 == True and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == True and self.other_2 == True and self.other_3 == True and self.other_4 == True and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == False:
                    self.primary_invoice, self.quantity_0, self.quantity_1, self.quantity_2, self.quantity_3, self.other_1, self.other_2, self.other_3, self.other_4 = False, False, False, False, False, False, False, False, False
                    self.Respond = "You have ordered 4 types of laptop. Thank you for using our service. \n Please enter 'help' if you want to check information of laptop or enter 'invoice' if you want to create an invoice or enter '[EXIT]' if you want to end the conversation."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                    self._invoice(self.user_laptopid, self.quant)
                    create_plot_invoice(self.invoice)
                    create_invoice()
                
                # Order three laptops
                if self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == True and self.quantity_3 == True and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == True and self.other_2 == True and self.other_3 == True and self.other_4 == False and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == True:
                    self.state_order = False
                    self.quant = message
                    self.other_4 = True
                    self.Respond = "You have successfully ordered " + message + " laptops with the above ID. Do you want to order another laptop? Please type 'Yes' or 'No'."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == True and self.quantity_3 == False and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == True and self.other_2 == True and self.other_3 == True and self.other_4 == False and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == True:
                    self.quantity_3 = True
                    self.user_laptopid = message
                    self.Respond = Query.query_ID(self, message) + "\n" + "Please enter quantity for this laptop (limit from 1 to 100)."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif message == "Yes" and self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == True and self.quantity_3 == False and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == True and self.other_2 == True and self.other_3 == False and self.other_4 == False and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == False:
                    self.state_order = True
                    self.other_3 = True
                    self.Respond = "Please enter the ID of the laptop (limit from 1 to 1320) you want to create an invoice."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                    self._invoice(self.user_laptopid, self.quant)
                elif message == "No" and self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == True and self.quantity_3 == False and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == True and self.other_2 == True and self.other_3 == False and self.other_4 == False and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == False:
                    self.primary_invoice, self.quantity_0, self.quantity_1, self.quantity_2, self.other_1, self.other_2 = False, False, False, False, False, False
                    self.Respond = "You have ordered 2 types of laptop. Thank you for using our service. \n Please enter 'help' if you want to check information of laptop or enter 'invoice' if you want to create an invoice or enter '[EXIT]' if you want to end the conversation."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                    self._invoice(self.user_laptopid, self.quant)
                    create_plot_invoice(self.invoice)
                    create_invoice()
                
                # Order two laptops
                elif self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == True and self.quantity_3 == False and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == True and self.other_2 == False and self.other_3 == False and self.other_4 == False and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == True:
                    self.state_order = False
                    self.quant = message
                    self.other_2 = True
                    self.Respond = "You have successfully ordered " + message + " laptops with the above ID. Do you want to order another laptop? Please type 'Yes' or 'No'."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name) 
                elif self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == False and self.quantity_3 == False and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == True and self.other_2 == False and self.other_3 == False and self.other_4 == False and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == True:
                    self.quantity_2 = True
                    self.user_laptopid = message
                    self.Respond = Query.query_ID(self, message) + "\n" + "Please enter quantity for this laptop (limit from 1 to 100)."
                elif message == "Yes" and self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == False and self.quantity_3 == False and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == False and self.other_2 == False and self.other_3 == False and self.other_4 == False and self.other_5 ==  False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == False:
                    self.state_order = True
                    self.other_1 = True
                    self.Respond = "Please enter the ID of the laptop (limit from 1 to 1320) you want to create an invoice."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                    self._invoice(self.user_laptopid, self.quant)
                elif message == "No" and self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == True and self.quantity_2 == False and self.quantity_3 == False and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == False and self.other_2 == False and self.other_3 == False and self.other_4 == False and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == False:
                    self.primary_invoice, self.quantity_0, self.quantity_1 = False, False, False
                    self.Respond = "You have ordered 1 type of laptop. Thank you for using our service. \n Please enter 'help' if you want to check information of laptop or enter 'invoice' if you want to create an invoice or enter '[EXIT]' if you want to end the conversation."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                    self._invoice(self.user_laptopid, self.quant)
                    create_plot_invoice(self.invoice)
                    create_invoice()
                
                # Only a laptop
                elif self.primary_invoice == True and self.quantity_0 == True and self.quantity_1 == False and self.quantity_2 == False and self.quantity_3 == False and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == False and self.other_2 == False and self.other_3 == False and self.other_4 == False and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == False:
                    self.quantity_1 = True
                    self.quant = message
                    self.Respond = "You have successfully ordered " + message + " laptops with the above ID. Do you want to order another laptop? Please type 'Yes' or 'No'."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                elif self.primary_invoice == True and self.quantity_0 == False and self.quantity_1 == False and self.quantity_2 == False and self.quantity_3 == False and self.quantity_4 == False and self.quantity_5 == False and self.other_1 == False and self.other_2 == False and self.other_3 == False and self.other_4 == False and self.other_5 == False and self.other_6 == False and self.other_7 == False and self.other_8 == False and self.state_order == False:
                    self.quantity_0 = True
                    self.user_laptopid = message
                    self.Respond = Query.query_ID(self, message) + "\n" + "Please enter quantity for this laptop (limit from 1 to 100)."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
                else:
                    self.primary_invoice = True
                    self.Respond = "Please enter the ID of the laptop (limit from 1 to 1320) you want to create an invoice. If you don't know the ID of laptop, you can check the laptop information by typing 'help'."
                    self.save_as_txt(self.Respond, "Bot: ", self.user_name)
            
            else:
                self.Respond = "Please enter 'help' if you want to check information of laptop or enter 'invoice' if you want to create an invoice or enter '[EXIT]' if you want to end the conversation."
                self.save_as_txt(self.Respond, "Bot: ", self.user_name)
        elif self.name_state == True and self.welcome_state == False:
            self.welcome_state = True
            self.user_name = message
            self.Respond = "Welcome " + self.user_name + " to the chatbot service."
            self.save_as_txt(self.Respond, "Bot: ", self.user_name)
        else:
            self.name_state = True
            self.Respond = "Please tell us your name!"
            self.save_as_txt(self.Respond, "Bot: ", self.user_name)
        
            
        

        
    
    def act(self):
        return {
            'id': self.id,
            'text': self.Respond,
        }



