import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time  # Import time to use sleep

def closing_price(symbol):
    # Fetch current closing price
    try:
        current_price = yf.Ticker(symbol).history(period='1d')['Close'].iloc[0]
        return current_price
    except:
        print(f"Failed to fetch current price for {symbol}")
        return 'Market closed'
    
# Define the stock symbol and the date range
# symbol = 'BTC=X'  # EUR/USD currency pair
# end_date = datetime.now()  # Current date
# start_date = end_date - timedelta(days=30)  # Last 30 days

# # Fetch historical data for the last 30 days
# historical_data = yf.Ticker(symbol).history(start=start_date, end=end_date)

# # Print the historical data
# print(historical_data)




# while True:
#     stock = yf.Ticker(symbol)
#     historical_data = stock.history(period='1d')
    
#     closing_prices = historical_data["Close"]
#     current_price = closing_prices.iloc[-1]  # Get the last closing price
#     current_time = historical_data.index[-1]  # Get the last date from the index
#     with open('eurusd.transactions', 'a+') as f:
#         f.writelines(f'{datetime.now()} {current_price}\n')    
#     print(f"Current Price: {current_price} at {current_time}")
    
#     time.sleep(20) 

# # Fetch historical data using yfinance
# ohlc = yf.download(symbol, start=start_date, end=end_date, interval='2m')  # 2-minute interval

# # Display the data
# print(ohlc)

# for i, v in ohlc.items():
#     print(i, v)

# Flatten the column names
# ohlc.columns = ohlc.columns.map(lambda x: x[1] if isinstance(x, tuple) else x)

# # Reset index to have datetime as a column
# ohlc.reset_index(inplace=True)

# # Plotting the closing prices
# fig = px.line(ohlc, x='Datetime', y='Close', title=f'{symbol} Closing Prices (Last 30 Days)')
# fig.show()