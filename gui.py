from customtkinter import *
from PIL import Image, Image
import asset as ast
import trading_data as td
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import time



def setup_gui(client_functions):
    # Create a new window
    app = CTk()
    app.title = "CryptoHive Trading Platform"
    app.geometry("1000x650+0+0")
    start_window(app, client_functions)
    return app


def start_window(app, client_functions):
    title = CTkLabel(master=app, text="CryptoHive Trading Platform", font=("Helvetica", 37), text_color="gold")
    title.place(relx=0.75, rely=0.3, anchor="center")

    slogan = CTkLabel(master=app, text="Buzzing Towards Financial Freedom.", font=("Helvetica", 22))
    slogan.place(relx=0.75, rely=0.37, anchor="center")

    description = CTkLabel(master=app, text="Login or signup.", font=("Helvetica", 19), text_color="gold")
    description.place(relx=0.75, rely=0.47, anchor="center")

    login_button = CTkButton(master=app, text="Login", font=("Helvetica", 20), command=lambda : login(app, client_functions))
    login_button.place(relx=0.75, rely=0.55, anchor="center")

    signup_button = CTkButton(master=app, text="Sign Up", font=("Helvetica", 20), command= lambda : signup(app, client_functions))
    signup_button.place(relx=0.75, rely=0.65, anchor="center")

def login(app, client_functions):
    if app.winfo_children():
        for widget in app.winfo_children():
            widget.destroy()

    title = CTkLabel(master=app, text="Login", font=("Helvetica", 45))
    title.place(relx=0.5, rely=0.3, anchor="center")
    
    username_label = CTkLabel(master=app, text="Username:", font=("Helvetica", 20))
    username_label.place(relx=0.35, rely=0.4, anchor="center")

    username_entry = CTkEntry(master=app)
    username_entry.place(relx=0.5, rely=0.4, anchor="center")

    password_label = CTkLabel(master=app, text="Password:", font=("Helvetica", 20))
    password_label.place(relx=0.35, rely=0.5, anchor="center")
    
    password_entry = CTkEntry(master=app, show="*")
    password_entry.place(relx=0.5, rely=0.5, anchor="center")
    
    login_button = CTkButton(master=app, text="Login", font=("Helvetica", 20), command=lambda: login_confirmation(app, username_entry.get(), password_entry.get(), client_functions))
    login_button.place(relx=0.5, rely=0.6, anchor="center")

def signup(app, client_functions):
    if app.winfo_children():
        for widget in app.winfo_children():
            widget.destroy()

    title = CTkLabel(master=app, text="Signup", font=("Helvetica", 45))
    title.place(relx=0.5, rely=0.3, anchor="center")
    
    username_label = CTkLabel(master=app, text="Username:", font=("Helvetica", 20))
    username_label.place(relx=0.35, rely=0.4, anchor="w")

    username_entry = CTkEntry(master=app)
    username_entry.place(relx=0.69, rely=0.4, anchor="e")

    password_label = CTkLabel(master=app, text="Password:", font=("Helvetica", 20))
    password_label.place(relx=0.35, rely=0.5, anchor="w")
    
    password_entry = CTkEntry(master=app, show="*")
    password_entry.place(relx=0.69, rely=0.5, anchor="e")

    confirm_password_label = CTkLabel(master=app, text="Confirm Password:", font=("Helvetica", 20))
    confirm_password_label.place(relx=0.35, rely=0.6, anchor="w")
    
    confirm_password_entry = CTkEntry(master=app, show="*")
    confirm_password_entry.place(relx=0.69, rely=0.6, anchor="e")

    initial_deposit_label = CTkLabel(master=app, text="Initial Deposit:", font=("Helvetica", 20))
    initial_deposit_label.place(relx=0.35, rely=0.7, anchor="w")
    
    initial_deposit_entry = CTkEntry(master=app, validate="key", validatecommand=(app.register(validate_initial_deposit), "%P"))
    initial_deposit_entry.place(relx=0.69, rely=0.7, anchor="e")
    
    
    signup_button = CTkButton(master=app, text="Signup", font=("Helvetica", 20), command=lambda: signup_confirmation(app, username_entry.get(), password_entry.get(), initial_deposit_entry.get(), client_functions))
    signup_button.place(relx=0.5, rely=0.8, anchor="center")

def validate_initial_deposit(value):
    if value == "":
        return True  
    try:
        float(value)  
        return True  
    except ValueError:
        return False  

