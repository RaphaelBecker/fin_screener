import streamlit as st
import datetime
from indicators.support_resistance import find_support_and_resistance_lines

from chart.chart import Chart
import data.db_connector as database
from data import helpers
import pandas_datareader as pdr

st.markdown("# Analyse assets")
st.sidebar.markdown("# Analyse assets")


@st.cache
def get_ticker_list():
    ticker_dict_list = database.view_all_tickers()
    ticker_list = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT']
    for ticker_dict in ticker_dict_list:
        ticker_list.append(ticker_dict["ticker"])
    return list(set(ticker_list))


ticker_selector = st.sidebar.selectbox('Select ticker', sorted(get_ticker_list()), index=0)

# Set start and end point to fetch data
start_date = st.sidebar.date_input('Start date', datetime.datetime(2021, 8, 1))
end_date = st.sidebar.date_input('End date', datetime.datetime.now().date())

database_update_progress_bar = st.sidebar.progress(0)

if st.sidebar.button('update database'):
    failed_ticker_list = database.snapshot(helpers.get_symbol_list('data/smp500_symbols.csv'), database_update_progress_bar)
    st.sidebar.write(f"Download failed on tickers: {failed_ticker_list}")

# Fetch data from database
df_ticker = database.get_hlocv_from_db(ticker_selector, start_date, end_date)

# Fetch the data for specified ticker e.g. AAPL from yahoo finance
#df_ticker = pdr.DataReader(ticker_selector, 'yahoo', start_date, end_date)


st.header(f'{ticker_selector} Stock Price')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(df_ticker)

chart = Chart(ticker_selector, df_ticker)

# Render plot using plotly_chart
st.plotly_chart(chart.fig)
