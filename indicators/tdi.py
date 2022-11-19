import numpy as np
import pandas
import talib
from talib import MA_Type


def rsi_sig_line_in_lower_bollinger_band_section(data, i) -> bool:
    try:
        if (data.at[data.index[i ], 'rsi_sig_line'] <= data.at[data.index[i], 'middle_rsi_bollinger']) \
                and (data.at[data.index[i], 'rsi_sig_line'] >= data.at[data.index[i], 'lower_rsi_bollinger']):
            return True
        else:
            return False
    except IndexError:
        pass


def rsi_sig_line_in_upper_bollinger_band_section(data, i) -> bool:
    try:
        if (data.at[data.index[i], 'rsi_sig_line'] >= data.at[data.index[i], 'middle_rsi_bollinger']) \
                and (data.at[data.index[i], 'rsi_sig_line'] <= data.at[data.index[i], 'upper_rsi_bollinger']):
            return True
        else:
            return False
    except IndexError:
        pass


def prev_rsi_below_lower_bollinger_band(data, i) -> bool:
    try:
        if data.at[data.index[i - 1], 'rsi'] <= data.at[data.index[i - 1], 'lower_rsi_bollinger']:
            return True
        else:
            return False
    except IndexError:
        pass


def prev_rsi_above_upper_bollinger_band(data, i) -> bool:
    try:
        if data.at[data.index[i - 1], 'rsi'] >= data.at[data.index[i - 1], 'upper_rsi_bollinger']:
            return True
        else:
            return False
    except IndexError:
        pass


def prev_rsi_below_signal_line(data, i) -> bool:
    try:
        if data.at[data.index[i - 1], 'rsi'] <= data.at[data.index[i - 1], 'rsi_sig_line']:
            return True
        else:
            return False
    except IndexError:
        pass


def prev_rsi_above_signal_line(data, i) -> bool:
    try:
        if data.at[data.index[i - 1], 'rsi'] >= data.at[data.index[i - 1], 'rsi_sig_line']:
            return True
        else:
            return False
    except IndexError:
        pass


def prev_rsi_below_threshold(data, i, threshold=50) -> bool:
    try:
        if data.at[data.index[i - 1], 'rsi'] <= threshold:
            return True
        else:
            return False
    except IndexError:
        pass


def prev_rsi_above_threshold(data, i, threshold=50) -> bool:
    try:
        if data.at[data.index[i - 1], 'rsi'] >= threshold:
            return True
        else:
            return False
    except IndexError:
        pass


def rsi_below_upper_bollinger_band(data, i) -> bool:
    if data.at[data.index[i], 'rsi'] <= data.at[data.index[i], 'upper_rsi_bollinger']:
        return True
    else:
        return False


def rsi_above_upper_bollinger_band(data, i) -> bool:
    if data.at[data.index[i], 'rsi'] >= data.at[data.index[i], 'upper_rsi_bollinger']:
        return True
    else:
        return False


def rsi_below_lower_bollinger_band(data, i) -> bool:
    if data.at[data.index[i], 'rsi'] <= data.at[data.index[i], 'lower_rsi_bollinger']:
        return True
    else:
        return False


def rsi_above_lower_bollinger_band(data, i) -> bool:
    if data.at[data.index[i], 'rsi'] >= data.at[data.index[i], 'lower_rsi_bollinger']:
        return True
    else:
        return False


def signal_line_below_threshold(data, i, threshold=50) -> bool:
    if data.at[data.index[i], 'rsi_sig_line'] <= threshold:
        return True
    else:
        return False


def signal_line_above_threshold(data, i, threshold=50) -> bool:
    if data.at[data.index[i], 'rsi_sig_line'] >= threshold:
        return True
    else:
        return False


def rsi_above_rsi_sig_line(data, i) -> bool:
    if data.at[data.index[i], 'rsi'] >= data.at[data.index[i], 'rsi_sig_line']:
        return True
    else:
        return False


def rsi_below_rsi_sig_line(data, i) -> bool:
    if data.at[data.index[i], 'rsi'] <= data.at[data.index[i], 'rsi_sig_line']:
        return True
    else:
        return False


def bullish_rsi_sig_line_cross(data, i) -> bool:
    # Bull cross:
    if prev_rsi_below_signal_line(data, i) and rsi_above_rsi_sig_line(data, i):
        return True
    return False