def login_confirmation(app, username, password, client_functions):
    if app.winfo_children():
        for widget in app.winfo_children():
            widget.destroy()

    response = client_functions["login"](username, password)
    if response is not None:
        try: 
            username, password, balance = response.split(",")
            balance = float(balance)
            login_confirm = CTkLabel(master=app, text="Login Successful", font=("Helvetica", 45), text_color="gold")
            login_confirm.place(relx=0.5, rely=0.3, anchor="center")
            welcome_msg = CTkLabel(master=app, text=f"Welcome {username}", font=("Helvetica", 35))
            welcome_msg.place(relx=0.5, rely=0.45, anchor="center")

            if balance > 0:
                color = "green"
            else:
                color = "red"

            balance_label = CTkLabel(master=app, text=f"Your current balance: ${balance:.2f}", font=("Helvetica",30), text_color=color)
            balance_label.place(relx=0.5, rely=0.6, anchor="center")
            
            proceed_button = CTkButton(master=app, text="Proceed", font=("Helvetica", 20), command=lambda: home_page(username, password, app, client_functions)) 
            proceed_button.place(relx=0.5, rely=0.7, anchor="center")
        except Exception as e:
            print(f"{e}")
            signup_error = CTkLabel(master=app, text="Error occurred while logging in", font=("Helvetica", 45), text_color="red")
            signup_error.place(relx=0.5, rely=0.3, anchor="center")
    else:  
        login_error = CTkLabel(master=app, text="Invalid credentials", font=("Helvetica", 45), text_color="red")
        login_error.place(relx=0.5, rely=0.3, anchor="center")

    

def signup_confirmation(app, username, password, deposit, client_functions):
    if app.winfo_children():
        for widget in app.winfo_children():
            widget.destroy()

    response = client_functions["signup"](username, password, deposit)
    try:
        username, password, balance = response.split(",")
        balance = float(deposit)
        signup_confirmed = CTkLabel(master=app, text="Signup Successful", font=("Helvetica", 45), text_color="gold")
        signup_confirmed.place(relx=0.5, rely=0.3, anchor="center")
        welcome_msg = CTkLabel(master=app, text=f"Welcome {username}", font=("Helvetica", 35))
        welcome_msg.place(relx=0.5, rely=0.45, anchor="center")

        if balance > 0:
            color = "green"
        else:
            color = "red"

        balance_label = CTkLabel(master=app, text=f"Your current balance: ${balance}", font=("Helvetica",30), text_color=color)
        balance_label.place(relx=0.5, rely=0.6, anchor="center")
        proceed_button = CTkButton(master=app, text="Proceed", font=("Helvetica", 20), command=lambda: login(app, client_functions)) 
        proceed_button.place(relx=0.5, rely=0.7, anchor="center")
    except:
        signup_error = CTkLabel(master=app, text="Error signing up. Please try again.", font=("Helvetica", 45), text_color="red")
        signup_error.place(relx=0.5, rely=0.3, anchor="center")
    
def plot_data(username, password, graph_frame, client_functions, app, asset="Bitcoin",):
    if graph_frame.winfo_children():
        for widget in graph_frame.winfo_children():
            widget.destroy()
    # Fetch the price history
    assets={
        'Bitcoin':'BTC-USD',
        'Ethereum':'ETH-USD',
        'Gold':'GC=F',
        'Silver':'SI=F',
        'EURUSD':'EURUSD=X',
    }
    price_history = td.asset_price_history(assets[asset])
    
    if price_history is not None:
        # Create a line plot
        plt.figure(figsize=(10, 5))
        plt.plot(price_history.index, price_history['Close'], label=f'{assets[asset]}', color='gold', linewidth=2)
        plt.title(f'{asset} Closing Prices Over the Last 30 Days')
        plt.xlabel('Date and Time')
        plt.ylabel('Closing Price (USD)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()

        # Show the plot in the CustomTkinter window
        canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        button_frame = CTkFrame(graph_frame)
        button_frame.place(relx=0.5, rely=0.05, anchor="center")  # Position the button frame at the top center

        # Create buttons
        buy_button = CTkButton(button_frame, text="BUY", text_color="white", fg_color='darkblue', command=lambda: process_transaction(username, password, asset, 'buy', graph_frame, client_functions, app))
        buy_button.pack(side=LEFT, padx=(0, 10))  # Add some padding between buttons

        sell_button = CTkButton(button_frame, text="SELL", text_color="white", fg_color='darkblue', command=lambda: process_transaction(username, password, asset, 'sell', graph_frame, client_functions, app))
        sell_button.pack(side=LEFT)

def process_transaction(username, password, asset, action, graph_frame, client_functions, app):
    transaction_frame = CTkFrame(graph_frame)
    transaction_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)

    title_label = CTkLabel(transaction_frame, text=f"{action.upper()} {asset.upper()}", font=("Helvetica", 45))
    title_label.place(relx=0.5, rely=0.3, anchor="center")

    amount_label = CTkLabel(transaction_frame, text="Enter Quantity:", font=("Helvetica", 20))
    amount_label.place(relx=0.5, rely=0.5, anchor="center")

    amount_entry = CTkEntry(transaction_frame)
    amount_entry.place(relx=0.5, rely=0.6, anchor="center")

    confirm_button = CTkButton(transaction_frame, text="Confirm", font=("Helvetica", 20), command=lambda: confirm_transaction(username, password, asset, action, amount_entry.get(), transaction_frame, client_functions, app))
    confirm_button.place(relx=0.5, rely=0.7, anchor="center")

