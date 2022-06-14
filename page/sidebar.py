import datetime
import streamlit as st


class Sidebar:
    def __init__(self, ticker_list):
        # Select ticker
        self.ticker_selector = st.sidebar.selectbox('Select ticker', sorted(ticker_list), index=0)

        # Set start and end point to fetch data
        self.start_date = st.sidebar.date_input('Start date', datetime.datetime(2021, 8, 1))
        self.end_date = st.sidebar.date_input('End date', datetime.datetime.now().date())