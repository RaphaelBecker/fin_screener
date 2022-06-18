import cufflinks as cf
import streamlit as st
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
            supres_df = df_ticker.dropna(axis=0, how="any", thresh=None, subset='supp_res_levels', inplace=False)
            last_close = df_ticker.tail(1)['Close'].item()
            for date, row in supres_df.T.iteritems():
                if last_close < row['Close'].item():
                    if row['Low'].item() == row['supp_res_levels'].item():
                        self.qf.add_resistance(date=str(date.date()), on='low', mode='toend')
                    if row['High'].item() == row['supp_res_levels'].item():
                        self.qf.add_resistance(date=str(date.date()), on='high', mode='toend')
                else:
                    self.qf.add_support(date=str(date.date()), on='high', mode='toend', color='green')

        if 'RSI' in technical_indicators:
            self.qf.add_rsi(periods=20, color='java')

        if 'MACD' in technical_indicators:
            self.qf.add_macd(fast_period=12, slow_period=26, signal_period=9)

        if 'Vol' in technical_indicators:
            self.qf.add_volume()

        self.fig = self.qf.iplot(asFigure=True, dimensions=(1400, 600), up_color='green', down_color='red',
                                 fixedrange=False)