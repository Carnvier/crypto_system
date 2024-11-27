import sqlite3

class CryptoHiveDB():
        # initialize db
        def __init__(self):
                self.conn = sqlite3.connect("cyptohive.db")
                self.c = self.conn.cursor()
                self.initialize_db()
        
       

        def initialize_db(self):
                # Create Accounts table
                self.c.execute("""
                CREATE TABLE IF NOT EXISTS Accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
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
                self.c.execute("INSERT INTO Accounts (username, password, balance) VALUES (?, ?, ?)", account)
                self.conn.commit()
               
                return

        def portfolio_insert_data(self, portfolio):
                self.c.execute("INSERT INTO Portfolio (username, action, asset, quantity, price) VALUES (?, ?, ?, ?, ?)", portfolio)
                self.conn.commit()
                return

        def transactions_insert_data(self, transaction):
                self.c.execute("INSERT INTO Transactions (username, action, asset, quantity, amount) VALUES (?, ?, ?, ?, ?)", transaction)
                self.conn.commit()
                return

        def account_update_data(self, username, password, balance):
                self.c.execute("UPDATE Accounts SET balance = ? WHERE username = ? and password = ?", (balance, username, password))
                self.conn.commit()
                return

        def portfolio_update_data(self, username, action, asset, quantity, price):
                self.c.execute("UPDATE Portfolio SET quantity = ?, price = ? WHERE username = ? and action = ? and asset = ?", (quantity, price, username, action, asset))
                self.conn.commit()
                return

        def read_account(self, username, password):
                self.c.execute("SELECT * FROM Accounts WHERE username = ? and password = ?", (username, password))
                account =  self.c.fetchall()
                return account


        def read_portfolio(self, username):
                self.c.execute("SELECT * FROM Portfolio WHERE username = ?", (username))
                portfolio =  self.c.fetchall()
                return portfolio
        
        def read_transactions(self, username):
                self.c.execute("SELECT * FROM Transactions WHERE username =?", (username))
                transactions =  self.c.fetchall()
                return transactions

        def close_db(self):
                self.c.close()
                self.conn.close()

account = CryptoHiveDB().read_account('denzel', 'mil12345')
CryptoHiveDB().close_db()
