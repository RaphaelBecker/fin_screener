import pandas_datareader as pdr
import datetime
# DB Management
import sqlite3
conn = sqlite3.connect('ohcl.db')
ohcl_database = conn.cursor()


# DB  Functions
def create_ohcl_table():
    ohcl_database.execute('CREATE TABLE IF NOT EXISTS ohlc(ticker,timeframe)')


def add_ohcl(ticker, timeframe):
    ohcl_database.execute('INSERT INTO ohlc(ticker,timeframe) VALUES (?,?)', (ticker, timeframe))
    conn.commit()


def get_ohlc(ticker, timeframe):
    ohcl_database.execute('SELECT * FROM ohlc WHERE ticker =? AND timeframe =?', (ticker, timeframe))
    data = ohcl_database.fetchall()
    return data


def view_all_tickers():
    ohcl_database.execute('SELECT * FROM ohlc')
    data = ohcl_database.fetchall()
    return data


tickers = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT']

for ticker in tickers:
    df_ticker = pdr.DataReader(ticker, 'yahoo', '2011-08-01', datetime.datetime.now().date())