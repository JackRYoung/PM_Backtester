# PM Backtester 1.0
# Jack Young

from yf2csv import *
from strategy import *

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from math import *

path = r'C:\Users\jacky\OneDrive\Documents\GitHub\PM_Backtester\data'
counter = -1


# Initializes sizes of vectors, csv files, etc, this function is kind of
# fragile right now
def init():
    # for now, we are restrained in the sense that all assets must
    # have the exact same length of data
    # unfortunately this means cryptocurrencies cannot be in the
    # portfolio while regular stocks are, I will work on this for version 1.1
    portfolio = ['SPY', 'TSLA', 'AAPL', 'AMD', 'AMZN']
    get_info_on_stock(path, portfolio, '2021-01-01', '2022-01-01', '1d')

    length = len(pd.read_csv(os.path.join(path, portfolio[0]+"_hist.csv")))
    arr = np.ndarray((len(portfolio), length, 7))
    dates = []

    idx = 0
    for ticker in portfolio:
        # print(f"{ticker}")
        df = pd.read_csv(os.path.join(path, f"{ticker}_hist.csv"))
        arr[idx, :, :] = df.loc[0:length, 'Open':'Stock Splits'].to_numpy()
        dates = df.Date.to_list()
        idx += 1
    return dates, arr, length


# Returns the next time-slice of data
#   If an error was thrown due to failure to execute orders,
#   the counter is not updated and the same data is returned.
def next_data(dates, arr, error):
    global counter
    if (error):
        return dates[counter], arr[:, counter, :]
    else:
        counter += 1
        return dates[counter], arr[:, counter, :]


# Updates portfolio and capital according to executed orders
def update_portfolio(portfolio, portfolio_delta, capital, capital_delta):
    return portfolio+portfolio_delta, capital+capital_delta


# TODO: Executes orders at prices found in the data, and returns change in
#   portfolio and capital as a result. Returns any orders which did not execute
#   yet due to the limit price.
def execute_orders(data, orders, capital):
    #   For now, just use one of the open or close values as the 'true price'
    #   at which orders are executed
    # Since we do not have access to live data, we may in the future approximate
    # the 'true price' with a gaussian centered between the high and low with a
    # standard deviation derived from other data

    outstanding_orders = []
    capital_delta = 0
    portfolio_delta = [0, 0, 0, 0, 0]
    if capital+capital_delta < 0:
        raise Exception("Insufficient Funds")
    return outstanding_orders, portfolio_delta, capital_delta


# Main loop, feeds data to strategy, tries to execute specified orders then
# returns the results back to the strategy. Repeats for all available data
if __name__ == '__main__':
    dates, arr, length = init()
    portfolio = [0, 0, 0, 0, 0]  # Init porfolio is 0 of every asset
    capital = 5e4  # Init capital is 50k
    orders = None  # No orders before any data is recieved

    error = False
    for i in range(0, length):
        date, data = next_data(dates, arr, error)
        orders = strategy(date, data, portfolio, capital, orders, error)
        error = False
        try:
            outstanding_orders, delta_p, delta_c = execute_orders(
                data, orders, capital)
            portfolio, capital, = update_portfolio(
                portfolio, delta_p, capital, delta_c)
            orders = outstanding_orders
        except Exception("Insufficient Funds"):
            i -= 1
            error = True
