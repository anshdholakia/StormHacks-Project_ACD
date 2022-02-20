from flask import Flask
from flask import request 
from flask import jsonify
from flask_cors import CORS

import json
import yfinance as yf
import pandas as pd
from get_stats import get_stats
from predictions import predictions

import requests as req

app = Flask(__name__)
CORS(app)


def try_get_data(ticker: str):
    df = pd.DataFrame()

    if ticker == None:
        return df 

    ticker = yf.Ticker(ticker)

    if ticker.info['regularMarketPrice'] == None:
        return df 
    else:
        df = ticker.history(period='2y')
        return df


def get_stats_wrapper(stock_data):
    return get_stats(stock_data)


def get_predictions_wrapper(stock_data):
    return predictions(stock_data)


def make_response(stats, preds):
    stats_json = stats.to_json(date_format='epoch')
    preds_json = preds.to_json(date_format='epoch')
    response = {'stats': json.loads(stats_json), 'preds': json.loads(preds_json)}
    return response


@app.route('/analyze', methods=['GET'])
def analyze():
    ticker = request.args.get('ticker')

    stock_data = try_get_data(ticker)

    if stock_data.empty:
        return 'stock does not exist!'

    predictions = get_predictions_wrapper(stock_data) # ansh's module
    stats = get_stats_wrapper(stock_data) # chau's module

    response = make_response(stats, predictions)
    return jsonify(response)


@app.route('/description', methods=['GET'])
def description():
    ticker = request.args.get('ticker')
    data = yf.Ticker(ticker)
    return jsonify(data.info)
