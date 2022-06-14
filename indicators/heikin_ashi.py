import pandas as pd


def heikin_ashi(df):
    df = df.astype(float)
    # ohlc
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close'])
    heikin_ashi_df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4

    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 2] = df['Open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 2] = (heikin_ashi_df.iat[i - 1, 2] + heikin_ashi_df.iat[i - 1, 3]) / 2

    heikin_ashi_df['High'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['High']).max(axis=1)
    heikin_ashi_df['Low'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['Low']).min(axis=1)
    heikin_ashi_df['Volume'] = df['Volume']
    heikin_ashi_df['Adj Close'] = df['Adj Close']

    return heikin_ashi_df