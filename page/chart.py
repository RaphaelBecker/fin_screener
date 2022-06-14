import cufflinks as cf

# Interactive data visualizations using cufflinks
# Create candlestick page

class Chart:
    def __init__(self, ticker, df_ticker):
        self.ticker = ticker
        self.df_ticker = df_ticker
        self.config = dict({'scrollZoom': True})
        self.qf = cf.QuantFig(self.df_ticker, kind='candlestick', legend='right', name=ticker)

        # key has to be checked if in dataframe!
        annotation = {'2022-04-06T00:00:00': 'text'}
        #self.qf.add_annotations(annotations=annotation, textangle=0)

        # dateformat: %y%m%d

        self.qf.add_trendline(date0='2022-04-04', date1='2022-06-08', from_strfmt='%y%b%d', on='high',
                              to_strfmt='%Y-%m-%d', color='blue')

        self.qf.add_trendline(date0='2022-04-01', date1='2022-05-20', from_strfmt='%y%b%d', on='low',
                              to_strfmt='%Y-%m-%d', color='blue')

        self.qf.add_support(date='2022-05-20', on='low', mode='starttoend', color='green')

        self.qf.add_resistance(date='2022-03-14', on='low', mode='starttoend')

        self.qf.add_resistance(date='2021-10-05', on='low', mode='starttoend')

        # Technical Analysis Studies can be added on demand
        self.qf.add_rsi(periods=20, color='java')

        self.qf.add_macd(fast_period=12, slow_period=26, signal_period=9)


        self.qf.add_ema(periods=50, color='green')
        self.qf.add_ema(periods=100, color='orange')
        self.qf.add_ema(periods=200, color='red')

        #self.qf.add_bollinger_bands(periods=20, boll_std=2, colors=['magenta', 'grey'], fill=False)

        # Add 'volume' study to QuantFigure.studies
        self.qf.add_volume()

        self.fig = self.qf.iplot(asFigure=True, dimensions=(1400, 800), up_color='green', down_color='red')




