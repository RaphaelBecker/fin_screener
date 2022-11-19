import matplotlib.pyplot as plt
import pandas
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num
import utils.talib_functions as talib_funcs
from data import db_connector

from indicators import vol_profile


def overlap_studies(ohlcvind_ticker_dataframe: pandas.DataFrame):
    columns = ohlcvind_ticker_dataframe.columns
    columns_compare = list(map(lambda col: col.split("_", 1)[0], columns))
    list_ = list(talib_funcs.overlap_studies_functions.keys())
    matches = set(columns_compare).intersection(list_)  # keep matchings values
    plotted_overlap_studies = []
    for column in columns:
        for match in matches:
            if match in column:
                plotted_overlap_studies.append(column)
    if 'HT_TRENDLINE_None' in columns:
        ohlcvind_ticker_dataframe.rename(columns={'HT_TRENDLINE_None': 'HT_TRENDLINE'}, inplace=True)
        plotted_overlap_studies.append('HT_TRENDLINE')
    return plotted_overlap_studies


def momentum_indicators(ohlcvind_ticker_dataframe: pandas.DataFrame):
    columns = ohlcvind_ticker_dataframe.columns
    columns_compare = list(map(lambda col: col.split("_", 1)[0], columns))
    list_ = list(talib_funcs.momentum_indicators.keys())
    matches = set(columns_compare).intersection(list_)  # keep matchings values
    plotted_momentum_indicators = []
    for column in columns:
        for match in matches:
            if match in column:
                plotted_momentum_indicators.append(column)
    return plotted_momentum_indicators


def volume_indicators():
    pass


def volatility_indicators(ohlcvind_ticker_dataframe: pandas.DataFrame):
    columns = ohlcvind_ticker_dataframe.columns
    columns_compare = list(map(lambda col: col.split("_", 1)[0], columns))
    list_ = list(talib_funcs.volatility_indicators.keys())
    matches = set(columns_compare).intersection(list_)  # keep matchings values
    plotted_volatility_indicators = []
    for column in columns:
        for match in matches:
            if match in column:
                plotted_volatility_indicators.append(column)
    return plotted_volatility_indicators


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


def custom_indicators(ohlcvind_ticker_dataframe: pandas.DataFrame):
    columns = ohlcvind_ticker_dataframe.columns
    columns_compare = list(map(lambda col: col.split("_", 1)[0], columns))
    list_ = list(talib_funcs.custom_indicators.keys())
    matches = set(columns_compare).intersection(list_)  # keep matchings values
    plotted_custom_indicators = []
    for column in columns:
        for match in matches:
            if match in column:
                plotted_custom_indicators.append(column)
    return plotted_custom_indicators


