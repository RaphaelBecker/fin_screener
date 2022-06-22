import os
import pathlib
from typing import Optional, Dict

import pandas_datareader as pdr
import pandas as pd
import datetime
# DB Management
import sqlalchemy as sqlalchemy
from pandas_datareader._utils import RemoteDataError

db_name = 'HLOCV.db'
root_dir0 = pathlib.Path(__file__).resolve().parents[0]
db_path = 'sqlite:///' + str(pathlib.Path.joinpath(root_dir0, db_name))

engine = sqlalchemy.create_engine(db_path, echo=True, connect_args={"check_same_thread": False})
db_hlocv_sqlite_connection = engine.connect()


def create_upsert_method(meta: sqlalchemy.MetaData, extra_update_fields: Optional[Dict[str, str]]):
    """
    Create upsert method that satisfied the pandas's to_sql API.
    """

    def method(table, conn, keys, data_iter):
        # select table that data is being inserted to (from pandas's context)
        sql_table = sqlalchemy.Table(table.name, meta, autoload=True)

        # list of dictionaries {col_name: value} of data to insert
        values_to_insert = [dict(zip(keys, data)) for data in data_iter]

        # create insert statement using postgresql dialect.
        # For other dialects, please refer to https://docs.sqlalchemy.org/en/14/dialects/
        insert_stmt = sqlalchemy.dialects.postgresql.insert(sql_table, values_to_insert)

        # create update statement for excluded fields on conflict
        update_stmt = {exc_k.key: exc_k for exc_k in insert_stmt.excluded}
        if extra_update_fields:
            update_stmt.update(extra_update_fields)

        # create upsert statement.
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=sql_table.primary_key.columns,  # index elements are primary keys of a table
            set_=update_stmt  # the SET part of an INSERT statement
        )

        # execute upsert statement
        conn.execute(upsert_stmt)

    return method


def upsert(ticker, pair, timeframe, market, df_ticker):
    # create DB metadata object that can access table names, primary keys, etc.
    meta = sqlalchemy.MetaData(engine)

    # dictionary which will add additional changes on update statement. I.e. all the columns which are not present in DataFrame,
    # but needed to be updated regardless. The common example is `updated_at`. This column can be updated right on SQL server, instead of in pandas DataFrame
    extra_update_fields = {"updated_at": "NOW()"}

    # create upsert method that is accepted by pandas API
    upsert_method = create_upsert_method(meta, extra_update_fields)

    # perform upsert of df DataFrame values to a table `table_name` and Postgres connection defined at `db_engine`
    hlocv_table_name = ticker + "," + pair + "," + timeframe + "," + market
    df_ticker.to_sql(
        hlocv_table_name,
        engine,
        schema="db_schema",
        index=False,
        if_exists="append",
        chunksize=200,  # it's recommended to insert data in chunks
        method=upsert_method
    )


def close_db_connection():
    db_hlocv_sqlite_connection.close()


def download_ticker_df(ticker, pair='USD', timeframe='1d', market='yahoo'):
    df_ticker = pdr.DataReader(ticker, market, '2010-01-01', datetime.datetime.now().date(), retry_count=3, pause=.3)
    return df_ticker


# DB  Functions
def add_hlocv_table(df_ticker, ticker, pair='USD', timeframe='1d', market='yahoo', if_exists='replace'):
    hlocv_table_name = ticker + "," + pair + "," + timeframe + "," + market
    df_ticker.to_sql(hlocv_table_name, db_hlocv_sqlite_connection, if_exists=if_exists)


def get_hlocv_from_db(ticker, pair, timeframe, market):
    # TODO: implement from_datetime to_datetime. Idea:
    # SELECT  *
    # FROM    "FB,USD,1d,yahoo"
    # WHERE   date BETWEEN '2013-07-25 00:00:00.000000' AND '2021-06-18 00:00:00.000000'
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


def snapshot(ticker_list, progress_bar, pair='USD', timeframe='1d', market='yahoo'):
    failed_ticker_list = []
    for i, ticker in enumerate(ticker_list):
        try:
            df_ticker = download_ticker_df(ticker, pair=pair, timeframe=timeframe, market=market)
            add_hlocv_table(df_ticker, ticker, pair, timeframe, market)
        except (RemoteDataError, KeyError):
            failed_ticker_list.append(ticker)
            pass
        progress_bar.progress(i-1 + 1)
    close_db_connection()
    return failed_ticker_list


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


def get_ticker_list():
    ticker_dict_list = view_all_tickers()
    ticker_list = []
    for ticker_dict in ticker_dict_list:
        ticker_list.append(ticker_dict["ticker"])
    return ticker_list
