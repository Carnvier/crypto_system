def Portfolio():
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def add_asset(self, asset,quantity):
        if asset in self.portfolio:
            self.portfolio[asset] += quantity
        else:
            self.portfolio[asset] = quantity

    def remove_asset(self, asset, quantity):
        if asset in self.portfolio and self.portfolio[asset] >= quantity:
            self.portfolio[asset] -= quantity
        else:
            print(f"Not enough {asset} in the portfolio.")

    def view_holding(self):
        for asset, quantity in self.portfolio.items():
            print(f"{quantity} {asset}")