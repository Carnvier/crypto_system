import trading_data as td
import time

class Asset():
     
    def get_values(self):
        assets = {
            "Bitcoin" : td.closing_price("BTC-USD"),
            "Ethereum" : td.closing_price("ETH-USD"),
            "Gold": td.closing_price("GC=F"),
            "Silver": td.closing_price("SI=F"),
            "EURUSD": td.closing_price("EURUSD=X"),
            }
        return assets      




