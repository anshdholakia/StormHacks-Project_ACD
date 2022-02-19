from cmath import nan
import yfinance as yf
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np


def predictions(ticker):

    obj1 = yf.Ticker(ticker)

    # JSON file for company information
    # print(obj1.info)

    # get historical market data
    hist = obj1.history(period="2y")
    hist = hist[['Open','High', 'Low', 'Close','Volume', 'Dividends','Stock Splits']]
    hist['HL_PCT'] = (hist['High']-hist['Close'])/hist['Close'] * 100.0 # high-low percentage
    hist['PCT_change'] = (hist['Close'] - hist['Open']) / hist['Open'] * 100.0 # Percentage change
    hist = hist[['Close','HL_PCT','PCT_change','Volume']]
    forecast_col = 'Close' # We are going to forecast the closing values
    hist.fillna(-9999,inplace = True)

    no_of_days = 30 # days we want to predict

    last_date = hist.tail(1).index.item()

    dti = pd.date_range(last_date, periods=no_of_days+1, freq="D")
 
    for i in range(no_of_days):
        hist.loc[dti[i+1]] = [nan, nan, nan, nan] 

    hist['label'] = hist[forecast_col].shift(-no_of_days) # Making the label attribute for values to be predicted
    # print(hist['label'])
    # hist.dropna(inplace = True)
    # X = np.array(hist.drop(['label'], 1))
    # y = np.array(hist['label'])
    # X = preprocessing.scale(X)
    
    



    # print(hist)
    # hist['Close'].plot(figsize=(16, 9))
    # plt.show()

    # for i in data.__dict__:
    #     print(i,"=>", getattr(data, i),"\n\n")

if __name__ == '__main__':
    predictions('MSFT')
