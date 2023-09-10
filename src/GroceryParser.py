import csv
from Groceries import *
from People import *

class Parser:
    def __init__(self, in_file) -> None:
        self.file = in_file
        self.people = []
        
    def parse(self):
        with open(self.file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            data = []
            for row in csv_reader:
                record = {}
                for i, val in enumerate(row):
                    record[headers[i]] = val
                data.append(record)
        return data        
        
 
    