def bearish_rsi_sig_line_cross(data, i) -> bool:
    # Bear cross:
    if prev_rsi_above_signal_line(data, i) and rsi_below_rsi_sig_line(data, i):
        return True
    return False


def rsi_outer_bollinger_band_cross(data, i) -> bool:
    # Bear cross:
    if prev_rsi_above_upper_bollinger_band(data, i) and rsi_below_upper_bollinger_band(data, i):
        return True
    # Bull cross:
    elif prev_rsi_below_lower_bollinger_band(data, i) and rsi_above_lower_bollinger_band(data, i):
        return True
    return False


def previous_cross_was_rsi_outer_bollinger_cross(data, i) -> bool:
    try:
        # rsi crosses signal and bollinger band in the same index:
        if (bullish_rsi_sig_line_cross(data, i) or bearish_rsi_sig_line_cross(data, i)) and rsi_outer_bollinger_band_cross(data, i):
            return True
        # check if previous cross is rsi-bollinger cross and not rsi-signal cross:
        r = i - 1
        while not (bullish_rsi_sig_line_cross(data, r) or bearish_rsi_sig_line_cross(data, r)):
            if rsi_outer_bollinger_band_cross(data, r):
                # if rsi_above_upper_bollinger_band(data, i) or rsi_below_lower_bollinger_band(data, i):
                return True
            r = r - 1
        return False
    except IndexError:
        pass


def compute_tdi_signal(dataframe, rsi_threshold_bull_sig=30, rsi_threshold_bear_sig=70) -> (bool, pandas.DataFrame):
    """
    :param rsi_threshold_bear_sig: only catch bear signal if previous rsi was above this value (int)
    :param rsi_threshold_bull_sig: only catch bear signal if previous rsi was below this value (int)
    :param data:
    :return:
    """
    # Get RSI
    dataframe["rsi"] = talib.RSI(dataframe["close"], timeperiod=14)
    #dataframe["rsi_smoothed"] = talib.EMA(dataframe["rsi"], timeperiod=2)
    # Get RSI MA:
    dataframe["rsi_sig_line"] = talib.MA(dataframe["rsi"], timeperiod=20)
    # Get Bollinger Bands:
    dataframe["upper_rsi_bollinger"], dataframe["middle_rsi_bollinger"], dataframe["lower_rsi_bollinger"] = talib.BBANDS(dataframe["rsi"], timeperiod=30, matype=MA_Type.T3)
    # signal:
    dataframe['TDI_signal'] = np.nan
    for i in range(len(dataframe)):
        try:
            # BULLISH SIGNAL IN BOLLINGER BAND:
            if (prev_rsi_below_threshold(dataframe, i, rsi_threshold_bull_sig)
                    and rsi_sig_line_in_lower_bollinger_band_section(dataframe, i)
                    and bullish_rsi_sig_line_cross(dataframe, i)
                    and previous_cross_was_rsi_outer_bollinger_cross(dataframe, i)):
                dataframe.at[dataframe.index[i], 'TDI_signal'] = 0  # buy flag: 200
                # BULLISH SIGNAL OUT OF BOLLIGER BAND:
            if (prev_rsi_below_threshold(dataframe, i, 34)
                    and rsi_outer_bollinger_band_cross(dataframe, i)):
                dataframe.at[dataframe.index[i], 'TDI_signal'] = 0  # buy flag: 200
            # BEARISH SIGNAL:
            if (prev_rsi_above_threshold(dataframe, i, rsi_threshold_bear_sig)
                    and rsi_sig_line_in_upper_bollinger_band_section(dataframe, i)
                    and bearish_rsi_sig_line_cross(dataframe, i)
                    and previous_cross_was_rsi_outer_bollinger_cross(dataframe, i)):
                dataframe.at[dataframe.index[i], 'TDI_signal'] = 100  # buy flag: 200
        except IndexError:
            pass
    len_df = len(dataframe) - 1
    for check_index in range(len_df-3, len_df, 1):
        if dataframe.at[dataframe.index[check_index], 'TDI_signal'] == 0 \
               or dataframe.at[dataframe.index[check_index], 'TDI_signal'] == 100:
            return True, dataframe
    return False, dataframe