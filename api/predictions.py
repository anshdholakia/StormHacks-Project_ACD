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
    t = hist.copy() #making a copy
    for i in range(no_of_days):
        hist.loc[dti[i+1]] = [hist['Close'].mean(axis = 0), hist['HL_PCT'].mean(axis = 0), hist['PCT_change'].mean(axis = 0), hist['Volume'].mean(axis = 0)]

    hist['label'] = hist[forecast_col].shift(-no_of_days) # Making the label attribute for values to be predicted
    hist.dropna(inplace=True)
    X = np.array(hist.drop(['label'], 1))
    y = np.array(hist['label'])
    X = preprocessing.scale(X)
    y=np.array(hist['label'])

    X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.2)
    clf = LinearRegression()
    clf.fit(X_train, y_train)
    accurate = clf.score(X_test, y_test)
    print(accurate) # Accuracy averages around 79.9%



    
    



    # print(hist)
    # hist['Close'].plot(figsize=(16, 9))
    # plt.show()

    # for i in data.__dict__:
    #     print(i,"=>", getattr(data, i),"\n\n")

if __name__ == '__main__':
    predictions('MSFT')