def confirm_transaction(username, password, asset, action, amount, transaction_frame, client_functions, app):
    if transaction_frame.winfo_children():
        for widget in transaction_frame.winfo_children():
            widget.destroy()

    response = client_functions["execute_trade"](username, password, asset, amount, action)
    if response:
        title =  CTkLabel(master=transaction_frame, text="Trade successfully executed", font=("Helvetica", 40))
        title.place(relx=0.5, rely=0.2, anchor="center")

        message = f"{action} of {asset}. Total {amount}"
        info_label = CTkLabel(master=transaction_frame, text=message, font=("Helvetica", 20))
        info_label.place(relx=0.5, rely=0.4, anchor="center")

        proceed_button = CTkButton(master=transaction_frame, text="Proceed", font=("Helvetica", 20), command=lambda : view_holdings(app, client_functions, username, password, transaction_frame))
        proceed_button.place(relx=0.5, rely=0.6, anchor="center") 


def home_page(username, password, app, client_functions):
    if app.winfo_children():
        for widget in app.winfo_children():
            widget.destroy()

    asset_frame = CTkFrame(master=app, fg_color='black', border_color="white", border_width=1, )
    asset_frame.place(relx=-0.01, rely=-0.01, relwidth=0.25, relheight=1.02)

    graph_frame = CTkFrame(master=app, fg_color="#B8860B")
    graph_frame.place(relx=0.25, rely=0.0, relwidth=0.8, relheight=1.02)

    title = CTkLabel(asset_frame, text="Assets", text_color="white", font=("Helvetica", 25))
    title.place(relx=0.5, rely=0.1, anchor="center")
    assets = ast.Asset().get_values()
    y = 0.2

    for asset, value in assets.items():
        asset_label = CTkLabel(asset_frame, text=f"{asset}", text_color="white", font=("Helvetica", 15))
        asset_label.place(relx=0.1, rely=y, anchor="w")
        try: 
            graph_button = CTkButton(asset_frame, text=f"{value:.2f}", fg_color="darkblue", font=("Helvetica", 15), width = 100, border_width=1, border_color="white", command=lambda asset=asset: plot_data(username, password, graph_frame, client_functions, app, asset))
        except:
                graph_button = CTkButton(asset_frame, text=f"{value}", fg_color="darkblue", font=("Helvetica", 15), width = 100, border_width=1, border_color="white", command=lambda asset=asset: plot_data(username, password, graph_frame, client_functions, app, asset))
        graph_button.place(relx=0.9, rely=y, anchor="e")
        y += 0.06

def close_position(id):
    messagebox.askyesno("Close Postion", "Are you sure you want to close?")


