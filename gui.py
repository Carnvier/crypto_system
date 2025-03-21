from customtkinter import *
from PIL import Image, Image
import asset as ast
import trading_data as td
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import time
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np


def setup_gui(client_functions):
    '''Create a new window'''
    app = CTk()
    app.title = "CryptoHive Trading Platform"
    app.geometry("1000x650+0+0")
    start_window(app, client_functions)
    return app


def nav(username, password, app, client_functions):
    nav_frame =CTkFrame(master=app, height=25, width=650)
    nav_frame.place(relx=1, rely=0, anchor="ne" )

    charts_button=CTkButton(master=nav_frame, text="Charts", command=lambda:home_page(username, password, app, client_functions))
    charts_button.place(relx = 0.0, rely = 0.5, anchor="w")

    holdings_button=CTkButton(master=nav_frame, text="Holdings", command=lambda:view_holdings(app, client_functions, username, password, nav_frame))
    holdings_button.place(relx = 0.2, rely = 0.5, anchor="w")

    transaction_button=CTkButton(master=nav_frame, text="Transactions", command=lambda:view_transactions(app, client_functions, username, password, nav_frame))
    transaction_button.place(relx = 0.4, rely = 0.5, anchor="w")

    profile_button=CTkButton(master=nav_frame, text="Profile", command=lambda:account_details(app, client_functions, username, password, nav_frame))
    profile_button.place(relx = 0.6, rely = 0.5, anchor="w")

    logout_button=CTkButton(master=nav_frame, text="Logout", command=lambda:logout(app, client_functions, username, password, nav_frame))
    logout_button.place(relx = 0.8, rely = 0.5, anchor="w")


# Function to start the main window
def start_window(app, client_functions):
    global root, background_label, frames, current_frame

    root = app  # Reference to the main application window

    wallpaper_frame = CTkFrame(master=root, fg_color="#B8860B")
    wallpaper_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1, anchor='nw')

    title = CTkLabel(master=app, text="CryptoHive Trading Platform", font=("Helvetica", 37), text_color="gold")
    title.place(relx=0.75, rely=0.3, anchor="center")

    slogan = CTkLabel(master=app, text="Buzzing Towards Financial Freedom.", font=("Helvetica", 22))
    slogan.place(relx=0.75, rely=0.37, anchor="center")

    description = CTkLabel(master=app, text="Login or signup.", font=("Helvetica", 19), text_color="gold")
    description.place(relx=0.75, rely=0.47, anchor="center")

    login_button = CTkButton(master=app, text="Login", font=("Helvetica", 20), command=lambda : login(app, client_functions, wallpaper_frame))
    login_button.place(relx=0.75, rely=0.55, anchor="center")

    signup_button = CTkButton(master=app, text="Sign Up", font=("Helvetica", 20), command= lambda : signup(app, client_functions, wallpaper_frame))
    signup_button.place(relx=0.75, rely=0.65, anchor="center")

# login function
def login(app, client_functions, wallpaper_frame):
    '''collecting data for login'''
    if app.winfo_children():
        for widget in app.winfo_children():
            if widget != wallpaper_frame:
                widget.destroy()

    signup_button = CTkButton(app, text="Signup", font=("Helvetica", 20), command=lambda : signup(app, client_functions, wallpaper_frame))
    signup_button.place(relx=1, rely=0, anchor="ne")

    title = CTkLabel(master=app, text="Login", font=("Helvetica", 45))
    title.place(relx=0.75, rely=0.3, anchor="center")
    
    username_label = CTkLabel(master=app, text="Username:", font=("Helvetica", 20))
    username_label.place(relx=0.65, rely=0.4, anchor="w")

    username_entry = CTkEntry(master=app)
    username_entry.place(relx=0.85, rely=0.4, anchor="center")

    password_label = CTkLabel(master=app, text="Password:", font=("Helvetica", 20))
    password_label.place(relx=0.65, rely=0.5, anchor="w")
    
    password_entry = CTkEntry(master=app, show="*")
    password_entry.place(relx=0.85, rely=0.5, anchor="center")
    
    login_button = CTkButton(master=app, text="Login", font=("Helvetica", 20), command=lambda: login_confirmation(app, username_entry.get(), password_entry.get(), client_functions, wallpaper_frame))
    login_button.place(relx=0.75, rely=0.6, anchor="center")

