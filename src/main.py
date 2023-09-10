from GroceryParser import * 
import os


cur_dir = os.getcwd()
csv_file = cur_dir + "/receipt.csv"
parser = Parser(csv_file)
data = parser.parse()
print(data)