def view_holdings(app, client_functions, username, password, transaction_frame):
    if transaction_frame:
        transaction_frame.destroy()

    if app.winfo_children():
        for widget in app.winfo_children():
            widget.destroy()

    data = client_functions["view_holdings"](username, password)

    page_title = CTkLabel(master=app, text="Holdings", font=("Helvetica", 45))
    page_title.place(relx=0.5, rely=0.1, anchor="center")

    id_title = CTkLabel(master=app, text="ID", font=("Helvetica",20) )
    id_title.place(relx=0.05, rely=0.2, anchor="center")

    date_title = CTkLabel(master=app, text="Date", font=("Helvetica", 20))
    date_title.place(relx=0.15, rely=0.2, anchor="center")

    asset_title = CTkLabel(master=app, text="Asset", font=("Helvetica",20) )
    asset_title.place(relx=0.275, rely=0.2, anchor="center")

    action_title = CTkLabel(master=app, text="Action", font=("Helvetica", 20))
    action_title.place(relx=0.45, rely=0.2, anchor="center")

    quantity_title = CTkLabel(master=app, text="Quantity", font=("Helvetica", 20))
    quantity_title.place(relx=0.55, rely=0.2, anchor="center")

    cost_title = CTkLabel(master=app, text="Total Cost", font=("Helvetica", 20))
    cost_title.place(relx=0.7, rely=0.2, anchor="center")

    close_title = CTkLabel(master=app, text="Cost Postion", font=("Helvetica", 20))
    close_title.place(relx=0.85, rely=0.2, anchor="center")

    database = [()]

    y = 0.25
    try: 
        if data:
            for i, line in enumerate(data):
                id, date, user_name, action, asset, quantity, cost, holding = data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7]  
                    # Make sure only active holdings are printed 
                if holding:
                    count += 1
                    id_label = CTkLabel(master=app, text=f"{id}", font=("Helvetica", 15))
                    id_label.place(relx=0.005, rely=y, anchor="w")
                    
                    date_label = CTkLabel(master=app, text=f"{date}", font=("Helvetica", 15))
                    date_label.place(relx=0.15, rely=y, anchor="w")

                    asset_label = CTkLabel(master=app, text=f"{asset}", font=("Helvetica", 15))
                    asset_label.place(relx=0.275, rely=y, anchor="w")

                    action_label = CTkLabel(master=app, text=f"{action}", font=("Helvetica", 15))
                    action_label.place(relx=0.45, rely=y, anchor="w")

                    quantity_label = CTkLabel(master=app, text=f"{quantity}", font=("Helvetica", 15))
                    quantity_label.place(relx=0.55, rely=y, anchor="w")

                    cost_label = CTkLabel(master=app, text=f"{cost}", font=("Helvetica", 15))
                    cost_label.place(relx=0.7, rely=y, anchor="w")

                    close_position_button = CTkButton(master=app, text=f"Close", font=("Helvetica", 15), command=lambda id=id: close_position(id))
                    close_position_button.place(relx=0.85, rely=y, anchor="w")
    except Exception as e:
        print(f"Error: {e}")

def account_details():
    page_title = CTkLabel(master=app, text="Account Details", font=("Helvetica", 45))
    page_title.place(relx=0.5, rely=0.1, anchor="center")

    username_label = CTkLabel(master=app, text="Username", font=("Helvetica", 20))
    username_label.place(relx=0.25, rely=0.2, anchor="center")

    balance = CTkLabel(master=app, text="Balance", font=("Helvetica", 20))
    balance.place(relx=0.75, rely=0.2, anchor="center")

    withdraw_label = CTkLabel(master=app, text="Withdraw", font=("Helvetica", 30))
    withdraw_label.place(relx=0.25, rely=0.5, anchor="center")

    deposit_label = CTkLabel(master=app, text="Deposit", font=("Helvetica", 30))
    deposit_label.place(relx=0.75, rely=0.5, anchor="center")

    withdraw_amount_entry = CTkEntry(master=app, )
    withdraw_amount_entry.place(relx=0.25, rely=0.6, anchor="center")

    deposit_amount_entry = CTkEntry(master=app, )
    deposit_amount_entry.place(relx=0.75, rely=0.6, anchor="center")

    withdraw_button = CTkButton(master=app, text="Withdraw", font=("Helvetica", 20), command=lambda : deposit_withdraw("withdraw", withdraw_amount_entry.get()))
    withdraw_button.place(relx=0.25, rely=0.7, anchor="center")

    deposit_button = CTkButton(master=app, text="Deposit", font=("Helvetica", 20), command=lambda : deposit_withdraw('deposit', deposit_amount_entry.get()))
    deposit_button.place(relx=0.75, rely=0.7, anchor="center")


def deposit_withdraw(action, amount=0):
    messagebox.askyesno(f"{action}", f"Do you want to {action} {amount}")




