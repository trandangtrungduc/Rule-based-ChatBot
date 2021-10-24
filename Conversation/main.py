import sys
sys.path.insert(0, 'E:/Project/ML_and_DL/CBD/Chatbot/')
from Configuration.parameter_constants import *
import re
import json
import nltk
from nltk.corpus import wordnet
from Database.function_retrieve_data import Query


class Intent():
    def __init__(self, data_rule_based, key="default", match_intent=None):
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

    def _find_intent(self, message):
        for intent, pattern in self.intents.items():
            if re.search(pattern, message):
                self.match_intent = intent
        if self.match_intent in self.responses:
            self.key = self.match_intent
        else:
            self.key = "default"
        return "BOT: " + self.responses[self.key]


class Help(Query):
    def __init__(self, user_help, user_os=None, user_typeLab=None, user_company=None, user_inches=None):
        Query.__init__(self, SERVER, DATABASE_LAPTOP, USER, PASSWORD)
        self.user_help = user_help
        self.user_os = user_os
        self.user_typeLab = user_typeLab
        self.user_company = user_company
        self.user_inches = user_inches

    def _help_process(self, user_help):
        self.user_help = user_help
        if self.user_help == 'info':
            print("BOT: Which operating system laptop do you want to choose? (Window, macOS, noOS, Linux, Android, or Chrome)")
            self.user_os = input("User: ")

            # WINDOWS 10
            if re.search(".*win.*", self.user_os):
                print(
                    "BOT: With windows operating system, we have the following 3 categories: Window 10, Window 10 S, Window 7")
                flag_os = True
                while flag_os == True:
                    print(
                        "BOT: Please press from 1 (Window 10), 2 (Window 10 S) or 3 (Window 7) that you want to check the information")
                    self.user_os = input("User: ")
                    if self.user_os in ["1", "2", "3"]:
                        flag_os = False
                if self.user_os == "1":
                    print("BOT: With type of laptop, we have the following 6 categories: 2 in 1 Convertible, Gaming, Notebook, Netbook, Ultrabook, Workstation")
                    self.user_os = "Windows 10"
                    flag_type = True
                    while flag_type == True:
                        print(
                            "BOT: Please press from 1 to 6 for the respective categories above")
                        self.user_typeLab = input("User: ")
                        if self.user_typeLab in ["1", "2", "3", "4", "5", "6"]:
                            flag_type = False
                    if self.user_typeLab == "1":
                        self.user_typeLab = "2 in 1 Convertible"
                        flag_ori = True
                        while flag_ori == True:
                            print(
                        "BOT: With origin of laptop, we have the following 7 categories: Dell, Acer, Asus, HP, Lenovo, Samsung, Mediacom")
                            print(
                                "BOT: Please press from 1 to 7 for the respective categories above")
                            self.user_company = input("User: ")
                            if self.user_company in ["1", "2", "3", "4", "5", "6", "7"]:
                                flag_ori = False
                        if self.user_company == "1":
                            print(
                            "BOT: How many inches do you want the screen to be? (11.6, 12.5, 13.3, 15, 15.6, 17.3 inches)")
                            self.user_company = "Dell"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 6 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4", "5", "6"]:
                                    flag_inc = False
                            self.user_inches = w_2in1_D_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "2":
                            print(
                            "BOT: How many inches do you want the screen to be? (11.6, 13.3, 14 inches)")
                            self.user_company = "Acer"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 3 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3"]:
                                    flag_inc = False
                            self.user_inches = w_2in1_Ac_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "3":
                            print(
                            "BOT: How many inches do you want the screen to be? (11.6, 13.3, 15.6 inches)")
                            self.user_company = "Asus"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 3 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3"]:
                                    flag_inc = False
                            self.user_inches = w_2in1_As_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "4":
                            print(
                            "BOT: How many inches do you want the screen to be? (11.6, 13.3, 14, 15.6 inches)")
                            self.user_company = "HP"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 4 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4"]:
                                    flag_inc = False
                            self.user_inches = w_2in1_HP_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "5":
                            print(
                            "BOT: How many inches do you want the screen to be? (10.1, 11.3, 13.3, 13.9, 14, 15.6 inches)")
                            self.user_company = "Lenovo"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 6 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4", "5", "6"]:
                                    flag_inc = False
                            self.user_inches = w_2in1_HP_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "6":
                            print("BOT: Unfortunately, we only have 1 laptop")
                            self.user_company = "Samsung"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "15.0")
                        elif self.user_company == "7":
                            print("BOT: Unfortunately, we only have 1 laptop")
                            self.user_company = "Mediacom"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "11.6")
            
                    # GAMING
                    elif self.user_typeLab == "2":
                        self.user_typeLab = "Gaming"
                        flag_ori = True
                        while flag_ori == True:
                            print(
                        "BOT: With origin of laptop, we have the following 7 categories: Dell, Acer, Asus, HP, Lenovo, MSI, Razer")
                            print(
                                "BOT: Please press from 1 to 7 for the respective categories above")
                            self.user_company = input("User: ")
                            if self.user_company in ["1", "2", "3", "4", "5", "6", "7"]:
                                flag_ori = False
                        if self.user_company == "1":
                            print(
                            "BOT: How many inches do you want the screen to be? (15.6, 17.3 inches)")
                            self.user_company = "Dell"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_gaming_D_A_HP_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "2":
                            print(
                            "BOT: How many inches do you want the screen to be? (15.6, 17.3 inches)")
                            self.user_company = "Acer"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_gaming_D_A_HP_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "3":
                            print(
                            "BOT: How many inches do you want the screen to be? (15.6, 17.3 inches)")
                            self.user_company = "Asus"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_gaming_D_A_HP_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "4":
                            print(
                            "BOT: How many inches do you want the screen to be? (15.6, 17.3 inches)")
                            self.user_company = "HP"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_gaming_D_A_HP_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "5":
                            print(
                            "BOT: How many inches do you want the screen to be? (15.6, 17.3 inches)")
                            self.user_company = "Lenovo"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 6 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_gaming_D_A_HP_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "6":
                            print(
                            "BOT: How many inches do you want the screen to be? (14, 15.6, 17.3, 18.4 inches)")
                            self.user_company = "MSI"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 4 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4"]:
                                    flag_inc = False
                            self.user_inches = w_gaming_MSI_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        else:
                            print(
                            "BOT: How many inches do you want the screen to be? (14, 17.3 inches)")
                            self.user_company = "Razer"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_gaming_Razer_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        
                    # NOTEBOOK
                    elif self.user_typeLab == "3":
                        self.user_typeLab = "Notebook"
                        flag_ori = True
                        while flag_ori == True:
                            print(
                        "BOT: With origin of laptop, we have the following 11 categories: Dell, Acer, Asus, HP, Lenovo, Chuwi, Fujitsu, Toshiba, Samsung, Mediacom, Vero")
                            print(
                                "BOT: Please press from 1 to 11 for the respective categories above")
                            self.user_company = input("User: ")
                            if self.user_company in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
                                flag_ori = False
                        if self.user_company == "1":
                            print(
                            "BOT: How many inches do you want the screen to be? (13.3, 14, 15.6, 17.3 inches)")
                            self.user_company = "Dell"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 4 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4"]:
                                    flag_inc = False
                            self.user_inches = w_notebook_D_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "2":
                            print(
                            "BOT: How many inches do you want the screen to be? (11.6, 13.3, 14, 15.6, 17.3 inches)")
                            self.user_company = "Acer"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 5 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4", "5"]:
                                    flag_inc = False
                            self.user_inches = w_notebook_Ac_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "3":
                            print(
                            "BOT: How many inches do you want the screen to be? (13.3, 14, 14.1, 15.6, 17.3 inches)")
                            self.user_company = "Asus"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 5 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4", "5"]:
                                    flag_inc = False
                            self.user_inches = w_notebook_As_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "4":
                            print(
                            "BOT: How many inches do you want the screen to be? (13.3, 14, 15.6, 17, 17.3 inches)")
                            self.user_company = "HP"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 5 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4", "5"]:
                                    flag_inc = False
                            self.user_inches = w_notebook_HP_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "5":
                            print(
                            "BOT: How many inches do you want the screen to be? (11.6, 13.3, 14, 15.6, 17.3 inches)")
                            self.user_company = "Lenovo"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 5 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4", "5"]:
                                    flag_inc = False
                            self.user_inches = w_notebook_Ac_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "6":
                            print(
                            "BOT: How many inches do you want the screen to be? (12.3, 15.6 inches)")
                            self.user_company = "Chuwi"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_notebook_Chu_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "7":
                            print("BOT: Unfortunately, we only have 1 laptop")
                            self.user_company = "Fujitsu"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "15.6")
                        elif self.user_company == "8":
                            print(
                            "BOT: How many inches do you want the screen to be? (13.3, 14.0, 15.6 inches)")
                            self.user_company = "Toshiba"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 3 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3"]:
                                    flag_inc = False
                            self.user_inches = w_notebook_Tos_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "9":
                            print("BOT: Unfortunately, we only have 1 laptop")
                            self.user_company = "Samsung"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "15.6")
                        elif self.user_company == "10":
                            print(
                            "BOT: How many inches do you want the screen to be? (13.3, 14.0 inches)")
                            self.user_company = "Mediacom"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_notebook_Med_Ve_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        else:
                            print(
                            "BOT: How many inches do you want the screen to be? (13.3, 14.0 inches)")
                            self.user_company = "Vero"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_notebook_Med_Ve_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
    
                    # ULTRABOOK
                    elif self.user_typeLab == "4":
                        self.user_typeLab = "Ultrabook"
                        flag_ori = True
                        while flag_ori == True:
                            print(
                        "BOT: With origin of laptop, we have the following 10 categories: Dell, Acer, Asus, HP, Lenovo, Huawei, LG, Toshiba, Samsung, Xiaomi, Razer")
                            print(
                                "BOT: Please press from 1 to 11 for the respective categories above")
                            self.user_company = input("User: ")
                            if self.user_company in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
                                flag_ori = False
                        if self.user_company == "1":
                            print(
                            "BOT: How many inches do you want the screen to be? (12.5, 13.3, 14, 15.6 inches)")
                            self.user_company = "Dell"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 4 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4"]:
                                    flag_inc = False
                            self.user_inches = w_ultrabook_D_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "2":
                            print(
                            "BOT: How many inches do you want the screen to be? (13.3, 14 inches)")
                            self.user_company = "Acer"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_ultrabook_Ac_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "3":
                            print(
                            "BOT: How many inches do you want the screen to be? (12.5, 13.3, 14.0, 15.6 inches)")
                            self.user_company = "Asus"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 4 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4"]:
                                    flag_inc = False
                            self.user_inches = w_ultrabook_As_HP_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "4":
                            print(
                            "BOT: How many inches do you want the screen to be? (12.5, 13.3, 14.0, 15.6 inches)")
                            self.user_company = "HP"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 4 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3", "4"]:
                                    flag_inc = False
                            self.user_inches = w_ultrabook_As_HP_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "5":
                            print(
                            "BOT: How many inches do you want the screen to be? (12.5, 14.0, 15.6 inches)")
                            self.user_company = "Lenovo"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 3 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3"]:
                                    flag_inc = False
                            self.user_inches = w_ultrabook_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "6":
                            print("BOT: Unfortunately, we only have 2 laptops")
                            self.user_company = "Huawei"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "13.0")
                        elif self.user_company == "7":
                            print(
                            "BOT: How many inches do you want the screen to be? (14.0, 15.6 inches)")
                            self.user_company = "LG"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_ultrabook_LG_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "8":
                            print(
                            "BOT: How many inches do you want the screen to be? (12.5, 13.3, 14 inches)")
                            self.user_company = "Toshiba"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 3 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3"]:
                                    flag_inc = False
                            self.user_inches = w_ultrabook_Tos_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "9":
                            print(
                            "BOT: How many inches do you want the screen to be? (13.3, 15.0 inches)")
                            self.user_company = "Samsung"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_ultrabook_Sam_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "10":
                            print("BOT: Unfortunately, we only have 1 laptop")
                            self.user_company = "Xiaomi"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "13.3")
                        else:
                            print("BOT: Unfortunately, we only have 2 laptops")
                            self.user_company = "Razer"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "12.5")
     
                    # NETBOOK
                    elif self.user_typeLab == "5":
                        self.user_typeLab = "Netbook"
                        flag_ori = True
                        while flag_ori == True:
                            print(
                        "BOT: With origin of laptop, we have the following 10 categories: Dell, Acer, Asus, HP, Lenovo")
                            print(
                                "BOT: Please press from 1 to 5 for the respective categories above")
                            self.user_company = input("User: ")
                            if self.user_company in ["1", "2", "3", "4", "5"]:
                                flag_ori = False
                        if self.user_company == "1":
                            print("BOT: Unfortunately, we only have 1 laptop")
                            self.user_company = "Dell"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "11.6")
                        elif self.user_company == "2":
                            print("BOT: Unfortunately, we only have 2 laptops")
                            self.user_company = "Acer"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "11.6")
                        elif self.user_company == "3":
                            print("BOT: Unfortunately, we only have 2 laptops")
                            self.user_company = "Asus"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "11.6")
                        elif self.user_company == "4":
                            print(
                            "BOT: How many inches do you want the screen to be? (11.6, 12.5 inches)")
                            self.user_company = "HP"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_netbook_HP_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        else:
                            print(
                            "BOT: How many inches do you want the screen to be? (11.6, 12.5 inches)")
                            self.user_company = "Lenovo"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_netbook_HP_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)

                    # WORKSTATION
                    elif self.user_typeLab == "6":
                        self.user_typeLab = "Workstation"
                        flag_ori = True
                        while flag_ori == True:
                            print(
                        "BOT: With origin of laptop, we have the following 10 categories: Dell, HP, Lenovo")
                            print(
                                "BOT: Please press from 1 to 3 for the respective categories above")
                            self.user_company = input("User: ")
                            if self.user_company in ["1", "2", "3"]:
                                flag_ori = False
                        if self.user_company == "1":
                            print(
                            "BOT: How many inches do you want the screen to be? (15.6, 17.3 inches)")
                            self.user_company = "Dell"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_workstation_D_HP_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "2":
                            print(
                            "BOT: How many inches do you want the screen to be? (15.6, 17.3 inches)")
                            self.user_company = "HP"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w_workstation_D_HP_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "3":
                            print("BOT: Unfortunately, we only have 3 laptops")
                            self.user_company = "Lenovo"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "15.6")
                    
                # WINDOWS 10S
                elif self.user_os == "2":
                    print("BOT: With type of laptop, we have the following 3 categories: Notebook, Ultrabook, Netbook")
                    self.user_os = "Windows 10 S"
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                                self, self.user_os, "Ultrabook", "Microsoft", "13.5")
                    Query.query_check_info(
                                self, self.user_os, "Notebook", "Asus", "14.0")
                    Query.query_check_info(
                                self, self.user_os, "Netbook", "Asus", "11.6")
                # WINDOWS 7
                elif self.user_os == "3":
                    print("BOT: With type of laptop, we have the following 6 categories: 2 in 1 Convertible, Notebook, Netbook, Ultrabook, Workstation")
                    self.user_os = "Windows 7"
                    flag_type = True
                    while flag_type == True:
                        print(
                            "BOT: Please press from 1 to 5 for the respective categories above")
                        self.user_typeLab = input("User: ")
                        if self.user_typeLab in ["1", "2", "3", "4", "5"]:
                            flag_type = False
                    if self.user_typeLab == "1":
                        self.user_typeLab = "2 in 1 Convertible"
                        print("BOT: Unfortunately, we only have 3 laptops")
                        print("BOT: You can refer to the following laptop")
                        Query.query_check_info(
                                self, self.user_os, self.user_typeLab, "ThinkPad P40", "14.0")
                    elif self.user_typeLab == "2":
                        self.user_typeLab = "Notebook"
                        flag_ori = True
                        while flag_ori == True:
                            print(
                        "BOT: With origin of laptop, we have the following 4 categories: Dell, HP, Lenovo, Toshiba")
                            print(
                                "BOT: Please press from 1 to 4 for the respective categories above")
                            self.user_company = input("User: ")
                            if self.user_company in ["1", "2", "3", "4"]:
                                flag_ori = False
                        if self.user_company == "1":
                            print("BOT: Unfortunately, we only have 3 laptops")
                            self.user_company = "Dell"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "15.6")
                        elif self.user_company == "2":
                            print(
                            "BOT: How many inches do you want the screen to be? (14.0, 15.6 inches)")
                            self.user_company = "HP"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 2 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2"]:
                                    flag_inc = False
                            self.user_inches = w7_notebook_HP_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        elif self.user_company == "3":
                            print(
                            "BOT: How many inches do you want the screen to be? (14.0, 15.6, 17.3 inches)")
                            self.user_company = "Lenovo"
                            flag_inc = True
                            while flag_inc == True:
                                print(
                                    "BOT: Please press key 1 to 3 for the respective categories above")
                                self.user_inches = input("User: ")
                                if self.user_inches in ["1", "2", "3"]:
                                    flag_inc = False
                            self.user_inches = w7_notebook_Le_inc(self.user_inches)
                            print("BOT: You can refer to the following laptops")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                        else:
                            print("BOT: Unfortunately, we only have 2 laptops")
                            self.user_company = "Toshiba"
                            print("BOT: You can refer to the following laptop")
                            Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "13.3")
            # MACOS AND MAC OS X
            elif re.search(".*mac.*", self.user_os):
                print("BOT: We have the following 2 categories: macOS, Mac OS X")
                flag_os = True
                while flag_os == True:
                    print(
                        "BOT: Please press from 1 (macOS) or 2 (Mac OS X) that you want to check the information")
                    self.user_os = input("User: ")
                    if self.user_os in ["1", "2"]:
                        flag_os = False
                self.user_company = "Apple"
                self.user_typeLab = "Ultrabook"
                if self.user_os == "1":
                    self.user_os = "macOS"
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "12.0")
                    Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "13.3")
                    Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "15.4")
                else:
                    self.user_os = "Mac OS X"
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "11.6")
                    Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "12.0")
                    Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "13.3")
                    Query.query_check_info(
                                self, self.user_os, self.user_typeLab, self.user_company, "15.4")

            # NO_OS
            elif re.search(".*no.*", self.user_os):
                print("BOT: With type of laptop, we have the following 3 categories: Gaming, Notebook, Ultrabook")
                self.user_os = "No OS"
                flag_type = True
                while flag_type == True:
                    print(
                        "BOT: Please press from 1 to 3 for the respective categories above")
                    self.user_typeLab = input("User: ")
                    if self.user_typeLab in ["1", "2", "3"]:
                        flag_type = False
                if self.user_typeLab == "1":
                    self.user_typeLab = "Gaming"
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Lenovo", "15.6")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Asus", "15.6")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Asus", "17.3")
                elif self.user_typeLab == "2":
                    self.user_typeLab = "Notebook"
                    flag_ori = True
                    while flag_ori == True:
                        print(
                    "BOT: With origin of laptop, we have the following 4 categories: Asus, HP, Lenovo, Xiaomi")
                        print(
                            "BOT: Please press from 1 to 4 for the respective categories above")
                        self.user_company = input("User: ")
                        if self.user_company in ["1", "2", "3", "4"]:
                            flag_ori = False
                    if self.user_company == "1":
                        print("BOT: Unfortunately, we only have 2 laptops")
                        self.user_company = "Asus"
                        print("BOT: You can refer to the following laptop")
                        Query.query_check_info(
                            self, self.user_os, self.user_typeLab, self.user_company, "15.6")
                        Query.query_check_info(
                            self, self.user_os, self.user_typeLab, self.user_company, "17.3")
                    elif self.user_company == "2":
                        print("BOT: Unfortunately, we only have 2 laptops")
                        self.user_company = "HP"
                        print("BOT: You can refer to the following laptop")
                        Query.query_check_info(
                            self, self.user_os, self.user_typeLab, self.user_company, "15.6")
                    elif self.user_company == "3":
                        print(
                        "BOT: How many inches do you want the screen to be? (14.0, 15.6, 17.3 inches)")
                        self.user_company = "Lenovo"
                        flag_inc = True
                        while flag_inc == True:
                            print(
                                "BOT: Please press key 1 to 3 for the respective categories above")
                            self.user_inches = input("User: ")
                            if self.user_inches in ["1", "2", "3"]:
                                flag_inc = False
                        self.user_inches = nOS_workstation_Le_inc(self.user_inches)
                        print("BOT: You can refer to the following laptops")
                        Query.query_check_info(
                            self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                    else:
                        print("BOT: Unfortunately, we only have 2 laptops")
                        self.user_company = "Xiaomi"
                        print("BOT: You can refer to the following laptop")
                        Query.query_check_info(
                            self, self.user_os, self.user_typeLab, self.user_company, "15.6")
                else:
                    self.user_typeLab = "Ultrabook"
                    print("BOT: Unfortunately, we only have 1 laptop")
                    self.user_company = "Xiaomi"
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, self.user_company, "13.3")
                
            # LINUX
            elif re.search(".*linux.*", self.user_os):
                print("BOT: With type of laptop, we have the following 3 categories: Gaming, Notebook, Ultrabook")
                self.user_os = "Linux"
                flag_type = True
                while flag_type == True:
                    print(
                        "BOT: Please press from 1 to 3 for the respective categories above")
                    self.user_typeLab = input("User: ")
                    if self.user_typeLab in ["1", "2", "3"]:
                        flag_type = False
                if self.user_typeLab == "1":
                    self.user_typeLab = "Gaming"
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Dell", "15.6")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Asus", "17.3")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Acer", "15.6")
                elif self.user_typeLab == "2":
                    self.user_typeLab = "Notebook"
                    flag_ori = True
                    while flag_ori == True:
                        print(
                    "BOT: With origin of laptop, we have the following 4 categories: Dell, Acer, Asus")
                        print(
                            "BOT: Please press from 1 to 3 for the respective categories above")
                        self.user_company = input("User: ")
                        if self.user_company in ["1", "2", "3"]:
                            flag_ori = False
                    if self.user_company == "1":
                        print(
                        "BOT: How many inches do you want the screen to be? (14.0, 15.6, 17.3 inches)")
                        self.user_company = "Dell"
                        flag_inc = True
                        while flag_inc == True:
                            print(
                                "BOT: Please press key 1 to 3 for the respective categories above")
                            self.user_inches = input("User: ")
                            if self.user_inches in ["1", "2", "3"]:
                                flag_inc = False
                        self.user_inches = Li_notebook_Le_inc(self.user_inches)
                        print("BOT: You can refer to the following laptops")
                        Query.query_check_info(
                            self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                    elif self.user_company == "2":
                        self.user_company = "Acer"
                        print("BOT: You can refer to the following laptop")
                        Query.query_check_info(
                            self, self.user_os, self.user_typeLab, self.user_company, "15.6")
                    else:
                        self.user_company = "Acer"
                        print("BOT: You can refer to the following laptop")
                        Query.query_check_info(
                            self, self.user_os, self.user_typeLab, self.user_company, "15.6")
                else:
                    self.user_typeLab = "Ultrabook"
                    self.user_company = "Dell"
                    print("BOT: Unfortunately, we only have 2 laptops")
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                        self, self.user_os, self.user_typeLab, self.user_company, "14.0")
                    Query.query_check_info(
                        self, self.user_os, self.user_typeLab, self.user_company, "13.3")
                    
            
            # ANDROID
            elif re.search(".*android.*", self.user_os):
                print("BOT: Unfortunately, we only have 2 laptops")
                self.user_os = "Android"
                self.user_typeLab = "2 in 1 Convertible"
                self.user_company = "Lenovo"
                Query.query_check_info(
                        self, self.user_os, self.user_typeLab, self.user_company, "10.1")
            # CHROME OS
            elif re.search(".*chrome.*", self.user_os):
                print("BOT: With type of laptop, we have the following 3 categories: 2 in 1 Convertible, Notebook, Ultrabook, Netbook")
                self.user_os = "Chrome OS"
                flag_type = True
                while flag_type == True:
                    print(
                        "BOT: Please press from 1 to 4 for the respective categories above")
                    self.user_typeLab = input("User: ")
                    if self.user_typeLab in ["1", "2", "3", "4"]:
                        flag_type = False
                if self.user_typeLab == "1":
                    self.user_typeLab = "2 in 1 Convertible"
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "HP", "11.6")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Asus", "12.5")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Acer", "11.6")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Samsung", "12.3")
                elif self.user_typeLab == "2":
                    self.user_typeLab = "Notebook"
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Lenovo", "13.3")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Lenovo", "14.0")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "HP", "13.3")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Acer", "14.0")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Acer", "15.6")
                elif self.user_typeLab == "3":
                    self.user_typeLab = "Ultrabook"
                    self.user_company = "Google"
                    self.user_inches = "12.3"
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, self.user_company, self.user_inches)
                else:
                    self.user_typeLab = "Netbook"
                    self.user_inches = "11.6"
                    print("BOT: You can refer to the following laptop")
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Samsung", self.user_inches)
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Dell", self.user_inches)
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Acer", self.user_inches)
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Asus", self.user_inches)
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "HP", self.user_inches)
                    Query.query_check_info(
                            self, self.user_os, self.user_typeLab, "Lenovo", self.user_inches)
            # OTHER CASES
            else:
                print("Please enter correct spelling.")
                Help._help_process(self, user_help)
            flag_order = True
            while flag_order == True:
                print("BOT: Do you want to order any laptop (press 1)? Or do you want to check the information of another laptop (press 2)?")
                self.user_help = input("User: ")
                if self.user_help in ["1","2"]:
                    flag_order = False
            if self.user_help == "1":
                ## GOI HAM IN HOA DON TAI DAY
                pass
                # print("BOT: Here is your invoice, thank you for your interest in the product")
            else:
                self.user_help = 'info'
                Help._help_process(self, self.user_help)
        else:
            Help._print_invoice(self, self.user_help)

    def _print_invoice(self, user_help):
        self.user_help = user_help
        if self.user_help == 'order':
            ## DESIGN TAI DAY
            pass


