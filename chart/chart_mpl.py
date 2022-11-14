import matplotlib.pyplot as plt
import numpy as np
import pandas
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num
import utils.talib_functions as talib_funcs
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from volume_profile import vol_profile


def overlap_studies(ohlcvind_ticker_dataframe: pandas.DataFrame):
    columns = ohlcvind_ticker_dataframe.columns
    columns_compare = list(map(lambda col: col.split("_", 1)[0], columns))
    list_ = list(talib_funcs.overlap_studies_functions.keys())
    matches = set(columns_compare).intersection(list_) # keep matchings values
    plotted_overlap_studies = []
    for column in columns:
        for match in matches:
            if match in column:
                plotted_overlap_studies.append(column)
    if 'HT_TRENDLINE_None' in columns:
        ohlcvind_ticker_dataframe.rename(columns={'HT_TRENDLINE_None': 'HT_TRENDLINE'}, inplace = True)
        plotted_overlap_studies.append('HT_TRENDLINE')
    return plotted_overlap_studies


def momentum_indicators():
    pass


def volume_indicators():
    pass


def volatility_indicators():
    pass


def price_transform():
    pass


def cycle_indicators():
    pass


def pattern_recognition():
    pass


def statistic_functions():
    pass


def math_transform():
    pass


def math_operators():
    pass


def plot_chart(ohlcvind_ticker_dataframe: pandas.DataFrame):
    if ohlcvind_ticker_dataframe.symbol:
        title_string = "Symbol: " + ohlcvind_ticker_dataframe.symbol + ", last: " + str(
            ohlcvind_ticker_dataframe.tail(1).index.item().date())
    else:
        title_string = "title not available"

    ohlc = []
    for date, row in ohlcvind_ticker_dataframe.iterrows():
        highp, lowp, openp, closep = row[:4]
        ohlc.append([date2num(date), float(openp), float(highp), float(lowp), float(closep)])

    # Create figure and set axes for subplots
    plt.style.use('seaborn-white')

    plt.rcParams.update({'font.size': 8})

    fig = plt.figure()

    # ax_candle = fig.add_axes((0, 0.72, 1, 0.32))
    ax_candle = fig.add_axes((0, 0.40, 1, 0.7))
    ax_candle.tick_params(axis='y', which='both', labelleft=False, labelright=True)

    plt.suptitle(title_string, ha='center', y=1.14, fontsize=10)

    # Format x-axis ticks as dates
    ax_candle.xaxis_date()

    # plot candle stick chart:
    bar_width = (1 / 5) * (ohlc[1][0] - ohlc[0][0])
    candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r", width=bar_width)
    ylable_text = 'USD'
    ax_candle.set_ylabel(ylable_text, size=10)

    # plot overlap studies:
    for overlap_study in overlap_studies(ohlcvind_ticker_dataframe):
        ax_candle.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe[overlap_study],
                   alpha=0.5,
                   label=overlap_study)

    ax_candle.legend(loc='best', fontsize='small', frameon=True, fancybox=True)
    ax_candle.get_legend().set_title("legend")

    # Volume Profile on y axis:
    bars_count = 100
    closes_ax, vol_ax, vol_peaks_closes, upper, lower = vol_profile.get_volume_prep(ohlcvind_ticker_dataframe, bars_count)
    bar_height = (upper - lower) / bars_count
    ax_candle.barh(closes_ax, vol_ax, height=bar_height, left=ohlcvind_ticker_dataframe[0:1].index, align='center', alpha=0.25, facecolor='b')

    for vol_peak_close in vol_peaks_closes:
        ax_candle.axhline(y=float(vol_peak_close), linewidth=1, alpha=.2, color='b', linestyle='-')
        ax_candle.text(x=max(ohlcvind_ticker_dataframe.index), y=float(vol_peak_close), s='{:.2f}'.format(float(vol_peak_close)), alpha=1, color='b', fontsize='x-small')

    # Add price at last candle:
    last_close = ohlcvind_ticker_dataframe.at[max(ohlcvind_ticker_dataframe.index), 'close']
    ax_candle.text(x=max(ohlcvind_ticker_dataframe.index), y=float(last_close),
                   s='   ' + '{:.2f}'.format(float(last_close)), alpha=1, color='r', fontsize='x-small')
    # Horizontal red dot line at price level
    ax_candle.axhline(y=float(last_close), linewidth=.5, color='r', linestyle='dashed')

    return fig
