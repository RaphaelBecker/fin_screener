import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import re

st.write("# This is the market screener")

# Set up sections of web page
header = st.container()
screen_settings = st.container()
result_list = st.container()

st.sidebar.markdown("# Market Screener")
st.sidebar.selectbox('Select index', sorted(['SMP500', 'DAX']), index=0)

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
        keywords = st_tags(
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


# classification:
def price(key: str) -> bool:
    if key in ['high', 'low', 'close', 'open']:
        return True


def operator(key: str) -> bool:
    if key in ['<', '>', '=', '-', '_']:
        return True


def indicator(key: str) -> bool:
    if not price(key):
        if not operator(key):
            return True


# parse logic
entry_strategy_query_list = []
i = 0
for key in keywords:
    key = re.split('(<|>|=|-|upturn|downturn)', key)
    key = list(filter(None, key))
    entry_strategy_query_list.append(key)


def check_format(entry_strategy_query_list):
    for query_list, query_string in zip(entry_strategy_query_list, keywords):
        if operator(query_list[0]):
            st.write(
                f"Format error: '{query_string}' ignored!")
            st.write("Begin with price type ('close' or 'low' etc.) or indicator type ('ema-20', cci-50)")
            keywords.remove(query_string)
            entry_strategy_query_list.remove(query_list)


st.write("#### Format Check:")
check_format(entry_strategy_query_list)
st.write("#### List:")
st.write(keywords)
st.write("#### parsed:")
st.write(entry_strategy_query_list)

























fundamental_values='''
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
