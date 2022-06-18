import datetime
import unittest
import pandas_datareader as pdr
import data.db_connector as db_connector

ticker = 'FB'
pair = 'USD'
timeframe = '1d'


class TestDbConnector(unittest.TestCase):

    def test_basics(self):
        df_ticker = db_connector.download_ticker_df(ticker, pair, timeframe)
        print(df_ticker)
        print(db_connector.root_dir0)

    def test_add_hlocv_table(self):
        db_connector.add_hlocv_table(ticker, pair, timeframe)

    def test_snapshot(self):
        ticker_list = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT']
        db_connector.snapshot(ticker_list)

    def test_view_all_tickers(self):
        ticker_list = db_connector.view_all_tickers()
        print(ticker_list)
        print('')

    def test_get_hlocv_from_db(self):
        ticker_dict_list = db_connector.view_all_tickers()
        for ticker_dict in ticker_dict_list:
            df_ticker = db_connector.get_hlocv_from_db(ticker_dict['ticker'], ticker_dict['pair'],
                                                       ticker_dict['timeframe'], ticker_dict['market'])
            print(df_ticker)


