from flask import Flask
from flask import request 

app = Flask(__name__)


def ticker_exists(ticker: str) -> bool:
    # Not yet implemented, assume true for now
    return True


def get_stock_data(ticker: str):
    # Not yet implemented
    return {}


def get_stats(stock_data):
    # Not yet implemented, Chau's module
    return {}


def get_predictions(stock_data):
    # Not yet implemented, Ansh's module
    return {}


@app.route("/analyze", methods=["GET"])
def analyze():
    ticker = request.args.get("ticker")

    if not ticker_exists(ticker):
        # If invalid ticker, return empty data. To be parsed on the front end.
        return data

    stock_data = get_stock_data(ticker)
    stats = get_stats(stock_data) # chau's module
    predictions = get_predictions(stock_data) # ansh's module

    return {
            "stats": stats,
            "predictions": predictions
            }
