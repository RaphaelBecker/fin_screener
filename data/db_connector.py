import os
import pathlib

import pandas_datareader as pdr
import pandas as pd
import datetime
# DB Management
from sqlalchemy import create_engine

db_name = 'HLOCV.db'
root_dir0 = pathlib.Path(__file__).resolve().parents[0]
db_path = 'sqlite:///' + str(pathlib.Path.joinpath(root_dir0, db_name))

engine = create_engine(db_path, echo=True)
db_hlocv_sqlite_connection = engine.connect()


def close_db_connection():
    db_hlocv_sqlite_connection.close()


def download_ticker_df(ticker, pair='USD', timeframe='1d', market='yahoo'):
    df_ticker = pdr.DataReader(ticker, market, '2010-01-01', datetime.datetime.now().date(), retry_count=3, pause=.3)
    return df_ticker


# DB  Functions
def add_hlocv_table(df_ticker, ticker, pair='USD', timeframe='1d', market='yahoo', if_exists='append'):
    hlocv_table_name = ticker + "," + pair + "," + timeframe + "," + market
    df_ticker.to_sql(hlocv_table_name, db_hlocv_sqlite_connection, if_exists=if_exists)


def get_hlocv_from_db(ticker, pair, timeframe, market):
    hlocv_table_name = str(ticker + "," + pair + "," + timeframe + "," + market)
    sqlite_query_string = f"SELECT * FROM '{hlocv_table_name}'"
    df_ticker = pd.read_sql(
        sqlite_query_string,
        con=db_hlocv_sqlite_connection,
        parse_dates=[
            'created_at',
            'updated_at'
        ]
    )
    return df_ticker


def snapshot(ticker_list, pair='USD', timeframe='1d', market='yahoo'):
    for ticker in ticker_list:
        df_ticker = download_ticker_df(ticker, pair=pair, timeframe=timeframe, market=market)
        add_hlocv_table(df_ticker, ticker, pair, timeframe, market)
    close_db_connection()


def view_all_tickers():
    """
    :return: ticker_dict_list = {ticker, pair, timeframe, market}
    """
    sqlite_query_string = f"SELECT name FROM sqlite_master WHERE type ='table'"
    result_proxy = db_hlocv_sqlite_connection.execute(sqlite_query_string)
    ticker_dict_list = []
    sqlite_legacy_rows = result_proxy.fetchall()
    for sqlite_legacy_row in sqlite_legacy_rows:
        try:
            ticker_dict_screwd = dict(sqlite_legacy_row)
            ticker, pair, timeframe, market = ticker_dict_screwd["name"].split(',')
            ticker_dict_list.append({'ticker': ticker, 'pair': pair, 'timeframe': timeframe, 'market': market})
        except ValueError:
            pass
    return ticker_dict_list