def plot_chart(ohlcvind_ticker_dataframe: pandas.DataFrame):
    # Get all fundamentals:
    ticker_info = db_connector.get_ticker_info(ohlcvind_ticker_dataframe.symbol)
    long_business_summary_line_broken_up = "not found"
    long_name = "not found"
    industry_sector = "not found"
    # fill info data if possible:
    try:
        long_name = ticker_info["longName"][0]
    except KeyError:
        pass

    try:
        long_business_summary = ticker_info["longBusinessSummary"][0]
        words = long_business_summary.split()
        long_business_summary_line_broken_up = ""
        word_count = 0
        break_count = 1
        for word in words:
            long_business_summary_line_broken_up += word + " "
            word_count += 1
            if word_count == 20 or "." in word:
                long_business_summary_line_broken_up += "\n"
                word_count = 0
                break_count = break_count + 1
        break_count = (break_count / 55) + ((1 / break_count) * 1.4)
    except KeyError:
        break_count = 0
    try:
        industry_sector = "Sektor: " + ticker_info["sector"][0] + ",      Industry: " + ticker_info["industry"][0]
    except KeyError:
        pass

    # compute technicals
    if ohlcvind_ticker_dataframe.symbol:
        title_string = "Symbol: " + ohlcvind_ticker_dataframe.symbol + ": " + long_name + ", last: " + str(
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
    ax_candle = fig.add_axes((0, 0.20, 1, 0.8))
    ax_candle.tick_params(axis='y', which='both', labelleft=False, labelright=True)

    plt.suptitle(title_string, ha='center', y=1.03, fontsize=10)

    # Format x-axis ticks as dates
    ax_candle.xaxis_date()

    # plot candle stick chart:
    bar_width = (1 / 5) * (ohlc[1][0] - ohlc[0][0])
    candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r", width=bar_width)
    ylable_text = 'USD'
    ax_candle.set_ylabel(ylable_text, size=10)

    # plot overlap studies:
    for overlap_study in overlap_studies(ohlcvind_ticker_dataframe):
        # BBANDS has 3 lines to plot:
        if overlap_study == 'BBANDS':
            ax_candle.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe["upper_bollinger"],
                           alpha=0.5, label="upper BB")
            ax_candle.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe["lower_bollinger"],
                           alpha=0.5, label="lower BB")
            # debug:
            # ax_candle.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe["KC_UPPER"],
            #               alpha=0.5, label="upper KC")
            # ax_candle.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe["KC_LOWER"],
            #               alpha=0.5, label="lower KC")
        # overlap studies with one single line to plot
        else:
            ax_candle.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe[overlap_study],
                           alpha=0.5,
                           label=overlap_study)

    # plot Indicators below chart:
    momentum_indicators_list = momentum_indicators(ohlcvind_ticker_dataframe)
    volatility_indicators_list = volatility_indicators(ohlcvind_ticker_dataframe)
    custom_id_indicators_list = custom_indicators(ohlcvind_ticker_dataframe)
    if momentum_indicators_list or volatility_indicators_list or custom_id_indicators_list:
        # create subplot section:
        ax_indicators = fig.add_axes((0, 0.001, 1, 0.2), sharex=ax_candle)
        ax_indicators.tick_params(axis='y', which='both', labelleft=False, labelright=True)

        for momentum_indicator in momentum_indicators_list:
            ax_indicators.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe[momentum_indicator],
                               alpha=0.5,
                               label="Momentum: " + momentum_indicator)
            last_momentum_value = ohlcvind_ticker_dataframe[momentum_indicator].tail(1)[0]
            ax_indicators.text(x=max(ohlcvind_ticker_dataframe.index), y=float(last_momentum_value),
                               s=' < ' + '{:.2f}'.format(float(last_momentum_value)), alpha=1, color='b',
                               fontsize='x-small')

        for volatility_indicator in volatility_indicators_list:
            ax_indicators.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe[volatility_indicator],
                               alpha=0.5,
                               label="Volatility: " + volatility_indicator)
            last_momentum_value = ohlcvind_ticker_dataframe[volatility_indicator].tail(1)[0]
            ax_indicators.text(x=max(ohlcvind_ticker_dataframe.index), y=float(last_momentum_value),
                               s=' < ' + '{:.2f}'.format(float(last_momentum_value)), alpha=1, color='b',
                               fontsize='x-small')

        for custom_id_indicator in custom_id_indicators_list:
            if custom_id_indicator == "TDI_signal":
                ax_indicators.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe["rsi"],
                                   alpha=0.5,
                                   label="TDI rsi_14")
                ax_indicators.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe["rsi_sig_line"],
                                   alpha=0.5,
                                   label="TDI rsi signal")
                ax_indicators.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe["upper_rsi_bollinger"],
                                   alpha=0.5,
                                   label="TDI upper bb")
                ax_indicators.plot(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe["lower_rsi_bollinger"],
                                   alpha=0.5,
                                   label="TDI lower bb")
                ax_indicators.scatter(ohlcvind_ticker_dataframe.index, ohlcvind_ticker_dataframe["TDI_signal"],
                                   alpha=0.5,
                                   label="SIGNAL")


        ax_indicators.legend(loc='lower left', fontsize='small', frameon=True, fancybox=True)
        ax_indicators.get_legend().set_title("Indicators")

    ax_candle.legend(loc='best', fontsize='small', frameon=True, fancybox=True)
    ax_candle.get_legend().set_title("legend")

    # Volume Profile on y axis:
    bars_count = 100
    closes_ax, vol_ax, vol_peaks_closes, upper, lower = vol_profile.get_volume_prep(ohlcvind_ticker_dataframe,
                                                                                    bars_count)
    bar_height = (upper - lower) / bars_count
    ax_candle.barh(closes_ax, vol_ax, height=bar_height, left=ohlcvind_ticker_dataframe[0:1].index,
                   align='center', alpha=0.25, facecolor='b')

    # price levels to volume lines
    for vol_peak_close in vol_peaks_closes:
        ax_candle.axhline(y=float(vol_peak_close), linewidth=1, alpha=.2, color='b', linestyle='-')
        ax_candle.text(x=max(ohlcvind_ticker_dataframe.index), y=float(vol_peak_close),
                       s='  ' + '{:.2f}'.format(float(vol_peak_close)), alpha=1, color='b', fontsize='x-small')

    # Add price at last candle:
    last_close = ohlcvind_ticker_dataframe.at[max(ohlcvind_ticker_dataframe.index), 'close']
    ax_candle.text(x=max(ohlcvind_ticker_dataframe.index), y=float(last_close),
                   s='                 ' + '{:.2f}'.format(float(last_close)), alpha=1, color='r', fontsize='x-small')

    # Horizontal red dot line at price level
    ax_candle.axhline(y=float(last_close), linewidth=.5, color='r', linestyle='dashed')

    # add info text to bottom:
    # ax_text = fig.add_axes((0, 0, 1, 0.001), sharex=ax_candle)
    plt.figtext(0, -.06, industry_sector, ha="left", fontsize='x-small')
    plt.figtext(0, -break_count, long_business_summary_line_broken_up, ha="left", fontsize='x-small')
    return fig
