import cufflinks as cf


class Chart:
    def __init__(self, ticker, df_ticker):
        self.ticker = ticker
        self.df_ticker = df_ticker
        # Interactive data visualizations using cufflinks
        # Create candlestick page
        self.qf = cf.QuantFig(self.df_ticker, legend='top', name=ticker)

        # Technical Analysis Studies can be added on demand
        # Add Relative Strength Indicator (RSI) study to QuantFigure.studies
        self.qf.add_rsi(periods=20, color='java')

        # Add Bollinger Bands (BOLL) study to QuantFigure.studies
        self.qf.add_bollinger_bands(periods=20, boll_std=2, colors=['magenta', 'grey'], fill=True)

        # Add 'volume' study to QuantFigure.studies
        self.qf.add_volume()

        self.fig = self.qf.iplot(asFigure=True, dimensions=(1200, 600))