def login_confirmation(app, username, password, client_functions, wallpaper_frame):
    '''confirmation of user's login details'''
    if app.winfo_children():
        for widget in app.winfo_children():
            if widget != wallpaper_frame:
                widget.destroy()

    response = client_functions["login"](username, password)
    if response is not None:
        try: 
            username, password, balance = response.split(",")
            balance = float(balance)
            login_confirm = CTkLabel(master=app, text="Login Successful", font=("Helvetica", 45), text_color="gold")
            login_confirm.place(relx=0.75, rely=0.3, anchor="center")
            welcome_msg = CTkLabel(master=app, text=f"Welcome {username}", font=("Helvetica", 35))
            welcome_msg.place(relx=0.75, rely=0.45, anchor="center")

            if balance > 0:
                color = "green"
            else:
                color = "red"

            balance_label = CTkLabel(master=app, text=f"Your current balance: ${balance:.2f}", font=("Helvetica",18), text_color=color)
            balance_label.place(relx=0.75, rely=0.6, anchor="center")
            
            proceed_button = CTkButton(master=app, text="Proceed", font=("Helvetica", 20), command=lambda: home_page(username, password, app, client_functions)) 
            proceed_button.place(relx=0.75, rely=0.7, anchor="center")
        except:
            signup_error = CTkLabel(master=app, text=response, font=("Helvetica", 30), text_color="red")
            signup_error.place(relx=0.75, rely=0.3, anchor="center")
            try_again_button = CTkButton(master=app, text="Try Again", font=("Helvetica", 20), command=lambda: login(app, client_functions, wallpaper_frame)) 
            try_again_button.place(relx=0.75, rely=0.5, anchor="center")
    else:  
        login_error = CTkLabel(master=app, text="Failed to login please try again.", font=("Helvetica", 30), text_color="red")
        login_error.place(relx=0.75, rely=0.3, anchor="center")
        try_again_button = CTkButton(master=app, text="Try Again", font=("Helvetica", 20), command=lambda: login(app, client_functions, wallpaper_frame)) 
        try_again_button.place(relx=0.75, rely=0.5, anchor="center")

# signup function
def signup(app, client_functions, wallpaper_frame):
    '''collecting data for account setup'''
    if app.winfo_children():
        for widget in app.winfo_children():
            if widget != wallpaper_frame:
                widget.destroy()

    login_button = CTkButton(app, text="Login", font=("Helvetica", 20), command=lambda : login(app, client_functions, wallpaper_frame))
    login_button.place(relx=1, rely=0, anchor="ne")

    title = CTkLabel(master=app, text="Signup", font=("Helvetica", 45))
    title.place(relx=0.75, rely=0.3, anchor="center")
    
    username_label = CTkLabel(master=app, text="Username:", font=("Helvetica", 20))
    username_label.place(relx=0.55, rely=0.4, anchor="w")

    username_entry = CTkEntry(master=app)
    username_entry.place(relx=0.85, rely=0.4, anchor="center")

    password_label = CTkLabel(master=app, text="Password:", font=("Helvetica", 20))
    password_label.place(relx=0.55, rely=0.5, anchor="w")
    
    password_entry = CTkEntry(master=app, show="*")
    password_entry.place(relx=0.85, rely=0.5, anchor="center")

    confirm_password_label = CTkLabel(master=app, text="Confirm Password:", font=("Helvetica", 20))
    confirm_password_label.place(relx=0.55, rely=0.6, anchor="w")
    
    confirm_password_entry = CTkEntry(master=app, show="*")
    confirm_password_entry.place(relx=0.85, rely=0.6, anchor="center")

    initial_deposit_label = CTkLabel(master=app, text="Initial Deposit:", font=("Helvetica", 20))
    initial_deposit_label.place(relx=0.55, rely=0.7, anchor="w")
    
    initial_deposit_entry = CTkEntry(master=app, validate="key", validatecommand=(app.register(validate_initial_deposit), "%P"))
    initial_deposit_entry.place(relx=0.85, rely=0.7, anchor="center")
    
    
    signup_button = CTkButton(master=app, text="Signup", font=("Helvetica", 20), command=lambda: signup_confirmation(app, username_entry.get(), password_entry.get(), confirm_password_entry.get(), initial_deposit_entry.get(), client_functions, wallpaper_frame))
    signup_button.place(relx=0.75, rely=0.8, anchor="center")

