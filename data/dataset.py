import streamlit as st
import csv
import data.db_connector as database

# lists
# selector
market_index_list = ['All', 'SMP500', 'DAX']

# paths
smp500_path = 'data/smp500_symbols.csv'
dax_path = "tbd"

@st.cache
def get_tickers(stock_index: str):
    """
    :param index: market index from selectbox
    :return: dictionary as -> symbol : company_name
    """
    path = ""
    if stock_index == "All":
        all_ticker_list = []
        for ticker_dict in database.view_all_tickers():
            all_ticker_list.append(ticker_dict['ticker'])
        return all_ticker_list

    if stock_index == 'SMP500':
        path = smp500_path
    if stock_index == 'DAX':
        path = dax_path
    with open(path, mode='r') as inp:
        reader = csv.reader(inp)
        index_dict = {rows[0] : rows[1] for rows in reader}
    return index_dict
