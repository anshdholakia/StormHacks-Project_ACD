from cmath import nan
import json
import datetime
import yfinance as yf
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import math
import numpy as np
import json

# get historical market data
def predictions(hist):
    style.use('ggplot')

    # JSON file for company information
    # print(obj1.info)

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
        hist.loc[dti[i+1]] = [hist['Close'].mean(axis = 0), hist['HL_PCT'].mean(axis = 0), hist['PCT_change'].mean(axis = 0), hist['Volume'].mean(axis = 0)]

    hist['label'] = hist[forecast_col].copy().shift(-no_of_days) # Making the label attribute for values to be predicted
    X = np.array(hist.drop(['label'], 1))
    X = X[:-no_of_days]
    X_lately = X[-no_of_days:]

    hist.dropna(inplace=True)
    y = np.array(hist['label'])

    X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.2)
    clf = LinearRegression(n_jobs=-1)
    clf.fit(X_train, y_train)
    # accurate = clf.score(X_test, y_test)
    # print(accurate) # Accuracy averages around 79.9%

    predictions = clf.predict(X_lately)

    hist['Forecast'] = np.nan
    start_date = hist.head(1).index.item()
    last_date = hist.tail(1).index.item()

    dtti = pd.date_range(start_date, periods=len(hist)-no_of_days, freq="D")
    dti = pd.date_range(last_date, periods=no_of_days+1, freq="D")
    k=0
    for i in dtti:
        hist.loc[i] = [np.nan for _ in range(len(hist.columns) - 1)] + [np.array(hist['Close'])[k]]
        k+=1

    for i,j in zip(range(no_of_days),predictions):
        hist.loc[dti[i+1]] = [np.nan for _ in range(len(hist.columns) - 1)] + [j]

    hist = hist.drop(['Close', 'HL_PCT', 'PCT_change', 'Volume', 'label'], 1)
    
    return hist #the last 30 are the predictions by the model

if __name__ == '__main__':
    print(yf.Ticker('MSFT').history("2y"))
