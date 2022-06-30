# reference: https://mrjbq7.github.io/ta-lib/
import numpy as np
import talib
from finta import TA
from matplotlib.dates import date2num

from talib import MA_Type

print_flag = 'BASIC INDICATORS: '


def get_ohlc(dataframe):
    ohlc = []
    for date, row in dataframe.iterrows():
        openp, highp, lowp, closep = row[:4]
        ohlc.append([date2num(date), float(openp), float(highp), float(lowp), float(closep)])
    return ohlc


def calculate_indicators(dataframe):
    print(print_flag + 'Compute basic indicators...')

    # Get MACD
    dataframe["macd"], dataframe["macd_indicator"], dataframe["macd_hist"] = talib.MACD(dataframe['close'])
    dataframe["macd_hist_gradient"] = np.nan
    for i in range(1, len(dataframe)):
        try:
            dataframe.at[dataframe.index[i], "macd_hist_gradient"] = dataframe.at[dataframe.indexTickerList[i - 1], "macd_hist"] - dataframe.at[dataframe.indexTickerList[i], "macd_hist"]
        except IndexError:
            pass

    # SMAs:
    dataframe["ma8"] = talib.MA(dataframe["close"], timeperiod=8)
    dataframe["ema10"] = talib.EMA(dataframe["close"], timeperiod=10)
    dataframe["ma10"] = talib.MA(dataframe["close"], timeperiod=10)
    dataframe["ma20"] = talib.MA(dataframe["close"], timeperiod=20)
    dataframe["ma30"] = talib.MA(dataframe["close"], timeperiod=30)
    dataframe["ma50"] = talib.MA(dataframe["close"], timeperiod=50)
    dataframe["ma100"] = talib.MA(dataframe["close"], timeperiod=100)
    dataframe["ma200"] = talib.MA(dataframe["close"], timeperiod=200)

    # EMAs:
    dataframe["ema100"] = talib.EMA(dataframe["close"], timeperiod=100)
    dataframe["ema133"] = talib.EMA(dataframe["close"], timeperiod=133)
    dataframe["ema166"] = talib.EMA(dataframe["close"], timeperiod=166)
    dataframe["ema200"] = talib.EMA(dataframe["close"], timeperiod=200)

    # Get RSI
    dataframe["rsi"] = talib.RSI(dataframe["close"], timeperiod=14)
    #dataframe["rsi_smoothed"] = talib.EMA(dataframe["rsi"], timeperiod=2)
    # Get RSI MA:
    dataframe["rsi_sig_line"] = talib.MA(dataframe["rsi"], timeperiod=20)
    # Get Bollinger Bands:
    dataframe["upper_rsi_bollinger"], dataframe["middle_rsi_bollinger"], dataframe["lower_rsi_bollinger"] = talib.BBANDS(dataframe["rsi"], timeperiod=30, matype=MA_Type.T3)
    # Get MFI, Money Flow Index
    dataframe['mfi'] = talib.MFI(dataframe["high"], dataframe["low"], dataframe["close"], dataframe["volume"], timeperiod=14)

    # Get STC, (Schaff Trend Cycle (sensitive trendindicator))
    ohlc = dataframe.filter(items=['open', 'high', 'low', 'close']).astype('float')
    dataframe['stc'] = TA.STC(ohlc)

    # get Momentum indicator:
    # dataframe['mom'] = talib.MOM(dataframe["close"], timeperiod=10)
    dataframe['willR_14'] = talib.WILLR(dataframe["high"], dataframe["low"], dataframe["close"], timeperiod=14) +100
    dataframe['willR_20'] = talib.WILLR(dataframe["high"], dataframe["low"], dataframe["close"], timeperiod=20) +100
    #dataframe['willR_14'] = np.where(dataframe['willR_14'] > 50, np.NaN, dataframe['willR_14'])
    #dataframe['willR_20'] = np.where(dataframe['willR_20'] > 50, np.NaN, dataframe['willR_20'])

    return dataframe