def validate_initial_deposit(value):
    '''validating if user deposit input is numeric'''
    if value == "":
        return True  
    try:
        float(value)  
        return True  
    except ValueError:
        return False  



    

def signup_confirmation(app, username, password, password_2nd, deposit, client_functions, wallpaper_frame):
    '''confirming if user account has been created'''
    if password != password_2nd:
        messagebox.showerror("Password", "Password do not match")
        signup(app, client_functions, wallpaper_frame)
        return
         
    if app.winfo_children():
        for widget in app.winfo_children():
            if widget != wallpaper_frame:
                widget.destroy()

    response = client_functions["signup"](username, password, deposit)
    try:
        username, password, balance = response.split(",")
        balance = float(balance)
        signup_confirmed = CTkLabel(master=app, text="Signup Successful", font=("Helvetica", 45), text_color="gold")
        signup_confirmed.place(relx=0.75, rely=0.3, anchor="center")
        welcome_msg = CTkLabel(master=app, text=f"Welcome {username}", font=("Helvetica", 35))
        welcome_msg.place(relx=0.75, rely=0.45, anchor="center")

        if balance > 0:
            color = "green"
        else:
            color = "red"

        balance_label = CTkLabel(master=app, text=f"Your current balance: ${balance}", font=("Helvetica",20), text_color=color)
        balance_label.place(relx=0.75, rely=0.6, anchor="center")
        proceed_button = CTkButton(master=app, text="Proceed", font=("Helvetica", 20), command=lambda: login(app, client_functions, wallpaper_frame)) 
        proceed_button.place(relx=0.75, rely=0.7, anchor="center")
    except:
        signup_error = CTkLabel(master=app, text=f"{response}", font=("Helvetica", 22), text_color="red")
        signup_error.place(relx=0.75, rely=0.3, anchor="center")
        try_again_button = CTkButton(master=app, text="Try Again", font=("Helvetica", 20), command=lambda: signup(app, client_functions, wallpaper_frame)) 
        try_again_button.place(relx=0.75, rely=0.5, anchor="center")

def home_page(username, password, app, client_functions):
    '''Home page display function'''
    if app.winfo_children():
        for widget in app.winfo_children():
            widget.destroy()

    nav(username, password, app, client_functions)

    asset_frame = CTkFrame(master=app, fg_color='black', border_color="white", border_width=1, )
    asset_frame.place(relx=-0.01, rely=-0.01, relwidth=0.25, relheight=1.02)

    graph_frame = CTkFrame(master=app, fg_color="#B8860B")
    graph_frame.place(relx=0.25, rely=0.05, relwidth=0.8, relheight=1.02)

    title = CTkLabel(asset_frame, text="Assets", text_color="white", font=("Helvetica", 25))
    title.place(relx=0.5, rely=0.1, anchor="center")
    assets = ast.Asset().get_values()
    

    def update_prices():
        # Clear existing labels and buttons
        try:
            for widget in asset_frame.winfo_children():
                if widget != title:
                        widget.destroy()
        except:
            pass

        y = 0.2
        # Fetch latest asset values
        assets = ast.Asset().get_values()  # Fetch updated values

        for asset, value in assets.items():
            asset_label = CTkLabel(asset_frame, text=f"{asset}", text_color="white", font=("Helvetica", 15))
            asset_label.place(relx=0.1, rely=y, anchor="w")

            # Create graph button
            try: 
                graph_button = CTkButton(
                    asset_frame, 
                    text=f"{value:.2f}", 
                    fg_color="darkblue", 
                    font=("Helvetica", 15), 
                    width=100, 
                    border_width=1, 
                    border_color="white", 
                    command=lambda asset=asset: plot_data(username, password, graph_frame, client_functions, app, asset)
                )
            except:
                graph_button = CTkButton(
                    asset_frame, 
                    text=f"{value}", 
                    fg_color="darkblue", 
                    font=("Helvetica", 15), 
                    width=100, 
                    border_width=1, 
                    border_color="white", 
                    command=lambda asset=asset: plot_data(username, password, graph_frame, client_functions, app, asset)
                )
            graph_button.place(relx=0.9, rely=y, anchor="e")
            y += 0.06

        # Schedule the next price update
        try:
            app.after(1000, lambda: update_prices)  # Call update_prices again after 5000 milliseconds
        except: 
            print('Update Failed')

    update_prices() 
    
