import streamlit as st
import datetime
from indicators.support_resistance import find_support_and_resistance_lines

from chart.chart import Chart
from data.StockDataset import StockDataset
import pandas_datareader as pdr

st.markdown("# Analyse assets")
st.sidebar.markdown("# Analyse assets")

stock_dataset = StockDataset
ticker_selector = st.sidebar.selectbox('Select ticker', sorted(stock_dataset.tickers), index=0)

# Set start and end point to fetch data
start_date = st.sidebar.date_input('Start date', datetime.datetime(2021, 8, 1))
end_date = st.sidebar.date_input('End date', datetime.datetime.now().date())


# Fetch the data for specified ticker e.g. AAPL from yahoo finance
df_ticker = pdr.DataReader(ticker_selector, 'yahoo', start_date, end_date)

df_ticker, levels, start_levels = find_support_and_resistance_lines(df_ticker)

st.header(f'{ticker_selector} Stock Price')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(df_ticker)

chart = Chart(ticker_selector, df_ticker)

# Render plot using plotly_chart
st.plotly_chart(chart.fig)
