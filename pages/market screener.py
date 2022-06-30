import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import re

st.write("# This is the market screener")

# Set up sections of web page
header = st.container()
screen_settings = st.container()
result_list = st.container()

st.sidebar.markdown("# Market Screener")
index = st.sidebar.selectbox('Select index', sorted(['SMP500', 'DAX']), index=0)

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

with screen_settings:
    with st.expander("Fundamental options"):
        st.write("TBD")

    with st.expander("Technical options"):
        keyWords = st_tags(
            label='# Entry Strategy:',
            text='Press enter to add more',
            value=['<ema-20', 'close<ema-20', 'close>ema-50', 'low>lowerbb', 'close<234', 'sma-200upturn',
                   'sma-200downturn',
                   'sma-20'
                   '<sma-50'],
            suggestions=['<ema-20', 'close<ema-20', 'close>ema-50', 'low>lowerbb', 'close<234', 'sma-200upturn',
                         'sma-200downturn', 'sma-20<sma-50'],
            maxtags=50,
            key="entry_stategy")


# QUERY PARSER:

## possible boolean operations in keys:
# price - oper - ind,
# price - oper - val,
# ind - oper - ind,
# ind - oper - val,
# ind - oper - bool

def strategy_list(keywords):
    # parse logic
    entry_strategy_query_list = []
    i = 0
    for key in keywords:
        key = re.split('(<|>|=|-|upturn|downturn)', key)
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
    for operator in ['<', '>', '=', '-', '_']:
        if key.find(operator) != -1:
            return True
        else:
            return False


def value(key: str) -> bool:
    if key.isdigit():
        return True
    else:
        return False


def indicator(key: str) -> bool:
    if not price(key):
        if not operator(key):
            if not value(key):
                return True
            else:
                return False


def filter_index(entry_strategy_query_list, index):
    for entry_list in entry_strategy_query_list:
        st.write(f"Length: {len(entry_list)}")
        for item in entry_list:
            if price(item):
                st.write(f"{item} -> Price")
            if operator(item):
                st.write(f"{item} -> Operator")
            if indicator(item):
                st.write(f"{item} -> Indicator")
            if value(item):
                st.write(f"{item} -> Value")
        st.write("---------------------")


def check_format(entry_strategy_query_list, keywords):
    for query_list, query_string in zip(entry_strategy_query_list, keywords):
        if operator(query_list[0]):
            st.write(
                f"Format error: '{query_string}' ignored!")
            st.write("Begin with price type ('close' or 'low' etc.) or indicator type ('ema-20', cci-50)")
            keywords.remove(query_string)
            entry_strategy_query_list.remove(query_list)


entryStrategyQueryList = strategy_list(keyWords)

with st.expander("Format Check:"):
    check_format(entryStrategyQueryList, keyWords)
with st.expander("List:"):
    st.write(keyWords)
with st.expander("Parsed:"):
    st.write(entryStrategyQueryList)
with st.expander("Parsed computation:"):
    filter_index(entryStrategyQueryList, index)

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
