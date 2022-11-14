import numpy as np


# stock = yf.Ticker(ticker)
# history_data = stock.history(interval = i, period = str(p) + "d")

def get_vol_axes(ticker_closes, ticker_volumes, closes_ax, bars_count):
    """

    :param ticker_closes: timeseries of close prices of a ticker
    :param ticker_volumes: timeseries of volumes
    :param closes_ax: range of bars charts between min and max ticker price
    :return:
    """
    volume_ax = np.zeros(bars_count)
    for i in range(0, len(ticker_volumes)):
        for bar in range(0, bars_count-1):
            if closes_ax[bar] <= ticker_closes[i] < closes_ax[bar+1]:
                volume_ax[bar] += ticker_volumes[i]

    return volume_ax


def get_volume_prep(ohlcvind_ticker_dataframe, bars_count):
    """
    :param ohlcvind_ticker_dataframe: ticker dataframe
    :param bars_count: amount of bar on y-axis
    :return:closes_ax: array, vol_ax: array, vol_peaks_closes: array, upper: int, lower: int
    """
    closes = ohlcvind_ticker_dataframe['close']
    volumes = ohlcvind_ticker_dataframe['volume']
    lower = closes.min()
    upper = closes.max()
    closes_ax = np.linspace(lower, upper, num=bars_count)
    vol_ax = get_vol_axes(closes, volumes, closes_ax, bars_count)
    length_df = ohlcvind_ticker_dataframe.size / 40
    max_vol_ax = vol_ax.max()
    bar_length_scale_factor = length_df / max_vol_ax
    vol_ax = vol_ax * bar_length_scale_factor
    vol_peaks_closes = []
    for i in range(0, len(vol_ax)):
        try:
            if vol_ax[i-4] < vol_ax[i] \
                and vol_ax[i-3] < vol_ax[i] \
                and vol_ax[i-2] < vol_ax[i] \
                and vol_ax[i-1] < vol_ax[i] \
                and vol_ax[i+1] < vol_ax[i] \
                and vol_ax[i+2] < vol_ax[i] \
                and vol_ax[i+3] < vol_ax[i]:
                vol_peaks_closes.append(closes_ax[i])
        except IndexError:
            pass
    return closes_ax, vol_ax, vol_peaks_closes, upper, lower