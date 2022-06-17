# source: https://medium.datadriveninvestor.com/how-to-detect-support-resistance-levels-and-breakout-using-python-f8b5dac42f21

import numpy as np


def is_support(df, i):
    support = df['Low'][i] < df['Close'][i - 1] < df['Close'][i - 2] < df['Close'][i - 3] and df['Low'][i] < df['Close'][i + 1] < \
              df['Close'][i + 2] < df['Close'][i + 3]
    return support


def is_resistance(df, i):
    resistance = df['High'][i] > df['Close'][i - 1] > df['Close'][i - 2] > df['Close'][i - 3]  and df['High'][i] > df['Close'][i + 1] > \
                 df['Close'][i + 2] > df['Close'][i + 3]
    return resistance


def is_far_from_level(l, levels, s):
    # print(print_flag + '   l: ' + str(type(l)) + ' ' + str(l))
    # print(print_flag + '   levels: ' + str(type(levels)) + ' ' + str(levels))
    # print(print_flag + '   s: ' + str(type(s)) + ' ' + str(s))
    return np.sum([abs(float(l) - float(x[1])) < s for x in levels]) == 0


def find_support_and_resistance_lines(dataframe):
    dataframe['supp_res_levels'] = np.nan
    s = np.mean(dataframe['High'].astype('float') - (dataframe['Low'].astype('float')))
    levels = []
    start_levels = []

    for i in range(2, dataframe.shape[0] - 2):
        if is_support(dataframe, i):
            l = dataframe['Low'][i]
            if is_far_from_level(l, levels, s):
                dataframe.at[dataframe.index[i], 'supp_res_levels'] = l
                levels.append((i, dataframe['Low'][i]))
                start_levels.append((i, dataframe.index[i]))
        elif is_resistance(dataframe, i):
            l = dataframe['High'][i]
            if is_far_from_level(l, levels, s):
                dataframe.at[dataframe.index[i], 'supp_res_levels'] = l
                levels.append((i, dataframe['High'][i]))
                start_levels.append((i, dataframe.index[i]))

    return dataframe, levels, start_levels