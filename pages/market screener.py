import csv
import datetime
from dataclasses import dataclass

import pandas as pd
import streamlit as st
import talib
import re
import numpy as np
from data import dataset, helpers
from data import db_connector as database
from chart import chart_mpl
from utils import talib_functions
from indicators import heikin_ashi as heik_ash

fundamental_values = \
    [
        'P/E',
        'Forward P/E',
        'PEG',
        'P/S',
        'P/B',
        'Price/Cash',
        'Price/Free Cash Flow',
        'EPS growth',
        'Sales growth',
        'Return on Assets',
        'Return on Equity',
        'Return on Investment',
        'Current Ratio',
        'Quick Ratio',
        'LT Debt/Equity',
        'Debt/Equity',
        'Gross Margin',
        'Operating Margin',
        'Net Profit Margin',
        'Payout Ratio',
        'Insider Ownership',
        'Insider Transactions',
        'Institutional Ownership'
    ]


@dataclass
class Condition:
    price: str = None
    operator: str = None
    indicator1: str = None
    indicator1_args: list = None
    indicator2: str = None
    indicator2_args: list = None


if "words" not in st.session_state:
    st.session_state.words = []

# Set up sections of web page
st.set_page_config(layout="wide")
header = st.container()
screen_settings = st.container()
result_list = st.container()

st.sidebar.markdown("# Market Screener")
# select market
index_selector = st.sidebar.selectbox('Select index', sorted(dataset.market_index_list), index=0)
timeframe_selector_mock = st.sidebar.selectbox('Select timeframe', ["1d", "6h", "12h", "1d", "3d", "1w", "1m"], index=0)

# Set start and end point to fetch data:
start_date = st.sidebar.date_input('Start date', datetime.datetime(2021, 6, 1))
end_date = st.sidebar.date_input('End date', datetime.datetime.now().date())

# Update Database on sidebar:
database_update_progress_bar = st.sidebar.progress(0)
if st.sidebar.button('update OHLCV-database'):
    success_ticker_list, failed_ticker_list = database.snapshot(helpers.get_symbol_list('data/smp500_symbols.csv'),
                                                                database_update_progress_bar)
    st.sidebar.write(f"Success: {len(success_ticker_list)} / Failed: {len(failed_ticker_list)} "
                     f" Total: {len(success_ticker_list) + len(failed_ticker_list)}")
    database_update_progress_bar.success("Successfully updated database!")


def get_index_ticker_list(index_ticker_list):
    # Select ticker from chosen market:
    index_ticker_list = dataset.get_tickers(index_ticker_list)
    if isinstance(index_ticker_list, dict):
        index_ticker_list = index_ticker_list.keys()
    return index_ticker_list


def get_talib_functions_format_list(nested_dict):
    list_ = list(nested_dict.values())
    return list(map(lambda x: list(x.keys())[0], list_))

st.write('### Technicals')
col1, col2, col3, col4, col5, col6 = st.columns(6)

heikin_ashi = False
with col1:
    if st.checkbox("heikin ashi"):
        heikin_ashi = True

vol_support = False
with col2:
    if st.checkbox("close @ vol supp"):
        vol_support = True

bull_div = False
with col3:
    if st.checkbox("bull div"):
        bull_div = True

bullish_candle = False
with col4:
    if st.checkbox("bull last candle"):
        bullish_candle = True

tdi = False
with col5:
    if st.checkbox("TDI"):
        tdi = True

bb_contraction = False
with col6:
    if st.checkbox("BB squeeze"):
        bb_contraction = True

keyWords = st.text_input('Entry Strategy',
                         value='close<SMA(50) AND close>SMA(100) AND SMA(50)>SMA(100) AND SMA(100)>SMA(150) AND SMA(150)>SMA(200)')
keyWords = keyWords.strip()
if " AND " in keyWords:
    keyWords = keyWords.split(" AND ")
else:
    keyWords = [keyWords]


# QUERY PARSER:
## possible boolean operations in keys:
# price - oper - ind,
# price - oper - val,
# ind - oper - ind,
# ind - oper - val,
# ind - oper - bool

def check_format(entry_strategy_query_list, keywords):
    for query_list, query_string in zip(entry_strategy_query_list, keywords):
        if operator(query_list[0]):
            st.warning(
                f"Format error: '{query_string}' ignored!")
            st.write("Begin with price type ('close' or 'low' etc.) or indicator type ('ema(20)', cci(50)")
            keywords.remove(query_string)
            entry_strategy_query_list.remove(query_list)


def strategy_list(keywords):
    # parse logic
    entry_strategy_query_list = []
    i = 0
    for key in keywords:
        key = re.split('(<|>|=)', key)
        key = list(filter(None, key))
        key = list(map(lambda element: element.strip(), key))
        entry_strategy_query_list.append(key)
    return entry_strategy_query_list


# classification:
def price(key: str) -> bool:
    if key.lower() in ['high', 'low', 'close', 'open']:
        return True
    else:
        return False


