import datetime
import time

import streamlit as st
import talib
from streamlit_tags import st_tags, st_tags_sidebar
import re
import numpy as np
from data import dataset
from data import db_connector as database
from chart import chart_mpl
from utils import talib_functions

st.write("# This is the market screener")


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


with header:
    with st.expander("Available commands and indicators"):
        st.markdown(
            """
        TODO: Show available commands and indicators here
        
        Fundamental indicators:
        ....
        Technical Indicators:
        ....
        """
        )


def get_talib_functions_format_list(nested_dict):
    list_ = list(nested_dict.values())
    return list(map(lambda x: list(x.keys())[0], list_))


with screen_settings:
    with st.expander("Fundamental options"):
        st.write("TBD")

    with st.expander("Technical options"):
        keyWords = st_tags(
            label='# Entry Strategy:',
            text='Press enter to add more',
            value=['<ema(20,10)', 'close<ema(20)', 'close>ema(50)', 'low>lowerbb', 'sma(30,30)<sma(1)'],
            suggestions=get_talib_functions_format_list(talib_functions.overlap_studies_functions) + list(talib_functions.overlap_studies.keys()),
            maxtags=50,
            key="entry_stategy")


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
            st.write(
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


def parse_etry_query_to_dict_list(entry_strategy_query_list):
    condition_list = []
    for entry_list in entry_strategy_query_list:
        condition_dict = dict()
        for item in entry_list:
            if price(item):
                condition_dict["price"] = item
            if operator(item):
                condition_dict["operator"] = item
            if indicator(item):
                if not "indicator1" in condition_dict:
                    condition_dict["indicator1"] = item
                else:
                    condition_dict["indicator2"] = item
        condition_list.append(condition_dict)
    return condition_list


def compute_talib_function(ohlcv_dataframe, talib_function_name, talib_function_args):
    print('Executing talib function: ' + talib_function_name + '(' + talib_function_args + ')')
    talib_function = getattr(talib, talib_function_name)
    ohlcv_dataframe[talib_function_name] = np.nan
    try:
        # TODO Mapping, how to built function argument list dynamically???
        result = talib_function(ohlcv_dataframe['open'], ohlcv_dataframe['high'], ohlcv_dataframe['low'],
                                ohlcv_dataframe['close'])
        ohlcv_dataframe[talib_function_name] = result.to_frame().replace(0, np.nan).replace(100, 1)
    except IndexError:
        print('IndexError!')
        pass
    return ohlcv_dataframe


def get_tickers_indicators_dataframe_list(strategy_dict, index_ticker_list, start_date, end_date):
    tickers_indicators_dataframe_list = []
    # TODO: delete, because of development reduced to 5 dataframes
    index_ticker_list = index_ticker_list[0:5]

    for i, ticker in enumerate(index_ticker_list):
        # Fetch data from database:
        hlocv_dataframe = database.get_hlocv_from_db(ticker, start_date, end_date)
        hlocv_dataframe.symbol = str(ticker)
        hlocv_dataframe.company = ""
        hlocv_dataframe.pair = "USD"
        for element in strategy_dict:
            # TODO: execute talib functions on hlocv_dataframe based on strategy dict
            #  Break if strategy condition is False
            #  If False, drop hlocv_dataframe and continue
            pass
        tickers_indicators_dataframe_list.append(hlocv_dataframe)
    return tickers_indicators_dataframe_list


def plot_chart(ticker_indicators_dataframe):
    return chart_mpl.plot_chart(ticker_indicators_dataframe)


# main:

# Set start and end point to fetch data:
start_date = st.sidebar.date_input('Start date', datetime.datetime(2021, 8, 1))
end_date = st.sidebar.date_input('End date', datetime.datetime.now().date())

entryStrategyQueryList = strategy_list(keyWords)

with st.expander("Format Check:"):
    check_format(entryStrategyQueryList, keyWords)
with st.expander("List:"):
    st.write(keyWords)
with st.expander("Parsed:"):
    condition_list = parse_etry_query_to_dict_list(entryStrategyQueryList)
    st.write(condition_list)

tickersIndicatorsDataframeList = []
debugString = ""
if st.checkbox("Run screener"):
    with st.spinner('Screening the market ..'):
        tickersIndicatorsDataframeList, debugString = get_tickers_indicators_dataframe_list(strategy_dict,
                                                                                            get_index_ticker_list(
                                                                                                index_selector),
                                                                                            start_date,
                                                                                            end_date)
    st.success('Screened the market!')

    if st.checkbox("show debug logs"):
        st.write(debugString)

    if st.checkbox("show raw dataframe"):
        for dataframe in tickersIndicatorsDataframeList:
            st.dataframe(dataframe)

    if st.checkbox("plot the dataframes"):
        for i, dataframe in enumerate(tickersIndicatorsDataframeList):
            figure = plot_chart(dataframe)
            st.pyplot(figure)
            if st.button("trade", key="trade_" + str(i)):
                st.write("Trading journal entry pop up")

fundamental_values = '''
P/E	
Forward P/E	
PEG	
P/S	
P/B	
Price/Cash	
Price/Free Cash Flow	
EPS growth
Sales growth
Return on Assets	
Return on Equity	
Return on Investment	
Current Ratio	
Quick Ratio	
LT Debt/Equity	
Debt/Equity	
Gross Margin	
Operating Margin	
Net Profit Margin	
Payout Ratio	
Insider Ownership	
Insider Transactions	
Institutional Ownership	
'''
