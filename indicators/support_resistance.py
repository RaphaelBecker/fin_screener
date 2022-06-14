import numpy as np


def is_support(df, i):
    support = df['low'][i] < df['close'][i - 1] < df['close'][i - 2] and df['low'][i] < df['close'][i + 1] < \
              df['close'][i + 2]
    return support


def is_resistance(df, i):
    resistance = df['high'][i] > df['close'][i - 1] > df['close'][i - 2] and df['high'][i] > df['close'][i + 1] > \
                 df['close'][i + 2]
    return resistance


def is_far_from_level(l, levels, s):
    # print(print_flag + '   l: ' + str(type(l)) + ' ' + str(l))
    # print(print_flag + '   levels: ' + str(type(levels)) + ' ' + str(levels))
    # print(print_flag + '   s: ' + str(type(s)) + ' ' + str(s))
    return np.sum([abs(float(l) - float(x[1])) < s for x in levels]) == 0


def find_support_and_resistance_lines(data):
    data['supp_res_levels'] = np.nan
    s = np.mean(data['High'].astype('float') - (data['Low'].astype('float')))
    levels = []
    start_levels = []

    for i in range(2, data.shape[0] - 2):
        if is_support(data, i):
            l = data['Low'][i]
            if is_far_from_level(l, levels, s):
                data.at[data.index[i], 'supp_res_levels'] = l
                levels.append((i, data['Low'][i]))
                start_levels.append((i, data.index[i]))
        elif is_resistance(data, i):
            l = data['High'][i]
            if is_far_from_level(l, levels, s):
                data.at[data.index[i], 'supp_res_levels'] = l
                levels.append((i, data['High'][i]))
                start_levels.append((i, data.index[i]))

    return data, levels, start_levels