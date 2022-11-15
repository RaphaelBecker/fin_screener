import pathlib
import yahoo_fin.stock_info as si
import yfinance as yf

import pandas_datareader as pdr
import pandas as pd
import datetime
# DB Management
import sqlalchemy as sqlalchemy
from pandas_datareader._utils import RemoteDataError

db_name = 'HLOCV.db'
root_dir0 = pathlib.Path(__file__).resolve().parents[0]
db_path = 'sqlite:///' + str(pathlib.Path.joinpath(root_dir0, db_name))

engine = sqlalchemy.create_engine(db_path, echo=True, connect_args={"check_same_thread": False, 'timeout': 5})
db_hlocv_sqlite_connection = engine.connect()


def close_db_connection():
    db_hlocv_sqlite_connection.close()


def get_dow_ticker_list():
    return si.tickers_dow()


def get_smp500_ticker_list():
    return si.tickers_sp500()


def get_nasdaq_ticker_list():
    return si.tickers_nasdaq()


def get_others_ticker_list():
    return si.tickers_other()


def get_fundamental_quote(ticker: str) -> dict:
    df = si.get_quote_table(ticker, dict_result=False).transpose()
    header_row = df.iloc[0]
    df2 = pd.DataFrame(df.values[1:], columns=header_row)
    return df2


def get_fundamental_stats_valuation(ticker):
    df = si.get_stats_valuation(ticker).transpose()
    header_row = df.iloc[0]
    df2 = pd.DataFrame(df.values[1:], columns=header_row)
    return df2


def get_ticker_info(ticker):
    """
    {'zip': '95014', 'sector': 'Technology', 'fullTimeEmployees': 164000, 'longBusinessSummary': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related services. In addition, the company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. Further, it provides AppleCare support and cloud services store services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. Additionally, the company offers various services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was incorporated in 1977 and is headquartered in Cupertino, California.', 'city': 'Cupertino', 'phone': '408 996 1010', 'state': 'CA', 'country': 'United States', 'companyOfficers': [], 'website': 'https://www.apple.com', 'maxAge': 1, 'address1': 'One Apple Park Way', 'industry': 'Consumer Electronics', 'ebitdaMargins': 0.33105, 'profitMargins': 0.2531, 'grossMargins': 0.43310001, 'operatingCashflow': 122151002112, 'revenueGrowth': 0.081, 'operatingMargins': 0.30289, 'ebitda': 130541002752, 'targetLowPrice': 122, 'recommendationKey': 'buy', 'grossProfits': 170782000000, 'freeCashflow': 90215251968, 'targetMedianPrice': 178.5, 'currentPrice': 149.275, 'earningsGrowth': 0.048, 'currentRatio': 0.879, 'returnOnAssets': 0.21214001, 'numberOfAnalystOpinions': 40, 'targetMeanPrice': 177.61, 'debtToEquity': 261.446, 'returnOnEquity': 1.75459, 'targetHighPrice': 214, 'totalCash': 48304001024, 'totalDebt': 132480000000, 'totalRevenue': 394328014848, 'totalCashPerShare': 3.036, 'financialCurrency': 'USD', 'revenuePerShare': 24.317, 'quickRatio': 0.709, 'recommendationMean': 1.9, 'exchange': 'NMS', 'shortName': 'Apple Inc.', 'longName': 'Apple Inc.', 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EST', 'isEsgPopulated': False, 'gmtOffSetMilliseconds': '-18000000', 'quoteType': 'EQUITY', 'symbol': 'AAPL', 'messageBoardId': 'finmb_24937', 'market': 'us_market', 'annualHoldingsTurnover': None, 'enterpriseToRevenue': 6.253, 'beta3Year': None, 'enterpriseToEbitda': 18.888, '52WeekChange': -0.0019999743, 'morningStarRiskRating': None, 'forwardEps': 6.81, 'revenueQuarterlyGrowth': None, 'sharesOutstanding': 15908100096, 'fundInceptionDate': None, 'annualReportExpenseRatio': None, 'totalAssets': None, 'bookValue': 3.178, 'sharesShort': 103178670, 'sharesPercentSharesOut': 0.0064999997, 'fundFamily': None, 'lastFiscalYearEnd': 1663977600, 'heldPercentInstitutions': 0.60247004, 'netIncomeToCommon': 99802996736, 'trailingEps': 6.11, 'lastDividendValue': 0.23, 'SandP52WeekChange': -0.14731997, 'priceToBook': 46.971363, 'heldPercentInsiders': 0.00072999997, 'nextFiscalYearEnd': 1727136000, 'yield': None, 'mostRecentQuarter': 1663977600, 'shortRatio': 1.14, 'sharesShortPreviousMonthDate': 1664496000, 'floatShares': 15891414476, 'beta': 1.246644, 'enterpriseValue': 2465621344256, 'priceHint': 2, 'threeYearAverageReturn': None, 'lastSplitDate': 1598832000, 'lastSplitFactor': '4:1', 'legalType': None, 'lastDividendDate': 1667520000, 'morningStarOverallRating': None, 'earningsQuarterlyGrowth': 0.008, 'priceToSalesTrailing12Months': 6.0220966, 'dateShortInterest': 1667174400, 'pegRatio': 2.69, 'ytdReturn': None, 'forwardPE': 21.91997, 'lastCapGain': None, 'shortPercentOfFloat': 0.0064999997, 'sharesShortPriorMonth': 103251184, 'impliedSharesOutstanding': 0, 'category': None, 'fiveYearAverageReturn': None, 'previousClose': 149.7, 'regularMarketOpen': 148.97, 'twoHundredDayAverage': 155.6808, 'trailingAnnualDividendYield': 0.006012024, 'payoutRatio': 0.14729999, 'volume24Hr': None, 'regularMarketDayHigh': 150.28, 'navPrice': None, 'averageDailyVolume10Day': 97152100, 'regularMarketPreviousClose': 149.7, 'fiftyDayAverage': 147.6636, 'trailingAnnualDividendRate': 0.9, 'open': 148.97, 'toCurrency': None, 'averageVolume10days': 97152100, 'expireDate': None, 'algorithm': None, 'dividendRate': 0.92, 'exDividendDate': 1667520000, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': 147.43, 'currency': 'USD', 'trailingPE': 24.43126, 'regularMarketVolume': 51750694, 'lastMarket': None, 'maxSupply': None, 'openInterest': None, 'marketCap': 2374681493504, 'volumeAllCurrencies': None, 'strikePrice': None, 'averageVolume': 88992084, 'dayLow': 147.43, 'ask': 149.66, 'askSize': 1100, 'volume': 51750694, 'fiftyTwoWeekHigh': 182.94, 'fromCurrency': None, 'fiveYearAvgDividendYield': 1, 'fiftyTwoWeekLow': 129.04, 'bid': 149.64, 'tradeable': False, 'dividendYield': 0.0061000003, 'bidSize': 1300, 'dayHigh': 150.28, 'coinMarketCapLink': None, 'regularMarketPrice': 149.275, 'preMarketPrice': 149.06, 'logo_url': 'https://logo.clearbit.com/apple.com'}
    """
    df = pd.DataFrame([yf.Ticker(ticker).info])
    return df