def operator(key: str) -> bool:
    found = False
    for operator in ['<', '>', '=']:
        if key.find(operator) != -1:
            found = True
            break
    return found


def argument_list(key: str) -> bool:
    if '(' and ')' in key:
        return True
    else:
        return False


def indicator(key: str) -> bool:
    if not price(key):
        if not operator(key):
            return True
        else:
            return False


def parse_entry_query_to_condition_dataclass_list(entry_strategy_query_list):
    condition_list = []
    for entry_list in entry_strategy_query_list:
        condition = Condition()
        for item in entry_list:
            if price(item):
                condition.price = item
            if operator(item):
                condition.operator = item
            if indicator(item):
                if not condition.indicator1:
                    if "(" in item:
                        item = item.replace(")", "")
                        arguments = item.split("(")[1]
                        condition.indicator1 = item.split("(")[0]
                        if "," in arguments:
                            args_list = arguments.split(",")
                            condition.indicator1_args = list(map(lambda x: int(x), args_list))
                        else:
                            if arguments:
                                condition.indicator1_args = int(arguments)
                    else:  # no argument indicator
                        condition.indicator1 = item
                else:
                    if "(" in item:
                        item = item.replace(")", "")
                        arguments = item.split("(")[1]
                        condition.indicator2 = item.split("(")[0]
                        if "," in arguments:
                            args_list = arguments.split(",")
                            condition.indicator2_args = list(map(lambda x: int(x), args_list))
                        else:
                            if arguments:
                                condition.indicator2_args = int(arguments)
                    else:  # no argument indicator
                        condition.indicator2 = item
        condition_list.append(condition)
    return condition_list


def compute_talib_function(function_talib, func_args, hlocv_dataframe):
    function_col_name = function_talib
    if type(func_args) == list:
        for arg in func_args:
            function_col_name = function_col_name + "_" + str(arg)
    else:
        function_col_name = function_col_name + "_" + str(func_args)
    if function_col_name not in hlocv_dataframe.columns.values:
        talib_function = getattr(talib, function_talib)
        hlocv_dataframe[function_col_name] = np.nan
        try:
            if func_args:
                result = talib_function(hlocv_dataframe['close'], func_args)
            else:
                result = talib_function(hlocv_dataframe['close'])
            hlocv_dataframe[function_col_name] = result.to_frame().replace(0, np.nan).replace(100, 1)
        except IndexError as e:
            print(f"IndexError: {e}")
    return hlocv_dataframe, function_col_name


def price_indicator_comparison(condition, hlocv_dataframe):
    function_talib = condition.indicator1
    func_args = condition.indicator1_args
    hlocv_dataframe, function_col_name = compute_talib_function(function_talib, func_args, hlocv_dataframe)
    keep = False
    if condition.operator == "<":
        keep = float(hlocv_dataframe[condition.price].tail(1).values[0]) < float(
            hlocv_dataframe[function_col_name].tail(1).values[0])
        # st.write(f"{hlocv_dataframe[condition.price].tail(1).values[0]} < {hlocv_dataframe[function_col_name].tail(1).values[0]} -> {keep}")
    elif condition.operator == ">":
        keep = float(hlocv_dataframe[condition.price].tail(1).values[0]) > float(
            hlocv_dataframe[function_col_name].tail(1).values[0])
        # st.write(f"{hlocv_dataframe[condition.price].tail(1).values[0]} > {hlocv_dataframe[function_col_name].tail(1).values[0]} -> {keep}")

    return hlocv_dataframe, keep


def indicator1_indicator2_comparison(condition, hlocv_dataframe):
    function_talib1 = condition.indicator1
    func_args1 = condition.indicator1_args

    function_talib2 = condition.indicator2
    func_args2 = condition.indicator2_args

    hlocv_dataframe, function_col_name1 = compute_talib_function(function_talib1, func_args1, hlocv_dataframe)
    hlocv_dataframe, function_col_name2 = compute_talib_function(function_talib2, func_args2, hlocv_dataframe)

    keep = False
    if condition.operator == "<":
        keep = float(hlocv_dataframe[function_col_name1].tail(1).values[0]) < float(
            hlocv_dataframe[function_col_name2].tail(1).values[0])
    if condition.operator == ">":
        keep = float(hlocv_dataframe[function_col_name1].tail(1).values[0]) > float(
            hlocv_dataframe[function_col_name2].tail(1).values[0])

    return hlocv_dataframe, keep


def custom_indicator():
    pass


