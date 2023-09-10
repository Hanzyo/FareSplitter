
from Groceries import *
import numpy as np
class Parser:
    def __init__(self) -> None:
        self.exit_flag = True
        self.num_people = 0
        self.num_orders = 0
        self.response = []
        self.orders = []
        self.paid_person = []
        self.index = []
        self.tax_rate_dict = {}
        self.people = {}
        
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
                    if self.response[0] not in self.people:
                        self.num_people += 1
                        self.people[self.response[0]] = self.num_people - 1
                        self.index.append(self.response[0])
                    item.update_splitter(self.response[0], float(self.response[1]))
                item.print_info()
                items.append(item)
                self.response[0] = ""
            print("Enter the alias of person who paid this order")
            self.get_response()
            self.paid_person.append(self.response[0])
            if self.response[0] not in self.people:
                self.num_people += 1
                self.people[self.response[0]] = self.num_people - 1
                self.index.append(self.response[0])
            self.orders.append(items)
                
    def calculate(self):
        transactions = np.zeros((self.num_people, self.num_people))
        for i in range(self.num_orders):
            items = self.orders[i]
            for item in items:
                for splitter, val in item.splitters.items():
                    from_id = self.people[splitter]
                    to_id = self.people[self.paid_person[i]]
                    transactions[from_id][to_id] += val
        for i in range(self.num_people):
            for j in range(self.num_people):
                if transactions[i][j] != 0 and transactions[j][i] != 0:
                    if transactions[i][j] >= transactions[j][i]:
                        transactions[i][j] -= transactions[j][i]
                        transactions[j][i] = 0
                    else:
                        transactions[j][i] -= transactions[i][j]
                        transactions[i][j] = 0
        with open("output.txt", 'w') as file:
            for i in range(self.num_people):
                for j in range(self.num_people):
                    if transactions[i][j] != 0:
                        file.write(f"{self.index[i]} needs to pay {self.index[j]}: ${round(transactions[i][j], 2)}\n")

    def print_result(self):
        with open("receipt.txt", 'w') as file:
            print("============== FareSplitter Interactive Tool ==============\n")
            for i in range(self.num_orders):
                file.write(f"For order #{i+1}: \n")
                items = self.orders[i]
                for item in items:
                    file.write(f"{item.name} -- ${item.price} -- tax rate: {item.tax_rate}\n")
                    file.write(f"   Splitted by: \n")
                    for splitter, val in item.splitters.items():
                        file.write(f"   {splitter} shares ${round(val,2)}\n")

    def parse(self):
        self.init_process()
        if(not self.exit_flag):
            return
        self.get_item_info()
        if(not self.exit_flag):
            return
        self.calculate()
        if(not self.exit_flag):
            return
        self.print_result()
        print("Calculation completed, see outputs in output.txt")