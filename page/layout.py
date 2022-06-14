import streamlit as st
from page.sidebar import Sidebar
from page.chart import Chart
from data.StockDataset import StockDataset
import pandas_datareader as pdr
import indicators.heikin_ashi as heikin_ashi


class Layout:
    def __init__(self, app_name):
        self.app_name = app_name
        self.stock_dataset = StockDataset
        self.sidebar = Sidebar(self.stock_dataset.tickers)

        # Add some markdown
        st.sidebar.markdown("Made with love using [Streamlit](https://streamlit.io/).")
        st.sidebar.markdown("# :chart_with_upwards_trend:")

        # Fetch the data for specified ticker e.g. AAPL from yahoo finance
        df_ticker = pdr.DataReader(self.sidebar.ticker_selector, 'yahoo', self.sidebar.start_date, self.sidebar.end_date)

        # TODO: make heikin ashi optional:
        df_ticker = heikin_ashi.heikin_ashi(df_ticker)

        st.header(f'{self.sidebar.ticker_selector} Stock Price')

        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(df_ticker)

        chart = Chart(self.sidebar.ticker_selector, df_ticker)

        # Render plot using plotly_chart
        st.plotly_chart(chart.fig)
