# source: https://medium.datadriveninvestor.com/how-to-detect-support-resistance-levels-and-breakout-using-python-f8b5dac42f21

import numpy as np


def is_support(df, i):
    support = False
    try:
        support = df['low'][i] < df['close'][i - 1] < df['close'][i - 2] < df['close'][i - 3] and df['low'][i] < df['close'][i + 1] < \
                  df['close'][i + 2] < df['close'][i + 3]
    except IndexError:
        pass
    return support


def is_resistance(df, i):
    resistance = False
    try:
        resistance = df['high'][i] > df['close'][i - 1] > df['close'][i - 2] > df['close'][i - 3]  and df['high'][i] > df['close'][i + 1] > \
                     df['close'][i + 2] > df['close'][i + 3]
    except IndexError:
        pass
    return resistance


def is_far_from_level(l, levels, s):
    # print(print_flag + '   l: ' + str(type(l)) + ' ' + str(l))
    # print(print_flag + '   levels: ' + str(type(levels)) + ' ' + str(levels))
    # print(print_flag + '   s: ' + str(type(s)) + ' ' + str(s))
    return np.sum([abs(float(l) - float(x[1])) < s for x in levels]) == 0


def find_support_and_resistance_lines(dataframe):
    dataframe['supp_res_levels'] = np.nan
    s = np.mean(dataframe['high'].astype('float') - (dataframe['low'].astype('float')))
    levels = []
    start_levels = []

    for i in range(2, dataframe.shape[0] - 2):
        if is_support(dataframe, i):
            l = dataframe['low'][i]
            if is_far_from_level(l, levels, s):
                dataframe.at[dataframe.index[i], 'supp_res_levels'] = l
                levels.append((i, dataframe['low'][i]))
                start_levels.append((i, dataframe.index[i]))
        elif is_resistance(dataframe, i):
            l = dataframe['high'][i]
            if is_far_from_level(l, levels, s):
                dataframe.at[dataframe.index[i], 'supp_res_levels'] = l
                levels.append((i, dataframe['high'][i]))
                start_levels.append((i, dataframe.index[i]))

    return dataframe, levels, start_levels