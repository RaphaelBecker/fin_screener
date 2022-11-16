import numpy as np
import pandas as pd
import talib
from talib import MA_Type


def compute_bb_bands(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe["upper_bollinger"], dataframe["middle_bollinger"], dataframe[
        "lower_bollinger"] = talib.BBANDS(dataframe["close"], timeperiod=30, matype=0) # MA_Type.T3
    return dataframe


def compute_contraction_signal(dataframe: pd.DataFrame):
    len_df = len(dataframe) - 1
    len_df_third = int(len_df / 3)
    bb_gap_last_close = dataframe["upper_bollinger"][len_df] - dataframe["lower_bollinger"][len_df]

    for i in range(len_df - len_df_third, len_df, 1):
        bb_gap_step = dataframe["upper_bollinger"][i] - dataframe["lower_bollinger"][i]
        if bb_gap_last_close > bb_gap_step:
            return False, dataframe
        else:
            continue
    dataframe['BBANDS'] = np.nan
    dataframe['BBANDS'][len_df] = 1
    return True, dataframe


def run_bb_contr(dataframe: pd.DataFrame):
    dataframe = compute_bb_bands(dataframe)
    signal_bool, dataframe = compute_contraction_signal(dataframe)
    return signal_bool
