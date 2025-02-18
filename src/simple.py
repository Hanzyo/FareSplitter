import argparse

class ReceiptParser:
    def __init__(self, input_list, output_filename):
        self.input_list = input_list
        self.tax = {}
        self.users = {}
        self.total_price = 0
        self.output_f = output_filename
        self.cross_pay = {}
        
        
    def clear_data(self):
        self.tax = {}
        self.users = {}
        self.total_price = {}
        
    def parse_tax(self, input_list):
        for i, entry in enumerate(input_list):
            if len(entry.split(' ')) == 1:
                return input_list[i:]
            self.tax[entry.split(' ')[0]] = float(entry.split(' ')[1].strip())
    
    def parse_prices(self, input_list):
        input_list = [i.strip() for i in input_list]
        for i, entry in enumerate(input_list):
            if i == 0:
                self.total_price = float(entry)
                continue
            if len(entry.split(' ')) == 1:
                return input_list[i:]
            user, value, tax = entry.split(' ')
            value = float(value)
            tax = tax
            if user not in self.users:
                self.users[user] = [(value, tax)]
            else:
                self.users[user].append((value, tax))
    
    def calculate(self, paid_user):
        remaining_list = []
        if len(paid_user) > 1:
            remaining_list = paid_user[1:]
        paid = paid_user[0]
        output_txt = f"{paid} paid total amount ${self.total_price}: \n"
        if paid not in self.users:
            self.users[paid] = []
        user_paying = {user: 0.0 for user in self.users}
        remaining_price = self.total_price
        for user, item_list in self.users.items():
            for tuple in item_list:
                price_after_tax = tuple[0] * (1 + self.tax[tuple[1]]*0.01)
                if price_after_tax > self.total_price:
                    print(f"Something wrong with the input. {price_after_tax} cannot be larger than {self.total_price}")
                    exit(1)
                user_paying[user] += price_after_tax
                remaining_price -= price_after_tax
        splitting_price = float(remaining_price / len(self.users))
        user_paying = {key: price + splitting_price for key, price in user_paying.items()}
        for user, price in user_paying.items():
            rounded = round(price,2)
            output_txt += f"{user} owed {rounded} to {paid}\n"
            if user not in self.cross_pay:
                self.cross_pay[user] = {}
            if paid in self.cross_pay[user]:
                self.cross_pay[user][paid] += rounded
            else:
                self.cross_pay[user][paid] = rounded
            
        return remaining_list, output_txt
    
    def handler(self):
        output_txt = ""
        remaining_list = self.input_list
        while True:
            self.clear_data()
            after_tax = self.parse_tax(remaining_list)
            paid_user = self.parse_prices(after_tax)
            remaining_list, output = self.calculate(paid_user)
            output_txt += output
            if len(remaining_list) == 0:
                break
        output_txt += "===== Final transaction info ===== \n"
        for payer in self.cross_pay:
            for payee, price in self.cross_pay[payer].items():
                if price == 0.0:
                    continue
                final_price = price
                if payee in self.cross_pay and payer in self.cross_pay[payee] and self.cross_pay[payee][payer] != 0.0:
                    final_price = price - self.cross_pay[payee][payer]
                final_price = round(final_price, 2)
                if final_price > 0.0:
                    output_txt += f"{payer} needs to pay {payee} ${final_price}\n"
                elif final_price < 0.0:
                    output_txt += f"{payee} needs to pay {payer} ${-1*final_price}\n"
                self.cross_pay[payee][payer] = 0.0
                self.cross_pay[payer][payee] = 0.0
                
            
        with open(self.output_f, "w") as f:
            f.write(output_txt)
            print(f"Output written to {self.output_f}")
        
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, required=True, help="Path to input file")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to output file")
    # Parse the arguments
    args = parser.parse_args()
    filename = args.input
    output_filename = args.output
    try: 
        f = open(filename, "r")
    except Exception as e:
        print("Failed to open input file", e)
        exit(1)
    
    p = ReceiptParser(f.readlines(), output_filename)
    p.handler()
    

if __name__ == "__main__":
    main()