import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import re

maxtags = st.slider('Number of tags allowed?', 1, 100, 34, key='sliderkl')

keywords = st_tags(
    label='# Entry Strategy:',
    text='Press enter to add more',
    value=['<ema-20', 'close<ema-20', 'close>ema-50', 'low>lowerbb', 'close<234', 'sma-200upturn', 'sma-200downturn',
           'sma-20'
           '<sma-50'],
    suggestions=['<ema-20', 'close<ema-20', 'close>ema-50', 'low>lowerbb', 'close<234', 'sma-200upturn', 'sma-200downturn', 'sma-20<sma-50'],
    maxtags=maxtags,
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