class Conversation(Intent, Help):
    def __init__(self, data_rule_based, flag=True):
        Intent.__init__(self, data_rule_based)
        Help.__init__(self, None)
        self.flag = flag

    def communicate(self):
        # Opening sentence
        print("BOT: Hi, I will try to respond to you reasonably. If you want to exit, please type 'Bye'.")
        # Loop to communicate with user
        while self.flag == True:
            # Handle input
            message = input("User: ")
            message = message.lower()
            # Respond from bot
            if message == 'bye':
                self.flag = False
                print("BOT: You are welcome. Goodbye!")
            else:
                print(Intent._find_intent(self, message))
                if self.key == "help":
                    flag_input = True
                    print("BOT: Please enter 'info' if you want to check information of laptop or enter 'invoice' if you want to issue an invoice.")
                    while flag_input == True:
                        user_help = input()
                        if user_help == 'info':
                            Help._help_process(self, user_help)
                            flag_input = False
                        elif user_help =="invoice":
                            Help._print_invoice(self, user_help)
                            flag_input = False
                        else:
                            print("BOT: Please enter 'info' if you want to check information of laptop or enter 'invoice' if you want to issue an invoice.")
                if self.key == "order":
                    pass


if __name__ == '__main__':
    PATH_RULE_BASED = './Data/intents_rule-based.json'
    user_bot = Conversation(PATH_RULE_BASED).communicate()
