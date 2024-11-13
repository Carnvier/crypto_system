assets = {
    "Bitcoin" : 72000,
    "Ethereum" : 27000,
    "Gold": 28000,
    "Silver": 20000,
}


class Asset():
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_value(self):
        total_value = self.price * self.quantity
        return total_value
    
