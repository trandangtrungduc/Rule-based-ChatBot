import sys
sys.path.insert(0, 'E:/Project/ML_and_DL/CBD/Chatbot/')

from Configuration.parameter_constants import *
from mysql.connector import Error
import mysql.connector as msql
import pandas as pd



"""    Class Laptop to show information of laptop  """


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


"""    Class Laptop to show information of order  """


class Order():

    def __init__(self, laptop_ID, Quantity, Month, user_ID):
        self.laptop_ID = laptop_ID
        self.Quantity = Quantity
        self.Month = Month
        self.user_ID = user_ID

    def info(self):

        return (f'- Laptop ID: {self.laptop_ID}\n'
                f'- Quantity: {self.Quantity}\n'
                f'- Month: {self.Month}\n'
                f'- User ID: {self.user_ID}\n')


"""    Class Query to retrieve the data  """


class Query(Laptop):

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.db = msql.connect(host=self.host, database=self.database,
                               user=self.user, password=self.password)
        self.count = 0

    def query_ID(self, id):
        cursor = self.db.cursor()
        query_id = "SELECT * FROM laptop_price_data WHERE laptop_ID = '%s'" % (
            id)
        try:
            cursor.execute(query_id)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_Company(self, Company):
        cursor = self.db.cursor()
        query_comp = "SELECT * FROM laptop_price_data WHERE Company = '%s'" % (
            Company)
        try:
            cursor.execute(query_comp)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_Product(self, Product):
        cursor = self.db.cursor()
        query_prod = "SELECT * FROM laptop_price_data WHERE Product = '%s'" % (
            Product)
        try:
            cursor.execute(query_prod)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_TypeName(self, TypeName):
        cursor = self.db.cursor()
        query_type = "SELECT * FROM laptop_price_data WHERE TypeName = '%s'" % (
            TypeName)
        try:
            cursor.execute(query_type)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_Inches(self, Inches):
        cursor = self.db.cursor()
        query_inch = "SELECT * FROM laptop_price_data WHERE Inches = '%s'" % (
            Inches)
        try:
            cursor.execute(query_inch)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_ScreenResolution(self, ScreenResolution):
        cursor = self.db.cursor()
        query_scre = "SELECT * FROM laptop_price_data WHERE ScreenResolution = '%s'" % (
            ScreenResolution)
        try:
            cursor.execute(query_scre)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_Cpu(self, Cpu):
        cursor = self.db.cursor()
        query_cpu = "SELECT * FROM laptop_price_data WHERE Cpu = '%s'" % (
            Cpu)
        try:
            cursor.execute(query_cpu)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_Ram(self, Ram):
        cursor = self.db.cursor()
        query_ram = "SELECT * FROM laptop_price_data WHERE Ram = '%s'" % (
            Ram)
        try:
            cursor.execute(query_ram)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_Memory(self, Memory):
        cursor = self.db.cursor()
        query_memo = "SELECT * FROM laptop_price_data WHERE Memory = '%s'" % (
            Memory)
        try:
            cursor.execute(query_memo)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_Gpu(self, Gpu):
        cursor = self.db.cursor()
        query_gpu = "SELECT * FROM laptop_price_data WHERE Gpu = '%s'" % (
            Gpu)
        try:
            cursor.execute(query_gpu)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_OpSys(self, OpSys):
        cursor = self.db.cursor()
        query_opsy = "SELECT * FROM laptop_price_data WHERE OpSys = '%s'" % (
            OpSys)
        try:
            cursor.execute(query_opsy)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_Weight(self, Weight):
        cursor = self.db.cursor()
        query_weig = "SELECT * FROM laptop_price_data WHERE Weight = '%s'" % (
            Weight)
        try:
            cursor.execute(query_weig)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_Price_euros(self, Price_euros):
        cursor = self.db.cursor()
        query_pric = "SELECT * FROM laptop_price_data WHERE Price_euros = '%s'" % (
            Price_euros)
        try:
            cursor.execute(query_pric)
            results = cursor.fetchall()
            for row in results:
                ID, Company, Product, TypeName, Inches = row[0], row[1], row[2], row[3], row[4]
                ScreenResolution, Cpu, Ram, Memory = row[5], row[6], row[7], row[8]
                GPU, OpSys, Weight, Price_euros = row[9], row[10], row[11], row[12]
                laptop = Laptop(ID, Company, Product, TypeName, Inches, ScreenResolution,
                                Cpu, Ram, Memory, GPU, OpSys, Weight, Price_euros)
                self.count += 1
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()

    def query_auto_Analytic_Report(self, month):
        Price, Total = [], []
        COLUMNS = ['laptop_ID', 'Quantity', 'Month', 'user_ID']
        row__idx = 0
        df_order = pd.DataFrame(columns=COLUMNS)
        cursor = self.db.cursor()
        query_month = "SELECT * FROM order_record_data WHERE Month = '%s' ORDER BY laptop_ID" % (
            month)

        try:
            cursor.execute(query_month)
            result_1 = cursor.fetchall()
            for row in result_1:
                laptop_ID, Quantity, Month, user_ID = row[0], row[1], row[2], row[3]
                df_order.loc[str(row__idx)] = list(row)
                row__idx += 1
                query_price = "SELECT Price_euros FROM laptop_price.laptop_price_data WHERE laptop_ID = '%s'" % (
                    laptop_ID)
                cursor.execute(query_price)
                result_2 = cursor.fetchone()
                Price.append(result_2[0])
                Total.append(round(float(result_2[0])*int(Quantity), 3))
            df_order.insert(4, "Price", Price)
            df_order.insert(5, "Total", Total)
            df_order = df_order.drop(columns=["Month"])
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            self.db.close()
        return df_order
    
    def query_check_info(self, OS, typeLap, origin, inches):
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
                print("Laptop Specification {0}:".format(self.count))
                print(laptop.info())
                print('--------------------------------')
        except:
            print("Error fetching data.")
        finally:
            self.count = 0
            # self.db.close()


if __name__ == '__main__':

    """Database 1"""
    DATABASE = DATABASE_LAPTOP
    # LAPTOP_ID = 4                         # query_ID
    # COMPANY = 'Apple'                     # query_Company
    # PRODUCT = 'Macbook'                   # query_Product
    # TYPENAME = 'Ultrabook'                # query_TypeName
    # INCHES = '13.3'                       # query_Inches
    # SCREEN_RESOLUTION = '1440x900'        # query_ScreenResolution
    # CPU = 'Intel Core i5 2.3GHz'          # query_Cpu
    # RAM = '8GB'                           # query_Ram
    # MEMORY = '128GB SSD'                  # query_Memory
    # GPU = 'Intel Iris Plus Graphics 650'  # query_Gpu
    # OPERATION_SYSTEM = 'macOS'            # query_OpSys
    # WEIGHT = '1.37kg'                     # query_Weight

    query = Query(SERVER, DATABASE, USER, PASSWORD)
    response = query.query_check_info("Windows 10", "2 in 1 Convertible", "Dell", "11.6")
    print(response)

    """Database 2"""
    # DATABASE = DATABASE_ORDER
    # MONTH = 1
    # query = Query(SERVER, DATABASE, USER, PASSWORD)
    # response = query.query_auto_Analytic_Report(MONTH)
    # print(response)
