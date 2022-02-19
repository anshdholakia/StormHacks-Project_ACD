import yfinance as yf
import sklearn
import pandas as pd
import matplotlib.pyplot as plt

data = yf.Ticker('GOOGL')
for i in data.__dict__:
    print(i,"=>", getattr(data, i),"\n\n")