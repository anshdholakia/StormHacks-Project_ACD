import yfinance as yf
import sklearn
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    ticker = 'MSFT'
    obj1 = yf.Ticker(ticker)

    # JSON file for company information
    # print(obj1.info)

    # get historical market data
    hist = obj1.history(period="1y")
    hist = hist[['Open','High', 'Low', 'Close','Volume', 'Dividends','Stock Splits']]
    hist['HL_PCT'] = (hist['High']-hist['Close'])/hist['Close'] * 100.0 # high-low percentage
    hist['PCT_change'] = (hist['Close'] - hist['Open']) / hist['Open'] * 100.0 # Percentage change
    hist = hist[['Close','HL_PCT','PCT_change','Volume']]
    hist.fillna(-9999,inplace = True)




    # print(hist)
    # hist['Close'].plot(figsize=(16, 9))
    # plt.show()

    # for i in data.__dict__:
    #     print(i,"=>", getattr(data, i),"\n\n")