
from Groceries import *
from People import *

class Parser:
    def __init__(self) -> None:
        self.exit_flag = True
        self.response = []
        self.num_orders = 0
        self.orders = []
        self.paid_person = []
        self.tax_rate_dict = {}
        self.transaction = []
        
    def get_response(self):
        print("Press ENTER after typing:")
        in_str = input()
        if in_str == "":
            print("Don't leave blank")
            self.exit_flag = False
            return False
        if in_str == "exit":
            self.exit_flag = False
            return False
        self.response = in_str.split(' ')
        return True
            
    def init_process(self):
        print("============== FareSplitter Interactive Tool ==============")
        print("Please enter grocery info from receipts when prompted")
        print("Enter 'exit' at any point to terminate the program'")
        print("Please enter the number of order to calculate. e.g. how many transactions have you made?")
        if self.get_response():
            self.num_orders = int(self.response[0])
        else:
            return
        print("Please enter all paid tax rate one by one. Enter 'Done' after finishing all entries.")
        while(self.response[0] != "Done"):
            print("Enter tax rate alias and the tax rate percentage separated by a space. e.g. A 9.0")
            self.get_response()
            if(self.response[0] == "Done"):
                break
            if self.response[0] in self.tax_rate_dict:
                print("[ERROR] alias already used, please use another name")
                pass
            self.tax_rate_dict[self.response[0]] = float(self.response[1]) / 100.0
            
    def get_item_info(self):
        for i in range(self.num_orders):
            self.response[0] = ""
            items = []
            print(f"Please enter info for order #{i+1}")
            while(self.response[0] != "Done"):
                print("Enter item name, price, and tax alias separated by a space. e.g. Apple 2.0 A")
                self.get_response()
                if(self.response[0] == "Done"):
                        break
                while(self.response[2] not in self.tax_rate_dict):
                    print("[ERROR] tax alias not recognized")
                    print("Enter item name, price, and tax alias separated by a space. e.g. Apple 2.0 A")
                    self.get_response()
                item = Groceries(self.response[0], float(self.response[1]), i+1, self.tax_rate_dict[self.response[2]])
                while(self.response[0] != "Done"):
                    print("If splitted by more than one person, please enter his/her alias and the portion separated by a space. e.g. M 0.5")
                    print("Enter 'Done' to finish")
                    self.get_response()
                    if(self.response[0] == "Done"):
                        break
                    item.update_splitter(self.response[0], float(self.response[1]))
                item.print_info()
                items.append(item)
                self.response[0] = ""
            print("Enter the alias of person who paid this order")
            self.get_response()
            self.paid_person.append(self.response[0])
            self.orders.append(items)
                
    def calculate(self):
        for i in range(self.num_orders):
            should_pay = {}
            items = self.orders[i]
            for item in items:
                for splitter, val in item.splitters.items():
                    if splitter not in should_pay:
                        should_pay[splitter] = val
                    else:
                        should_pay[splitter] += val
            self.transaction.append(should_pay)
            
    def print_result(self):
        for i in range(self.num_orders):
            print(f"For order #{i + 1}, the following people should pay {self.paid_person[i]} this much:")
            for person, val in self.transaction[i].items():
                if person != self.paid_person[i]:
                    print(f"{person}: ${val}")

    def parse(self):
        self.init_process()
        if(not self.exit_flag):
            return
        self.get_item_info()
        if(not self.exit_flag):
            return
        self.calculate()
        self.print_result()