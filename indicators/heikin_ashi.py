import pandas as pd


def heikin_ashi(df):
    df = df.astype(float)
    # ohlc
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['high', 'low', 'open', 'close', 'volume', 'adj close'])
    heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 2] = df['open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 2] = (heikin_ashi_df.iat[i - 1, 2] + heikin_ashi_df.iat[i - 1, 3]) / 2

    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)
    heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)
    heikin_ashi_df['volume'] = df['volume']
    heikin_ashi_df['adj close'] = df['adj close']

    return heikin_ashi_df