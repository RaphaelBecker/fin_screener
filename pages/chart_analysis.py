import streamlit as st
import datetime
from indicators.support_resistance import find_support_and_resistance_lines

from chart.chart import Chart
import data.db_connector as database
from data import helpers
from data import dataset

st.markdown("# Analyse assets")
st.sidebar.markdown("# Analyse assets")

# Select market:
stock_index_selector = st.sidebar.selectbox('Select index', sorted(dataset.market_index_list), index=0)

# Select ticker from choosen market:
tickers = dataset.get_tickers(stock_index_selector)
if isinstance(tickers, list):
    ticker_selector = st.sidebar.selectbox('Select ticker', sorted(tickers), index=0)
elif isinstance(tickers, dict):
    ticker_selector = st.sidebar.selectbox('Select ticker', sorted(tickers.keys()), index=0)

# Set start and end point to fetch data:
start_date = st.sidebar.date_input('Start date', datetime.datetime(2021, 8, 1))
end_date = st.sidebar.date_input('End date', datetime.datetime.now().date())

# Update Database on sidebar:
database_update_progress_bar = st.sidebar.progress(0)
if st.sidebar.button('update database'):
    success_ticker_list, failed_ticker_list = database.snapshot(helpers.get_symbol_list('data/smp500_symbols.csv'), database_update_progress_bar)
    st.sidebar.write(f"Success: {len(success_ticker_list)} / Failed: {len(failed_ticker_list)} "
                     f" Total: {len(success_ticker_list) +len(failed_ticker_list)}")
    database_update_progress_bar.success("Successfully updated database!")

# Fetch data from database
df_ticker = database.get_hlocv_from_db(ticker_selector, start_date, end_date)

# Fetch the data for specified ticker e.g. AAPL from yahoo finance
#df_ticker = pdr.DataReader(ticker_selector, 'yahoo', start_date, end_date)

if isinstance(tickers, list):
    st.header(f'{ticker_selector},  last: {df_ticker.tail(1).index.item()}')
elif isinstance(tickers, dict):
    st.header(f'[{ticker_selector}] {tickers[ticker_selector]}, last: {df_ticker.tail(1).index.item().date()}')


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(df_ticker)

chart = Chart(ticker_selector, df_ticker)

# Render plot using plotly_chart
st.plotly_chart(chart.fig)
