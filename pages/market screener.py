import csv
import datetime
from dataclasses import dataclass

import streamlit as st
import talib
import re
import numpy as np
from data import dataset
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


st.write("# Market Screener")

if "words" not in st.session_state:
    st.session_state.words = []

# Set up sections of web page
header = st.container()
screen_settings = st.container()
result_list = st.container()

st.sidebar.markdown("# Market Screener")
# select market
index_selector = st.sidebar.selectbox('Select index', sorted(dataset.market_index_list), index=0)
timeframe_selector_mock = st.sidebar.selectbox('Select timeframe', ["4h", "6h", "12h", "1d", "3d", "1w", "1m"], index=0)


def get_index_ticker_list(index_ticker_list):
    # Select ticker from choosen market:
    index_ticker_list = dataset.get_tickers(index_ticker_list)
    if isinstance(index_ticker_list, dict):
        index_ticker_list = index_ticker_list.keys()
    return index_ticker_list


def get_talib_functions_format_list(nested_dict):
    list_ = list(nested_dict.values())
    return list(map(lambda x: list(x.keys())[0], list_))


heikin_ashi = False
if st.checkbox("Heikin Anshi"):
    heikin_ashi = True

keyWords = st.text_input('Entry Strategy',
                         value='close>SMA(100) AND close<SMA(50) AND SMA(100)>SMA(200) AND SMA(50)>SMA(100)')
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


def parse_etry_query_to_condition_dataclass_list(entry_strategy_query_list):
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


def save_to_csv(tickers: []):
    filename = 'tickers_condition_met.csv'
    with open(filename, 'w', encoding='utf8', newline='') as output_file:
        mywriter = csv.writer(output_file, delimiter=',')
        mywriter.writerow(tickers)

def read_from_csv() -> []:
    ticker_list = []
    with open('tickers_condition_met.csv', 'r', newline='') as file:
        myreader = csv.reader(file, delimiter=',')
        for rows in myreader:
            ticker_list.append(rows)
    return ticker_list[0]

# main:

# Set start and end point to fetch data:
start_date = st.sidebar.date_input('Start date', datetime.datetime(2019, 1, 1))
end_date = st.sidebar.date_input('End date', datetime.datetime.now().date())

entryStrategyQueryList = strategy_list(keyWords)

with st.expander("Format Check:"):
    check_format(entryStrategyQueryList, keyWords)
with st.expander("Parsed:"):
    condition_dataclass_list = parse_etry_query_to_condition_dataclass_list(entryStrategyQueryList)
    st.write(condition_dataclass_list)

tickersIndicatorsDataframeList = []
if st.button("Run screener"):
    with st.spinner('Screening the market ..'):
        tickersIndicatorsDataframeList, tickers_condition_met_list = get_ticker_list_conditions_met(condition_dataclass_list,
                                                                        get_index_ticker_list(
                                                                            index_selector),
                                                                        start_date,
                                                                        end_date)
    st.success(
        f"Screened the market! Found {len(tickersIndicatorsDataframeList)} out of {len(get_index_ticker_list(index_selector))}")

    save_to_csv(tickers_condition_met_list)

tickers_condition_met_list = read_from_csv()
st.write(f"Currents screening results ({len(tickers_condition_met_list)})")
st.write(tickers_condition_met_list)

if st.button("Plot tickers"):

    tickersIndicatorsDataframeList, _ = get_ticker_list_conditions_met(
        condition_dataclass_list,
        read_from_csv(),
        start_date,
        end_date)
    with st.spinner('Processing and plotting ..'):
        for i, dataframe in enumerate(tickersIndicatorsDataframeList):
            figure = plot_chart(dataframe)
            st.pyplot(figure)