def download_ticker_df(ticker, pair='USD', timeframe='1d', market='yahoo'):
    df_ticker = pdr.DataReader(ticker, market, '2010-01-01', datetime.datetime.now().date(), retry_count=3, pause=.3)
    # make all column names lower case:
    df_ticker.columns = map(str.lower, df_ticker.columns)
    return df_ticker


# DB  Functions
def add_hlocv_table(df_ticker, ticker, pair='USD', timeframe='1d', market='yahoo', if_exists='replace'):
    hlocv_table_name = ticker + "," + pair + "," + timeframe + "," + market
    df_ticker.to_sql(hlocv_table_name, db_hlocv_sqlite_connection, if_exists=if_exists)


def get_hlocv_from_db(ticker, from_date, to_date, timeframe='1d', pair='USD', market='yahoo'):
    # TODO: implement from_datetime to_datetime. Idea:
    # SELECT  *
    # FROM    "FB,USD,1d,yahoo"
    # WHERE   date BETWEEN '2013-07-25 00:00:00.000000' AND '2021-06-18 00:00:00.000000'
    hlocv_table_name = str(ticker + "," + pair + "," + timeframe + "," + market)
    # format: 2014-07-25 00:00:00.000000
    # fmt = '%Y-%m-%d %H:%M:%S.%s'
    sqlite_query_string = f"SELECT * FROM '{hlocv_table_name}' WHERE date BETWEEN '{from_date}' AND '{to_date}'"
    df_ticker = pd.read_sql(
        sqlite_query_string,
        con=db_hlocv_sqlite_connection,
        parse_dates=[
            'created_at',
            'updated_at'
        ]
    )
    # cast date index to datetimeindex as all computation is based on that!:
    datetime_series = pd.to_datetime(df_ticker['Date'])
    # create datetime index passing the datetime series
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    df_buffer = df_ticker.set_index(datetime_index)
    df_buffer.drop('Date', axis=1, inplace=True)
    # make all column names lower case:
    df_buffer.columns = map(str.lower, df_buffer.columns)
    return df_buffer


def snapshot(ticker_list, progress_bar, pair='USD', timeframe='1d', market='yahoo'):
    failed_ticker_list = []
    success_ticker_list = []
    progressbar_range = len(ticker_list)
    for i, ticker in enumerate(ticker_list):
        try:
            df_ticker = download_ticker_df(ticker, pair=pair, timeframe=timeframe, market=market)
            add_hlocv_table(df_ticker, ticker, pair, timeframe, market)
            success_ticker_list.append(ticker)
        except (RemoteDataError, KeyError):
            failed_ticker_list.append(ticker)
            pass
        # start progressbar with 1 to indicate the user the process started
        progress = max((int((i / progressbar_range) * 100) - 1), 0)
        progress_bar.progress(2 + progress)
    return success_ticker_list, failed_ticker_list


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
