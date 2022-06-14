import yfinance as yf
import utils.helpers as hlps


class StockDataset:
    tickers = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT']

    def __init__(self):
        self.smp500_symbols_link = 'datasets/smp500_symbols.csv'
        self.smp500_symbols = self.get_stock_symbols()

    def snapshot(self, start="2021-06-01", end=str(hlps.get_current_date())):
        with open(self.smp500_symbols_link) as f:
            for line in f:
                if "," not in line:
                    continue
                symbol = line.split(",")[0]
                data = yf.download(symbol, start=start, end=end)
                data.to_csv('data/tickers/daily/{}.csv'.format(symbol))

    def get_stock_symbols(self):
        stock_symbols = []
        with open(self.smp500_symbols_link) as f:
            for line in f:
                if "," not in line:
                    continue
                symbol = line.split(",")[0]
                stock_symbols.append(symbol)
        return stock_symbols
