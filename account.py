import getpass
import cryptohive_db as db
class Account():

    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance

    def create_account(self):    
        '''Creating a new account with specified username, password and initial deposit'''  
        account =  (self.username, self.password, self.balance)
        response = db.CryptoHiveDB().account_insert_data(account)
        if response.lower() == "success":
            return f'{self.username}, {self.password}, {self.balance}'
        else: 
            return f"{response}"
        
    def deposit(self, amount, initial_deposit):
        '''Depositing specified amount to account'''
        try:
            self.balance = float(initial_deposit + amount)
            account = (self.balance, self.username, self.password)
            db.CryptoHiveDB().account_update_data(account)
            print(f"Deposit of {amount} successful! Your new balance is {self.balance}.")
            return self.balance
        except Exception as e:
            return f"Error, failed to process deposit: \n\t{e}"

    def withdraw(self, amount, initial_deposit):
        '''Withdrawing specified amount from account'''
        try:
            if amount > initial_deposit:
                return "Withdrawal failed insufficient funds!!!"
            
            self.balance = float(initial_deposit - amount)
            account = (self.balance, self.username, self.password)
            db.CryptoHiveDB().account_update_data(account)
            print(f"Withdrawal of {amount} successful! Your new balance is {self.balance}.")
            return self.balance
        except Exception as e:
            return f"Error, Failed to process withdrawal: \n\t{e}"

    def update_balance(self, action, amount):  
        '''Update account balance based on action'''
        try:
            account = db.CryptoHiveDB().read_account(self.username, self.password)  
            
            if account:
                # updating account by either withdrawing or depositing
                username, password, initial_deposit = account[0][1], account[0][2], account[0][3]
                initial_deposit = float(initial_deposit)
                if action.startswith('d'):
                    balance = self.deposit(amount, initial_deposit)
                    details = f"Deposit of {amount}"
                    transaction = (username, details, amount)
                    db.CryptoHiveDB().transactions_insert_data(transaction)
                elif action.startswith('w'):
                    details = f'Withdraw of {amount}'
                    balance = self.withdraw(amount, initial_deposit)
                    transaction = (username, details, amount)
                    db.CryptoHiveDB().transactions_insert_data(transaction)
                else:
                    print(f"{action.title()} not found!")    

            else: 
                return "Account not found!"

            return balance
        except Exception as e:
            return f"Error, failed to update balance: \n\t{e}"