def get_ticker_condition_met(ticker, cond_dataclass_list, start_date, end_date):
    # Fetch data from database:
    hlocv_dataframe = database.get_hlocv_from_db(ticker, start_date, end_date)
    if heikin_ashi:
        hlocv_dataframe = heik_ash.heikin_ashi(hlocv_dataframe)
    hlocv_dataframe.symbol = str(ticker)
    hlocv_dataframe.company = ""
    hlocv_dataframe.pair = "USD"
    # st.write(str(ticker))
    final_hlocv_dataframe = hlocv_dataframe
    keep = False
    for condition in cond_dataclass_list:
        if condition.price:
            final_hlocv_dataframe, keep = price_indicator_comparison(condition, final_hlocv_dataframe)
            if not keep:
                break
        elif condition.indicator1 and condition.indicator2 and not condition.price:
            final_hlocv_dataframe, keep = indicator1_indicator2_comparison(condition, final_hlocv_dataframe)
            if not keep:
                break
    if keep:
        return final_hlocv_dataframe, ticker, True
    else:
        return None, None, False


def get_ticker_list_conditions_met(cond_dataclass_list, index_ticker_list, start_date, end_date):
    tickers_indicators_dataframe_list = []
    ticker_list_condition_met = []

    for i, ticker in enumerate(index_ticker_list):
        df_ticker_cm, ticker_cm, filled = get_ticker_condition_met(ticker, cond_dataclass_list, start_date, end_date)
        if filled:
            tickers_indicators_dataframe_list.append(df_ticker_cm)
            ticker_list_condition_met.append(ticker_cm)
    return tickers_indicators_dataframe_list, ticker_list_condition_met


def plot_chart(ticker_indicators_dataframe):
    return chart_mpl.plot_chart(ticker_indicators_dataframe)


def save_to_csv(df: pd.DataFrame):
    filename = 'tickers_condition_met.csv'
    df.to_csv(filename, index=False)


def read_from_csv() -> pd.DataFrame:
    filename = 'tickers_condition_met.csv'
    return pd.read_csv(filename, index_col=None)


# main:
entryStrategyQueryList = strategy_list(keyWords)

with st.expander("Format Check:"):
    check_format(entryStrategyQueryList, keyWords)
with st.expander("Parsed:"):
    condition_dataclass_list = parse_entry_query_to_condition_dataclass_list(entryStrategyQueryList)
    st.write(condition_dataclass_list)

header = {'symbol': [], 'sector': [], 'close (USD)': [], 'change (1d)': [], 'last date': []}
current_screen_list = pd.DataFrame(header)
tickersIndicatorsDataframeList = []

if st.button("Run technical screener"):
    with st.spinner('Screening the market ..'):
        tickersIndicatorsDataframeList, tickers_condition_met_list = get_ticker_list_conditions_met(
            condition_dataclass_list,
            get_index_ticker_list(
                index_selector),
            start_date,
            end_date)
    st.success(
        f"Screened the market! Found {len(tickersIndicatorsDataframeList)} out of {len(get_index_ticker_list(index_selector))}")

    for ticker, df in zip(tickers_condition_met_list, tickersIndicatorsDataframeList):
        date_str = str(df.tail(1).index[0]).split(" ", 1)[0]
        last_open = round(df.tail(1).iloc[0]['open'], 2)
        last_close = round(df.tail(1).iloc[0]['close'], 2)
        percent_gain = str(round((last_close-last_open), 2)) + " % "
        row = {'symbol': str(ticker), 'sector': "htbf", 'close (USD)': str(last_close), 'change (1d)': percent_gain, 'last date': date_str}
        current_screen_list = current_screen_list.append(row, ignore_index=True)

    save_to_csv(current_screen_list)

current_screen_list = read_from_csv()
st.write(f"Last screening results:")
st.dataframe(data=current_screen_list.style.highlight_max(axis=0))

st.markdown("""---""")
st.write('#### Fundamentals')
if st.checkbox("Enable filter"):
    fund_col0, fund_col1, fund_col2, fund_col3, fund_col4, fund_col5 = st.columns(6)

    with fund_col0:
        max_peg_ration = st.text_input('Max PEG-Ratio', '2')
    with fund_col1:
        min_beta = st.text_input('Min beta', '1.1')
    with fund_col2:
        min_revenueGrowth = st.text_input('Min revenueGrowth', '0.08')
    with fund_col3:
        min_returnOnEquity = st.text_input('Min returnOnEquity', '1.5')
    with fund_col4:
        min_returnOnAssets = st.text_input('Min returnOnAssets', '0.20')
    with fund_col5:
        min_dividendRate = st.text_input('Min dividendRate', '0.9')


if st.button("Add fundamental Stats"):
    current_screen_list = read_from_csv()
    st.write(f"After fundamental filter: ({len(current_screen_list)})")
    st.dataframe(data=current_screen_list)

st.markdown("""---""")
st.write('#### Generate charts and reports')
if st.button("Plot tickers"):
    tickersIndicatorsDataframeList, _ = get_ticker_list_conditions_met(
        condition_dataclass_list,
        read_from_csv()['symbol'],
        start_date,
        end_date)
    with st.spinner('Processing and plotting ..'):
        for i, dataframe in enumerate(tickersIndicatorsDataframeList):
            figure = plot_chart(dataframe)
            st.pyplot(figure)
