import yfinance as yf
import pandas as pd 
import pandas_ta as ta
import json


def get_stats(stock_data):
    stock_data.ta.strategy(ta.CommonStrategy)
    return stock_data


# Testing
if __name__ == "__main__":
    data = yf.Ticker("MSFT")
    print(data.info)
    data_points = data.history(period="2y")[['Open', 'High', 'Low', 'Close', 'Volume']]
    data_json = get_stats(data_points)
    with open('test.json', 'w') as f:
        f.write(data_json.to_json(date_format='epoch'))
