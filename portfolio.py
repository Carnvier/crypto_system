import os
from datetime import datetime
import asset as ast, cryptohive_db as db


class Portfolio():
    def __init__(self):
        self.portfolio = {}
        self.assets = ast.assets
    if not os.path.exists('portfolio.txt'):
        with open('portfolio.txt', 'w') as p:
            p.write("")

    def close_position(self, username, asset, action):
        profit = 0
        user_found = False
        asset_found = False

        with open('portfolio.txt', 'r+') as p:
            existing_data = p.readlines()

            for i, line in enumerate(existing_data):
                user_name, i_action, holding, quantity, cost =  line.split(',')
                quantity, cost = float(quantity), float(cost)
                if username != user_name.strip() or action.lower() != i_action.strip().lower():
                    continue

                user_found = True
                if asset != holding.strip():
                    continue
                asset_found = True

                if i_action.strip().lower().startswith('b'):
                    current_cost = quantity * self.assets[asset]
                    profit = current_cost - cost                    
                elif i_action.strip().lower().startswith('s'):
                    current_cost = quantity * self.assets[asset]
                    profit = cost - current_cost
                else:
                    print("Action not found")
                    break

                total_earnings = cost + profit                
                existing_data.remove(line)
                print(f"Removed {asset.title()} from your portfolio.")
                break


            p.seek(0)
            p.writelines(existing_data)
            p.truncate()

            with open('accounts.txt', 'r+') as f:
                existing_data = f.readlines()
                for i, line in enumerate(existing_data):
                    user_name, password, balance =  line.split(',')
                    if username != user_name.strip():
                        continue

                    user_found = True
                    balance = float(balance)

                    if user_found and profit > 0:
                        print(f'Profit: {profit}')
                        balance += total_earnings
                        print(f"Updated balance: {balance}")
                        existing_data[i] = f"{user_name},{password}, {balance}\n"
                    
                    if user_found and profit < 0:
                        print(f'Loss: {abs(profit)}')
                        balance -= abs(profit)
                        print(f"Updated balance: {balance}")
                        existing_data[i] = f"{user_name},{password}, {balance}\n"
                
                f.seek(0)
                f.writelines(existing_data)
                f.truncate()       



    def view_holdings(self, username, data):
        print(f"Portfolio for {username.title()}:")
        for i, line in enumerate(data):
            date, user_name, action, asset, quantity, cost = data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6]    
            print(f"{date:<13} {action.upper():<10} {asset:<10} {quantity:<10} {cost}")
    
    def buy_asset(self, username, password, asset, quantity):
        account = db.CryptoHiveDB().read_account(username, password)
        quantity = int(quantity)
        action = "buy"

        if asset not in self.assets:
            print("Asset not found in our portfolio.")
            return

        asset_value  = self.assets[asset]
        total_cost = asset_value * quantity

        if account:
            balance = float(account[0][3])
            if balance < total_cost:
                print("Insufficient funds for purchase.")
                return
            
            portfolio = (username, action, asset, quantity, total_cost)
            db.CryptoHiveDB().portfolio_insert_data(portfolio)

            balance = balance - total_cost
            account = (balance, username, password)
            db.CryptoHiveDB().account_update_data(account)
            print(f"Buy Transaction Success!\nCurrent Balance: {balance}\n")
            print(f"{username.title()} Buy Transaction Summary:")
            print (f"{asset} {quantity} {asset_value} {total_cost}")
            return 
                
        if not account:
            print(f"{username.title()} not found!")
        return
                        



    def sell_asset(self, username, password, asset, quantity):
        account = db.CryptoHiveDB().read_account(username, password)
        quantity = int(quantity)
        action = "sell"

        if asset not in self.assets:
            print("Asset not found in our portfolio.")
            return
        
        asset_value  = self.assets[asset]
        total_cost = asset_value * quantity
        
        if account:
            balance = float(account[0][3])
            if balance < total_cost:
                print("Insufficient funds for sale.")
                return
            
            portfolio = (username, action, asset, quantity, total_cost)
            db.CryptoHiveDB().portfolio_insert_data(portfolio)

            balance = balance - total_cost
            account = (balance, username, password)
            db.CryptoHiveDB().account_update_data(account)
      
            print(f"Sell Transaction Success!\nCurrent Balance: {balance}\n")
            print(f"{username.title()} Sell Transaction Summary:")
            print (f"{asset} {quantity} {asset_value} {total_cost}")
            return 
                        
        if not account:
            print(f"{username.title()} not found!")
        return 

    def save_transaction(self, username, asset, quantity, action):
        amount = float(quantity * self.assets[asset])
        transaction = (username, action, asset, quantity, amount)
        db.CryptoHiveDB().transactions_insert_data(transaction)
        return

