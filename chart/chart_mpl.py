import matplotlib.pyplot as plt
import pandas
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num


def plot_chart(ohlcvind_ticker_dataframe: pandas.DataFrame):
    if ohlcvind_ticker_dataframe.symbol:
        title_string = "Symbol: " + ohlcvind_ticker_dataframe.symbol + ", last: " + str(ohlcvind_ticker_dataframe.tail(1).index.item().date())
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
    ax_candle = fig.add_axes((0, 0.48, 1, 0.63))
    ax_candle.tick_params(axis='y', which='both', labelleft=False, labelright=True)

    plt.suptitle(title_string, ha='center', y=1.14, fontsize=10)

    # Format x-axis ticks as dates
    ax_candle.xaxis_date()

    # plot candle stick chart:
    bar_width = (1 / 2.5) * (ohlc[1][0] - ohlc[0][0])
    candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r", width=bar_width)
    ylable_text = 'USD'
    ax_candle.set_ylabel(ylable_text, size=10)
    ax_candle.legend(loc='lower left', fontsize='small', frameon=True, fancybox=True)

    ax_candle.get_legend().set_title("legend")

    # add price at last candle:
    last_close = ohlcvind_ticker_dataframe.at[max(ohlcvind_ticker_dataframe.index), 'close']
    ax_candle.text(x=max(ohlcvind_ticker_dataframe.index), y=float(last_close),
                   s='  ← ' + '{:.2f}'.format(float(last_close)), alpha=1, color='blue', fontsize='x-small')

    return fig
