import cufflinks as cf
import streamlit as st
# Interactive data visualizations using cufflinks
# Create candlestick pages
from indicators import heikin_ashi


class Chart:
    def __init__(self, ticker, df_ticker):
        self.ticker = ticker
        self.df_ticker = df_ticker
        self.config = dict({'scrollZoom': True, 'theme': 'white'})
        cf.set_config_file(self.config)

        # Add technical overlay studies to candlestick chart:
        overlay_studies = st.multiselect(
            'Add Overlay Studies',
            ['BB', 'EMA', 'S&R', 'Trendline', 'Heikin_Ashi'],
            [])

        # Add technical overlay studies to candlestick chart:
        technical_indicators = st.multiselect(
            'Add technical indicators',
            ['RSI', 'MACD', 'Vol'],
            [])

        if 'Heikin_Ashi' in overlay_studies:
            self.df_ticker = heikin_ashi.heikin_ashi(df_ticker)

        self.qf = cf.QuantFig(self.df_ticker, kind='candlestick', legend='right', name=ticker)
        # List of Cufflinks Themes :  ['ggplot', 'pearl', 'solar', 'space', 'white', 'polar', 'henanigans']

        # dateformat: %y%m%d

        if 'BB' in overlay_studies:
            self.qf.add_bollinger_bands(periods=20, boll_std=2, colors=['magenta', 'grey'], fill=False)

        if 'EMA' in overlay_studies:
            self.qf.add_ema(periods=50, color='green')
            self.qf.add_ema(periods=100, color='orange')
            self.qf.add_ema(periods=200, color='red')

        if 'Trendline' in overlay_studies:
            self.qf.add_trendline(date0='2022-04-04', date1='2022-06-08', from_strfmt='%y%b%d', on='high',
                                  to_strfmt='%Y-%m-%d', color='blue')

            self.qf.add_trendline(date0='2022-04-01', date1='2022-05-20', from_strfmt='%y%b%d', on='low',
                                  to_strfmt='%Y-%m-%d', color='blue')

        if 'S&R' in overlay_studies:
            self.qf.add_support(date='2022-05-20', on='low', mode='starttoend', color='green')
            self.qf.add_resistance(date='2022-03-14', on='low', mode='starttoend')
            self.qf.add_resistance(date='2021-10-05', on='low', mode='starttoend')


        if 'RSI' in technical_indicators:
            self.qf.add_rsi(periods=20, color='java')

        if 'MACD' in technical_indicators:
            self.qf.add_macd(fast_period=12, slow_period=26, signal_period=9)

        if 'Vol' in technical_indicators:
            self.qf.add_volume()

        self.fig = self.qf.iplot(asFigure=True, dimensions=(1400, 600), up_color='green', down_color='red', fixedrange=False)

