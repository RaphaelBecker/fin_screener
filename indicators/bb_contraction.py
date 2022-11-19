import numpy as np
import pandas as pd
import talib
from finta import TA
from talib import MA_Type


def compute_bb_bands(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe["upper_bollinger"], dataframe["middle_bollinger"], dataframe[
        "lower_bollinger"] = talib.BBANDS(dataframe["close"], timeperiod=20, matype=MA_Type.T3)  # MA_Type.T3
    return dataframe


def compute_kc_channel(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = TA.KC(dataframe, period=20, kc_mult=1)  # MA_Type.T3
    return dataframe


def highest_high_last20(dataframe: pd.DataFrame) -> str:
    return max(dataframe.tail(20)["high"])


def lowest_low_last20(dataframe: pd.DataFrame) -> str:
    return min(dataframe.tail(20)["low"])


def mean(val1, val2) -> str:
    return (val1 + val2) / 2


def compute_contraction_signal(dataframe: pd.DataFrame):
    len_df = len(dataframe) - 1

    # kc channel wider than bollinger channel:
    if dataframe["upper_bollinger"][len_df] < dataframe["KC_UPPER"][len_df] and \
            dataframe["KC_LOWER"][len_df] < dataframe["lower_bollinger"][len_df]:
        dataframe["BBANDS"] = np.nan
        return True, dataframe
    else:
        return False, dataframe


def run_bb_contr(dataframe: pd.DataFrame):
    dataframe = compute_bb_bands(dataframe)
    kc_dataframe = compute_kc_channel(dataframe)
    dataframe = dataframe.join(kc_dataframe)
    return compute_contraction_signal(dataframe)

# Step 1: Calculate the Bollinger Bands on the market price.

# Step 2: Calculate the Keltner Channel on the market price.

# Step 3: Calculate the highest high in the last 20 periods.

# Step 4: Calculate the lowest low in the last 20 periods.

# Step 5: Find the mean between the two above results.

# Step 6: Calculate a 20-period simple moving average on the closing price
# Step 7: Calculate the delta between the closing price and the mean between the result from step 5 and 6.
