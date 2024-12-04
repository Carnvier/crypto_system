import os
from datetime import datetime
import asset as ast, cryptohive_db as db


class Portfolio():
    def __init__(self):
        self.portfolio = {}
        self.assets = ast.Asset().get_values()

    def close_position(self, username, password, holding_id):
        '''Closing position of asset and updating database'''
        try:
            profit = 0.0
            holding_found = False

            # getting account and holding information
            try:
                account = db.CryptoHiveDB().read_account(username, password)
                balance = account[0][3]
                data = db.CryptoHiveDB().active_holdings(username)
                print(data)

                for holding in data:
                    # checking if holding exists
                    if holding_id == holding[0]:
                        details = (username, holding_id)
                        asset = holding[4]
                        quantity = holding[5]
                        i_action = holding[3]
                        cost = holding[6]
                        db.CryptoHiveDB().close_holding(details)
                        holding_found = True 
                        print(details, asset)               
                        break
            except:
                return "Error occurred while trying to get data from database"
            
            if not holding_found:
                print("Holding not found")
                return "Holding not found"
            print(i_action)
            # calculate profit based on buy or sell of the asset
            if i_action.strip().lower().startswith('b'):
                current_cost = quantity * self.assets[asset]
                profit += current_cost - cost                    
            elif i_action.strip().lower().startswith('s'):
                current_cost = quantity * self.assets[asset]
                profit += cost - current_cost
            else:
                return "Action not found"
        
            print(self.assets[asset])
            print(cost, current_cost, profit)
            total_earnings = cost + profit                
            print(f"Closed {asset.title()} in your portfolio.")

            # calculating new balance
            if profit > 0:
                print(f'Profit: {profit}')

            if profit < 0:
                print(f'Loss: {profit}') 
            balance += total_earnings
            print(f"Updated balance: {balance}")

            # updating account balance in the database
            account = (balance, username, password)
            response = db.CryptoHiveDB().account_update_data(account)
            if response.lower() == "success":
                return f"{profit}, {total_earnings}, {balance}"
            else:
                return response
        except Exception as e:
            return f"Error: {e}"
            
    def view_holdings(self, username, data):
        '''Print user's current holdings'''
        print(f"Portfolio for {username.title()}:")
        count = 0
        for i, line in enumerate(data):
            id, date, user_name, action, asset, quantity, cost, holding = data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7]  
            # Make sure only active holdings are printed 
            if holding:
                count += 1
                print(f"{id:<5} {date:<13} {action.upper():<10} {asset:<10} {quantity:<10} {cost}")
        if count == 0:
            print("No holdings found.")
    
    
    def buy_asset(self, username, password, asset, quantity):
        '''Record purchase of asset in database'''
        try:
            # Getting account information
            account = db.CryptoHiveDB().read_account(username, password)
            quantity = int(quantity)
            action = "buy"

            if asset not in self.assets:
                return ("Asset not found in our portfolio.")
                

            asset_value  = self.assets[asset]
            total_cost = asset_value * quantity

            # checking if account exists
            if account:
                balance = float(account[0][3])
                if balance < total_cost:
                    return ("Insufficient funds for purchase.")
                    
                # adding holding to user portfolio
                portfolio = (username, action, asset, quantity, total_cost)
                db.CryptoHiveDB().portfolio_insert_data(portfolio)

                balance = balance - total_cost
                account = (balance, username, password)
                db.CryptoHiveDB().account_update_data(account)
                return (f"Buy Transaction Success!\nCurrent Balance: {balance}\n{username.title()} Buy Transaction Summary: \n{asset} {quantity} {asset_value} {total_cost}")
                
                    
            if not account:
                return (f"{username.title()} not found!")
        except Exception as e:
            return f"Error: {e}"    
        
                        



    def sell_asset(self, username, password, asset, quantity):
        '''Record sell of asset in database'''
        try:
            account = db.CryptoHiveDB().read_account(username, password)
            quantity = int(quantity)
            action = "sell"

            if asset not in self.assets:
                return ("Asset not found in our portfolio.")
                
            
            asset_value  = self.assets[asset]
            total_cost = asset_value * quantity
            
            if account:
                balance = float(account[0][3])
                if balance < total_cost:
                    return ("Insufficient funds for sale.")
                    
                
                portfolio = (username, action, asset, quantity, total_cost)
                db.CryptoHiveDB().portfolio_insert_data(portfolio)

                balance = balance - total_cost
                account = (balance, username, password)
                db.CryptoHiveDB().account_update_data(account)
        
                return (f"Sell Transaction Success!\nCurrent Balance: {balance}\n {username.title()} Sell Transaction Summary: \n{asset} {quantity} {asset_value} {total_cost}")
            
                            
            if not account:
                return (f"{username.title()} not found!")
        except Exception as e:
            return f"Error: {e}"
         

    def save_transaction(self, username, asset, quantity, action):
        '''Save transaction information of either sell or purchase of asset'''
        try:
            amount = float(quantity * self.assets[asset])
            transaction = (username, action, asset, quantity, amount)
            db.CryptoHiveDB().transactions_insert_data(transaction)
            return "Transaction saved successfully"
        except:
            return "Error occurred while trying to save transaction"


