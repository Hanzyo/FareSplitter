
class Groceries:
    def __init__(self, name, price, origin, tax_rate) -> None:
        self.name = name
        self.price = float(price)
        self.origin = origin
        self.tax_rate = tax_rate
        self.total_price = self.price * (1 + self.tax_rate)
        self.splitters = {}
    
    def update_splitter(self, name, portion):
        self.splitters[name] = portion
        
    def print_info(self):
        print(f"Item {self.name} costs {self.total_price} and is splitted by ")
        for person in self.splitters:
            print(f"{person}: ${self.splitters[person] * self.total_price}")
        
