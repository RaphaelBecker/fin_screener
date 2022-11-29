import numpy as np
import pandas
import talib


def _arg_x_as_expected(value):
    """Ensure argument `x` is a 1-D C-contiguous array of dtype('float64').
    Used in `find_peaks`, `peak_prominences` and `peak_widths` to make `x`
    compatible with the signature of the wrapped Cython functions.
    Returns
    -------
    value : ndarray
        A 1-D C-contiguous array with dtype('float64').
    """
    value = np.asarray(value, order='C', dtype=np.float64)
    if value.ndim != 1:
        raise ValueError('`x` must be a 1-D array')
    return value


def find_simple_peaks(x, threshold: int, min_width: int) -> []:
    x = _arg_x_as_expected(x)
    return_arr = []
    # print(len(x))
    for i in range(0, len(x)):
        # print(f"Elem: {i}: {x[i]}")
        prev_higher = False
        for y in range(0, min_width):
            prev_higher = False
            if x[i - y] > x[i - 1]:
                prev_higher = True
                break
        if not prev_higher and x[i - 1] > threshold and x[i] < x[i - 1]:
            return_arr.append(i - 1)
            # if x[i-5] < x[i-1] and x[i-4] < x[i-1] and x[i-3] < x[i-1] and x[i-2] < x[i-1] and x[i] < x[i-1] and x[i-1] > threshhold:
            # print(f"Peak at: {i-1}: {x[i-1]}")
            # return_arr.append(i-1)
    return return_arr


def find_and_insert_peaks_in_dataframe(dataframe, indicator, lower_barrier, upper_barrier, min_width=6):
    peak_name = str(indicator.lower()) + "_peak"
    dataframe[peak_name] = np.nan

    peaks = find_simple_peaks(dataframe[indicator], threshold=upper_barrier, min_width=min_width)
    peaks_neg = find_simple_peaks(-dataframe[indicator], threshold=-lower_barrier, min_width=min_width)

    for i in range(len(peaks)):
        dataframe.at[dataframe.index[peaks[i]], peak_name] = 1

    for i in range(len(peaks_neg)):
        dataframe.at[dataframe.index[peaks_neg[i]], peak_name] = -1

    return dataframe


def compute_divergence_signal(dataframe, peaks_df, indicator, divergence_name, price_x_indicator_filter_d):
    dataframe[divergence_name] = np.nan
    if indicator == 'RSI':
        threshold_first = 73
        threshold_last = 69
        downbreak = 1  # first rsi value after rsi div has to fall down, otherwise too many false signals ware generated
    else:
        threshold_first = 0
        threshold_last = 0
        downbreak = 0
    try:
        for i in range(len(peaks_df)):
            price_diff_normalized = (abs(float(dataframe.at[peaks_df.index[i], 'close']) - float(dataframe.at[
                                                                                                peaks_df.index[
                                                                                                    i + 1], 'close']))) / float(
                dataframe.at[peaks_df.index[i], 'close'])
            rsi_diff = abs(
                float(dataframe.at[peaks_df.index[i], indicator]) - float(dataframe.at[peaks_df.index[i + 1], indicator]))
            price_x_rsi = price_diff_normalized * rsi_diff

            # BEAR:
            if dataframe.at[peaks_df.index[i], indicator] > threshold_first and dataframe.at[
                peaks_df.index[i + 1], indicator] > threshold_last:
                if ((float(dataframe.at[peaks_df.index[i], indicator]) > float(dataframe.at[peaks_df.index[i + 1], indicator]))
                        and (float(dataframe.at[peaks_df.index[i], 'close']) < float(
                            dataframe.at[peaks_df.index[i + 1], 'close']))
                        and price_x_rsi > price_x_indicator_filter_d):
                    # print(f"{float(data.at[peaks_df.index[i + 1], indicator])} - {float(data.at[peaks_df.index[i + 1] + 1, indicator])} > {downbreak}")
                    dataframe.at[peaks_df.index[i + 1], divergence_name] = -0.1  # bear flag
            # BULL:
            if dataframe.at[peaks_df.index[i], indicator] < threshold_first and dataframe.at[
                peaks_df.index[i + 1], indicator] < threshold_last:
                if ((float(dataframe.at[peaks_df.index[i], indicator]) < float(dataframe.at[peaks_df.index[i + 1], indicator]))
                        and (float(dataframe.at[peaks_df.index[i], 'close']) > float(
                            dataframe.at[peaks_df.index[i + 1], 'close']))
                        and price_x_rsi > price_x_indicator_filter_d):
                    dataframe.at[peaks_df.index[i + 1], divergence_name] = 100  # bull flag
    except IndexError:
        pass
    return dataframe


def rsi_div_run(dataframe, lower_barrier, upper_barrier, divergence_name, min_width, max_width_d,
                price_x_indicator_filter_d) -> pandas.DataFrame:
    dataframe["RSI"] = talib.RSI(dataframe["close"], timeperiod=14)
    dataframe = find_and_insert_peaks_in_dataframe(dataframe, "RSI", lower_barrier, upper_barrier, min_width)
    peaks_df = dataframe[-np.isnan(dataframe['rsi_peak'])]
    return_div_df = compute_divergence_signal(dataframe, peaks_df, "RSI", divergence_name, price_x_indicator_filter_d)
    return return_div_df


def macd_div_run(dataframe, lower_barrier, upper_barrier, divergence_name, min_width, max_width_d,
                 price_x_indicator_filter_d) -> pandas.DataFrame:
    # MACD has to be calculted first:
    dataframe["MACD"], dataframe["MACD_INDICATOR"], _ = talib.MACD(dataframe['close'])
    dataframe = find_and_insert_peaks_in_dataframe(dataframe, "MACD", lower_barrier, upper_barrier, min_width)
    peaks_df = dataframe[-np.isnan(dataframe['macd_peak'])]
    return_div_df = compute_divergence_signal(dataframe, peaks_df, "MACD", divergence_name, price_x_indicator_filter_d)
    return return_div_df


def divergence(dataframe, divergence_name, lower_barrier, upper_barrier, min_width, max_width_d,
               price_x_indicator_filter_d):
    if 'rsi_div_signal' in divergence_name:
        dataframe = rsi_div_run(dataframe, lower_barrier, upper_barrier, divergence_name, min_width, max_width_d,
                                price_x_indicator_filter_d)
    if 'macd_div_signal' in divergence_name:
        dataframe = macd_div_run(dataframe, lower_barrier, upper_barrier, divergence_name, min_width, max_width_d,
                                 price_x_indicator_filter_d)

    return dataframe
