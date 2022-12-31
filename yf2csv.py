import yfinance as yf
import os


def get_info_on_stock(path, portfolio, start, end, interval):
    for ticker in portfolio:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start, end=end, interval=interval)
        hist.to_csv(os.path.join(path, f"{ticker}_hist.csv"))
