import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time  # Import time to use sleep

def closing_price(symbol):
    '''Fetch current closing price'''
    try:
        current_price = yf.Ticker(symbol).history(period='1d')['Close'].iloc[0]
        return current_price
    except:
        print(f"Failed to fetch current price for {symbol}")
        return 'Market closed'
    
def asset_price_history(asset):
    '''Fetch historical data for the last 3 days with a 30-minute interval '''
    try:
        start_date = datetime.now() - timedelta(days=3)
        historical_data = yf.Ticker(asset).history(start=start_date, end=datetime.now(), interval='30m')
        
        # Format the index to a specific string format (e.g., 'YYYY-MM-DD HH:MM')
        historical_data.index = historical_data.index.strftime('%d %H:%M')
        
        # Return only the date and closing price
        return historical_data[['Close']]
    except Exception as e:
        print(f'Failed to fetch historical data: {e}')
        return None