def plot_data(username, password, graph_frame, client_functions, app, asset="Bitcoin",):
    '''Plotting a graph for specified asset'''
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
        plt.title(f'{asset} Trend')
        plt.xlabel('Date and Time', fontsize=8)
        plt.ylabel('Closing Price (USD)', fontsize=14)
        # Set x-ticks with increased spacing
        tick_positions = np.arange(0, len(price_history.index), step=5)  # Adjust step for spacing
        plt.xticks(tick_positions, price_history.index[tick_positions], rotation=45)
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
    else:
        message_label = CTkLabel(master=graph_frame, text='Market closed', font =('Helvetica', 35))
        message_label.place(relx = 0.5, rely = 0.5, anchor='center')


def process_transaction(username, password, asset, action, graph_frame, client_functions, app):
    transaction_frame = CTkFrame(graph_frame)
    transaction_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75, relheight=0.5)

    title_label = CTkLabel(transaction_frame, text=f"{action.upper()} {asset.upper()}", font=("Helvetica", 42))
    title_label.place(relx=0.5, rely=0.3, anchor="center")

    amount_label = CTkLabel(transaction_frame, text="Enter Quantity:", font=("Helvetica", 20))
    amount_label.place(relx=0.5, rely=0.5, anchor="center")

    amount_entry = CTkEntry(transaction_frame)
    amount_entry.place(relx=0.5, rely=0.6, anchor="center")

    confirm_button = CTkButton(transaction_frame, text="Confirm", font=("Helvetica", 20), command=lambda: confirm_transaction(username, password, asset, action, amount_entry.get(), transaction_frame, client_functions, app, graph_frame))
    confirm_button.place(relx=0.5, rely=0.7, anchor="center")

def confirm_transaction(username, password, asset, action, amount, transaction_frame, client_functions, app, graph_frame):
    if transaction_frame.winfo_children():
        for widget in transaction_frame.winfo_children():   
            widget.destroy()

    response = client_functions["execute_trade"](username, password, asset, amount, action)
    if response:
        title =  CTkLabel(master=transaction_frame, text="Trade", font=("Helvetica", 35))
        title.place(relx=0.5, rely=0.2, anchor="center")

        message = f"{response}"
        info_label = CTkLabel(master=transaction_frame, text=message, font=("Helvetica", 20))
        info_label.place(relx=0.5, rely=0.4, anchor="center")

        proceed_button = CTkButton(master=transaction_frame, text="Proceed", font=("Helvetica", 20), command=lambda asset=asset: plot_data(username, password, graph_frame, client_functions, app, asset))
        proceed_button.place(relx=0.5, rely=0.6, anchor="center") 
    else:
        messagebox.showerror("Trade", "Failed to execute trade!!!")


