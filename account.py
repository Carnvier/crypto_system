import getpass
import cryptohive_db as db
class Account():

    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance

    def create_account(self):      
        account =  (self.username, self.password, self.balance)
        db.CryptoHiveDB().account_insert_data(account)
        print(f"Welcome {self.username}! You have a current balance of {self.balance}.")
        return self.username, self.password, self.balance
        
    def deposit(self, amount, initial_deposit):
        self.balance = initial_deposit + amount
        db.CryptoHiveDB().account_update_data(self.username, self.password, self.balance)
        print(f"Deposit of {amount} successful! Your new balance is {self.balance}.")
        return self.balance

    def withdraw(self, amount, initial_deposit):
        if amount > initial_deposit:
            print("Withdrawal failed insufficient funds!!!")
            return

        self.balance = initial_deposit - amount
        db.CryptoHiveDB().account_update_data(self.username, self.password, self.balance)
        print(f"Withdrawal of {amount} successful! Your new balance is {self.balance}.")
        return self.balance

    def update_balance(self, action, amount):   
        account = db.CryptoHiveDB().read_account(self.username, self.password)  
        
        if account:
            user_found = True
            username, password, initial_deposit = account[0][1], account[0][2], account[0][3]
            initial_deposit = float(initial_deposit)
            if action.startswith('d'):
                balance = self.deposit(amount, initial_deposit)
            elif action.startswith('w'):
                balance = self.withdraw(amount, initial_deposit)
            else:
                print(f"{action.title()} not found!")    

        else:
            print("Account not found!")
            return 

        return balance
                      

                        

# ADD ERROR HANDLING LINES AND COMMENTS
