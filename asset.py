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


    def view_assets(self, assets):
        print("Current assets:")
        for asset, value in assets.items():
            print(f"{asset:<10}: {value}")


    def get_value(self):
        total_value = self.price * self.quantity
        print(total_value)
    
   