def view_holdings(app, client_functions, username, password, nav_frame):
   
    if app.winfo_children():    
        for widget in app.winfo_children():
            if widget != nav_frame:
                widget.destroy()
    
    
    holding_frame = CTkScrollableFrame(master = app, border_color="#")
    holding_frame.place(relx=0.5, rely=0.25, anchor="n", relwidth=0.95, relheight=0.7)

    data = client_functions["view_holdings"](username, password)

    page_title = CTkLabel(master=app, text="Holdings", font=("Helvetica", 45))
    page_title.place(relx=0.5, rely=0.1, anchor="center")

    id_title = CTkLabel(master=app, text="ID", font=("Helvetica",20) )
    id_title.place(relx=0.05, rely=0.2, anchor="w")

    date_title = CTkLabel(master=app, text="Date", font=("Helvetica", 20))
    date_title.place(relx=0.15, rely=0.2, anchor="w")

    asset_title = CTkLabel(master=app, text="Asset", font=("Helvetica",20) )
    asset_title.place(relx=0.325, rely=0.2, anchor="w")

    action_title = CTkLabel(master=app, text="Action", font=("Helvetica", 20))
    action_title.place(relx=0.45, rely=0.2, anchor="center")

    quantity_title = CTkLabel(master=app, text="Quantity", font=("Helvetica", 20))
    quantity_title.place(relx=0.55, rely=0.2, anchor="center")

    cost_title = CTkLabel(master=app, text="Total Cost", font=("Helvetica", 20))
    cost_title.place(relx=0.65, rely=0.2, anchor="w")

    close_title = CTkLabel(master=app, text="Cost Postion", font=("Helvetica", 20))
    close_title.place(relx=0.85, rely=0.2, anchor="w")

    count = 0
    y = 0.25

    try: 
        if data:
            for i, line in enumerate(data):
                id, date, user_name, action, asset, quantity, cost, holding = data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7]  
                    # Make sure only active holdings are printed 
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                if holding:
                    row_frame = CTkFrame(master=holding_frame)
                    row_frame.pack(fill="x", padx=5, pady=2)

                    id_label = CTkLabel(master=row_frame, text=f"{id}", font=("Helvetica", 15))
                    id_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

                    date_label = CTkLabel(master=row_frame, text=f"{date.strftime('%Y-%m-%d %H:%M')}", font=("Helvetica", 15))
                    date_label.grid(row=0, column=1, padx=(0, 10), sticky="e")

                    asset_label = CTkLabel(master=row_frame, text=f"{asset}", font=("Helvetica", 15))
                    asset_label.grid(row=0, column=2, padx=(0, 10), sticky="e")

                    action_label = CTkLabel(master=row_frame, text=f"{action}", font=("Helvetica", 15))
                    action_label.grid(row=0, column=3, padx=(0, 10), sticky="nsew")

                    quantity_label = CTkLabel(master=row_frame, text=f"{quantity}", font=("Helvetica", 15))
                    quantity_label.grid(row=0, column=4, padx=(0, 10), sticky="nsew")

                    cost_label = CTkLabel(master=row_frame, text=f"{cost:.2f}", font=("Helvetica", 15))
                    cost_label.grid(row=0, column=5, padx=(0, 10), sticky="e")

                    close_position_button = CTkButton(
                        master=row_frame, 
                        text="Close", 
                        font=("Helvetica", 15), 
                        command=lambda id=id: close_position(id, username, password, app, nav_frame, client_functions)
                    )
                    close_position_button.grid(row=0, column=6, padx=(50, 0), sticky="e")

                    for col in range(7):  # Adjust according to the number of columns
                        row_frame.grid_columnconfigure(col, minsize=175)


    except Exception as e:
        print(f"Error: {e}")



def view_transactions(app, client_functions, username, password, nav_frame):
   
    if app.winfo_children():    
        for widget in app.winfo_children():
            if widget != nav_frame:
                widget.destroy()
    
    
    transaction_frame = CTkScrollableFrame(master = app, border_color="#")
    transaction_frame.place(relx=0.5, rely=0.25, anchor="n", relwidth=0.95, relheight=0.7)

    data = client_functions["view_transactions"](username, password)

    page_title = CTkLabel(master=app, text="Transaction History", font=("Helvetica", 45))
    page_title.place(relx=0.5, rely=0.1, anchor="center")

    id_title = CTkLabel(master=app, text="ID", font=("Helvetica",20) )
    id_title.place(relx=0.01, rely=0.2, anchor="w")

    date_title = CTkLabel(master=app, text="Date", font=("Helvetica", 20))
    date_title.place(relx=0.25, rely=0.2, anchor="w")

    details_title = CTkLabel(master=app, text="Asset", font=("Helvetica",20) )
    details_title.place(relx=0.425, rely=0.2, anchor="w")

    amount_title = CTkLabel(master=app, text="Total Cost", font=("Helvetica", 20))
    amount_title.place(relx=0.65, rely=0.2, anchor="w")

    

    count = 0
    y = 0.25

    try: 
        if data:
            for i, line in enumerate(data):
                id, date, user_name, details, amount = data[i][0], data[i][1], data[i][2], data[i][3], data[i][4]  
                    # Make sure only active holdings are printed 
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                
                row_frame = CTkFrame(master=transaction_frame)
                row_frame.pack(fill="x", padx=5, pady=2)

                id_label = CTkLabel(master=row_frame, text=f"{id}", font=("Helvetica", 15))
                id_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

                date_label = CTkLabel(master=row_frame, text=f"{date.strftime('%Y-%m-%d %H:%M')}", font=("Helvetica", 15))
                date_label.grid(row=0, column=1, padx=(0, 10), sticky="w")

                details_label = CTkLabel(master=row_frame, text=f"{details}", font=("Helvetica", 15))
                details_label.grid(row=0, column=2, padx=(0, 10), sticky="nsew")

                amount_label = CTkLabel(master=row_frame, text=f"{amount}", font=("Helvetica", 15))
                amount_label.grid(row=0, column=3, padx=(0, 10), sticky="e")

                for col in range(7):  # Adjust according to the number of columns
                    row_frame.grid_columnconfigure(col, minsize=260)


    except Exception as e:
        print(f"Error: {e}")


