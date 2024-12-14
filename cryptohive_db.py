import sqlite3

class CryptoHiveDB():
        # initialize db
        def __init__(self):
                self.conn = sqlite3.connect("cyptohive.db")
                self.c = self.conn.cursor()
                self.initialize_db()
        
       

        def initialize_db(self):
                '''Create a new database'''
                # Create Accounts table
                self.c.execute("""
                CREATE TABLE IF NOT EXISTS Accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password VARCHAR NOT NULL,
                        balance FLOAT NOT NULL
                )
                """)

                # Create Portfolio table
                self.c.execute("""
                CREATE TABLE IF NOT EXISTS Portfolio (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        username TEXT,
                        action TEXT NOT NULL,
                        asset TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price FLOAT NOT NULL,
                        holding BOOLEAN DEFAULT TRUE,
                        FOREIGN KEY (username) REFERENCES Accounts(username)
                )
                """)

                # Create Transactions table
                self.c.execute("""
                CREATE TABLE IF NOT EXISTS Transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        username TEXT,
                        action TEXT NOT NULL,
                        asset TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        amount FLOAT NOT NULL,
                        FOREIGN KEY (username) REFERENCES Accounts(username)
                )
                """)

                # Commit changes and close the connection
                self.conn.commit()
                

        def account_insert_data(self, account):
                '''Insert user account data into database'''
                try:
                        self.c.execute("INSERT INTO Accounts (username, password, balance) VALUES (?, ?, ?)", account)
                        self.conn.commit()
                        return "Success"
                except Exception as e:
                        return f"Error creating new user: \n\t{e}."

        def portfolio_insert_data(self, portfolio):
                '''Insert user portfolio data into database'''
                self.c.execute("INSERT INTO Portfolio (username, action, asset, quantity, price) VALUES (?, ?, ?, ?, ?)", portfolio)
                self.conn.commit()
                return

        def transactions_insert_data(self, transaction):
                '''Insert user transaction data into database'''
                self.c.execute("INSERT INTO Transactions (username, action, asset, quantity, amount) VALUES (?, ?, ?, ?, ?)", transaction)
                self.conn.commit()
                return

        def account_update_data(self, account):
                '''Update user account data'''
                try:
                        self.c.execute("UPDATE Accounts SET balance = ? WHERE username = ? and password = ?", account)
                        self.conn.commit()
                        return "Success"
                except Exception as e:
                        return f"Error updating user balance: \n\t{e}."
                

        def portfolio_update_data(self, username, action, asset, quantity, price):
                '''Update the portfolio data for the specified user and asset'''
                self.c.execute("UPDATE Portfolio SET quantity = ?, price = ? WHERE username = ? and action = ? and asset = ?", (quantity, price, username, action, asset))
                self.conn.commit()
                return

        def read_account(self, username, password):
                '''Read user account data'''
                try:
                        self.c.execute("SELECT * FROM Accounts WHERE username = ? and password = ?", (username, password))
                        account =  self.c.fetchall()
                except Exception as e:
                        account = 'Invalid username or password'
                return account


        def read_portfolio(self, username):
                '''Read the portfolio from the database'''
                self.c.execute("SELECT * FROM Portfolio WHERE username = ?", (username,))
                portfolio =  self.c.fetchall()
                if portfolio:
                        return portfolio
                else:
                        return None
        
        def active_holdings(self, username):
                '''Read the active holdings for the specified user'''
                self.c.execute("SELECT * FROM Portfolio WHERE username =? and holding =?", (username, True))
                active_holdings =  self.c.fetchall()
                return active_holdings
        
        def close_holding(self, details):
                '''Close a holding by updating the holding status in the portfolio'''
                self.c.execute("UPDATE Portfolio SET holding = False WHERE username = ? and id = ?",
                               details)
                self.conn.commit()
                return 'success'
        
        def read_transactions(self, username):
                '''Read the transactions for the specified user'''
                self.c.execute("SELECT * FROM Transactions WHERE username =?", (username,))
                transactions =  self.c.fetchall()
                return transactions

        def close_db(self):
                '''Close the database connection'''
                self.c.close()
                self.conn.close()


details = ('denzel', 4)
CryptoHiveDB().close_holding(details)


print(CryptoHiveDB().active_holdings('denzel'))