def close_position(id, username, password, app, nav_frame, client_functions):
    response = messagebox.askyesno("Close Postion", "Are you sure you want to close?")
    if response:
        response = client_functions["close_position"](username, password, id)
        messagebox.showinfo("Close Position", response)
    else:
        messagebox.showerror("Close Position", response)
    view_holdings(app, client_functions, username, password, nav_frame)


def account_details(app, client_functions, username, password, nav_frame):
    if app.winfo_children():    
        for widget in app.winfo_children():
            if widget != nav_frame:
                widget.destroy()
    response = client_functions["view_account"](username, password)
    try:   
        user_name, password, balance = response[0][1], response[0][2], response[0][3]
    except:
        messagebox.showerror("Error", f"{response}")
    
    page_title = CTkLabel(master=app, text="Account Details", font=("Helvetica", 45))
    page_title.place(relx=0.5, rely=0.15, anchor="center")

    username_label = CTkLabel(master=app, text=f"Username: {user_name}", font=("Helvetica", 30))
    username_label.place(relx=0.2, rely=0.3, anchor="center")

    balance = CTkLabel(master=app, text=f"Balance: {balance:.2f}", font=("Helvetica", 30))
    balance.place(relx=0.75, rely=0.3, anchor="center")

    withdraw_label = CTkLabel(master=app, text="Withdraw", font=("Helvetica", 25))
    withdraw_label.place(relx=0.25, rely=0.5, anchor="center")

    deposit_label = CTkLabel(master=app, text="Deposit", font=("Helvetica", 25))
    deposit_label.place(relx=0.75, rely=0.5, anchor="center")

    withdraw_amount_entry = CTkEntry(master=app, )
    withdraw_amount_entry.place(relx=0.25, rely=0.6, anchor="center")

    deposit_amount_entry = CTkEntry(master=app, )
    deposit_amount_entry.place(relx=0.75, rely=0.6, anchor="center")

    withdraw_button = CTkButton(master=app, text="Withdraw", font=("Helvetica", 20), command=lambda : deposit_withdraw(user_name, password, "withdraw", client_functions, app, nav_frame, withdraw_amount_entry.get()))
    withdraw_button.place(relx=0.25, rely=0.7, anchor="center")

    deposit_button = CTkButton(master=app, text="Deposit", font=("Helvetica", 20), command=lambda : deposit_withdraw(user_name, password, 'deposit', client_functions, app, nav_frame, deposit_amount_entry.get()))
    deposit_button.place(relx=0.75, rely=0.7, anchor="center")


def deposit_withdraw(username, password, action, client_functions, app, nav_frame, amount=0):
    response = messagebox.askyesno(f"{action}", f"Do you want to {action} {amount}")
    if response:
        if action.lower() == "withdraw":
            response = client_functions["withdraw_funds"](username, password, amount)
        elif action.lower() == "deposit":
            response = client_functions["deposit_funds"](username, password, amount)
        messagebox.showinfo("Transaction", response)
    else:
        messagebox.showerror("Transaction", "Transaction failed please try again later.")
    account_details(app, client_functions, username, password, nav_frame)
    

def logout(app, client_functions, username, password, nav_frame):
    logout = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if logout:
        client_functions['logout']
        app.quit()
        app.destroy()

    else: 
        home_page(username, password, app, client_functions, nav_frame)