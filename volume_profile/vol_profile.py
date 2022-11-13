# source: https://github.com/teobeeguan/market_profile/blob/main/MarketProfileAppDemo.py
import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


# stock = yf.Ticker(ticker)
# history_data = stock.history(interval = i, period = str(p) + "d")

def get_vol_axes(ticker_closes, ticker_volumes, closes_ax):
    """

    :param ticker_closes: timeseries of close prices of a ticker
    :param ticker_volumes: timeseries of volumes
    :param closes_ax: range of bars charts between min and max ticker price
    :return:
    """
    volume_ax = np.zeros(80)
    for i in range(0, len(ticker_volumes)):
        if closes_ax[0] <= ticker_closes[i] < closes_ax[1]:
            volume_ax[0] += ticker_volumes[i]

        elif closes_ax[1] <= ticker_closes[i] < closes_ax[2]:
            volume_ax[1] += ticker_volumes[i]

        elif closes_ax[2] <= ticker_closes[i] < closes_ax[3]:
            volume_ax[2] += ticker_volumes[i]

        elif closes_ax[3] <= ticker_closes[i] < closes_ax[4]:
            volume_ax[3] += ticker_volumes[i]

        elif closes_ax[4] <= ticker_closes[i] < closes_ax[5]:
            volume_ax[4] += ticker_volumes[i]

        elif closes_ax[5] <= ticker_closes[i] < closes_ax[6]:
            volume_ax[5] += ticker_volumes[i]

        elif closes_ax[6] <= ticker_closes[i] < closes_ax[7]:
            volume_ax[6] += ticker_volumes[i]

        elif closes_ax[7] <= ticker_closes[i] < closes_ax[8]:
            volume_ax[7] += ticker_volumes[i]

        elif closes_ax[8] <= ticker_closes[i] < closes_ax[9]:
            volume_ax[8] += ticker_volumes[i]

        elif closes_ax[9] <= ticker_closes[i] < closes_ax[10]:
            volume_ax[9] += ticker_volumes[i]

        elif closes_ax[10] <= ticker_closes[i] < closes_ax[11]:
            volume_ax[10] += ticker_volumes[i]

        elif closes_ax[11] <= ticker_closes[i] < closes_ax[12]:
            volume_ax[11] += ticker_volumes[i]

        elif closes_ax[12] <= ticker_closes[i] < closes_ax[13]:
            volume_ax[12] += ticker_volumes[i]

        elif closes_ax[13] <= ticker_closes[i] < closes_ax[14]:
            volume_ax[13] += ticker_volumes[i]

        elif closes_ax[14] <= ticker_closes[i] < closes_ax[15]:
            volume_ax[14] += ticker_volumes[i]

        elif closes_ax[15] <= ticker_closes[i] < closes_ax[16]:
            volume_ax[15] += ticker_volumes[i]

        elif closes_ax[16] <= ticker_closes[i] < closes_ax[17]:
            volume_ax[16] += ticker_volumes[i]

        elif closes_ax[17] <= ticker_closes[i] < closes_ax[18]:
            volume_ax[17] += ticker_volumes[i]

        elif closes_ax[18] <= ticker_closes[i] < closes_ax[19]:
            volume_ax[18] += ticker_volumes[i]
        ###
        elif closes_ax[19] <= ticker_closes[i] < closes_ax[20]:
            volume_ax[19] += ticker_volumes[i]

        elif closes_ax[20] <= ticker_closes[i] < closes_ax[21]:
            volume_ax[20] += ticker_volumes[i]

        elif closes_ax[21] <= ticker_closes[i] < closes_ax[22]:
            volume_ax[21] += ticker_volumes[i]

        elif closes_ax[22] <= ticker_closes[i] < closes_ax[23]:
            volume_ax[22] += ticker_volumes[i]

        elif closes_ax[23] <= ticker_closes[i] < closes_ax[24]:
            volume_ax[23] += ticker_volumes[i]

        elif closes_ax[24] <= ticker_closes[i] < closes_ax[25]:
            volume_ax[24] += ticker_volumes[i]

        elif closes_ax[25] <= ticker_closes[i] < closes_ax[26]:
            volume_ax[25] += ticker_volumes[i]

        elif closes_ax[26] <= ticker_closes[i] < closes_ax[27]:
            volume_ax[26] += ticker_volumes[i]

        elif closes_ax[27] <= ticker_closes[i] < closes_ax[28]:
            volume_ax[27] += ticker_volumes[i]

        elif closes_ax[28] <= ticker_closes[i] < closes_ax[29]:
            volume_ax[28] += ticker_volumes[i]

        elif closes_ax[29] <= ticker_closes[i] < closes_ax[30]:
            volume_ax[29] += ticker_volumes[i]

        elif closes_ax[30] <= ticker_closes[i] < closes_ax[31]:
            volume_ax[30] += ticker_volumes[i]

        elif closes_ax[31] <= ticker_closes[i] < closes_ax[32]:
            volume_ax[31] += ticker_volumes[i]

        elif closes_ax[32] <= ticker_closes[i] < closes_ax[33]:
            volume_ax[32] += ticker_volumes[i]

        elif closes_ax[33] <= ticker_closes[i] < closes_ax[34]:
            volume_ax[33] += ticker_volumes[i]

        elif closes_ax[34] <= ticker_closes[i] < closes_ax[35]:
            volume_ax[34] += ticker_volumes[i]

        elif closes_ax[35] <= ticker_closes[i] < closes_ax[36]:
            volume_ax[35] += ticker_volumes[i]

        elif closes_ax[37] <= ticker_closes[i] < closes_ax[38]:
            volume_ax[37] += ticker_volumes[i]

        ######
        elif closes_ax[38] <= ticker_closes[i] < closes_ax[39]:
            volume_ax[38] += ticker_volumes[i]

        elif closes_ax[39] <= ticker_closes[i] < closes_ax[40]:
            volume_ax[39] += ticker_volumes[i]

        elif closes_ax[40] <= ticker_closes[i] < closes_ax[41]:
            volume_ax[40] += ticker_volumes[i]

        elif closes_ax[41] <= ticker_closes[i] < closes_ax[42]:
            volume_ax[41] += ticker_volumes[i]

        elif closes_ax[42] <= ticker_closes[i] < closes_ax[43]:
            volume_ax[42] += ticker_volumes[i]

        elif closes_ax[43] <= ticker_closes[i] < closes_ax[44]:
            volume_ax[43] += ticker_volumes[i]

        elif closes_ax[44] <= ticker_closes[i] < closes_ax[45]:
            volume_ax[44] += ticker_volumes[i]

        elif closes_ax[45] <= ticker_closes[i] < closes_ax[46]:
            volume_ax[45] += ticker_volumes[i]

        elif closes_ax[46] <= ticker_closes[i] < closes_ax[47]:
            volume_ax[46] += ticker_volumes[i]

        elif closes_ax[47] <= ticker_closes[i] < closes_ax[48]:
            volume_ax[47] += ticker_volumes[i]

        elif closes_ax[48] <= ticker_closes[i] < closes_ax[49]:
            volume_ax[48] += ticker_volumes[i]

        elif closes_ax[49] <= ticker_closes[i] < closes_ax[50]:
            volume_ax[49] += ticker_volumes[i]

        elif closes_ax[50] <= ticker_closes[i] < closes_ax[51]:
            volume_ax[50] += ticker_volumes[i]

        elif closes_ax[51] <= ticker_closes[i] < closes_ax[52]:
            volume_ax[51] += ticker_volumes[i]

        elif closes_ax[52] <= ticker_closes[i] < closes_ax[53]:
            volume_ax[52] += ticker_volumes[i]

        elif closes_ax[53] <= ticker_closes[i] < closes_ax[54]:
            volume_ax[53] += ticker_volumes[i]

        elif closes_ax[54] <= ticker_closes[i] < closes_ax[55]:
            volume_ax[54] += ticker_volumes[i]

        elif closes_ax[55] <= ticker_closes[i] < closes_ax[56]:
            volume_ax[55] += ticker_volumes[i]

        elif closes_ax[56] <= ticker_closes[i] < closes_ax[57]:
            volume_ax[56] += ticker_volumes[i]

        elif closes_ax[57] <= ticker_closes[i] < closes_ax[58]:
            volume_ax[57] += ticker_volumes[i]

        elif closes_ax[58] <= ticker_closes[i] < closes_ax[59]:
            volume_ax[58] += ticker_volumes[i]

        ###

        elif closes_ax[59] <= ticker_closes[i] < closes_ax[60]:
            volume_ax[59] += ticker_volumes[i]

        elif closes_ax[60] <= ticker_closes[i] < closes_ax[61]:
            volume_ax[60] += ticker_volumes[i]

        elif closes_ax[61] <= ticker_closes[i] < closes_ax[62]:
            volume_ax[61] += ticker_volumes[i]

        elif closes_ax[62] <= ticker_closes[i] < closes_ax[63]:
            volume_ax[62] += ticker_volumes[i]

        elif closes_ax[63] <= ticker_closes[i] < closes_ax[64]:
            volume_ax[63] += ticker_volumes[i]

        elif closes_ax[64] <= ticker_closes[i] < closes_ax[65]:
            volume_ax[64] += ticker_volumes[i]

        elif closes_ax[65] <= ticker_closes[i] < closes_ax[66]:
            volume_ax[65] += ticker_volumes[i]

        elif closes_ax[66] <= ticker_closes[i] < closes_ax[67]:
            volume_ax[66] += ticker_volumes[i]

        elif closes_ax[67] <= ticker_closes[i] < closes_ax[68]:
            volume_ax[67] += ticker_volumes[i]

        ###

        elif closes_ax[68] <= ticker_closes[i] < closes_ax[69]:
            volume_ax[68] += ticker_volumes[i]

        elif closes_ax[69] <= ticker_closes[i] < closes_ax[70]:
            volume_ax[69] += ticker_volumes[i]

        elif closes_ax[70] <= ticker_closes[i] < closes_ax[71]:
            volume_ax[70] += ticker_volumes[i]

        elif closes_ax[71] <= ticker_closes[i] < closes_ax[72]:
            volume_ax[71] += ticker_volumes[i]

        elif closes_ax[72] <= ticker_closes[i] < closes_ax[73]:
            volume_ax[72] += ticker_volumes[i]

        elif closes_ax[73] <= ticker_closes[i] < closes_ax[74]:
            volume_ax[73] += ticker_volumes[i]

        elif closes_ax[74] <= ticker_closes[i] < closes_ax[75]:
            volume_ax[74] += ticker_volumes[i]

        elif closes_ax[75] <= ticker_closes[i] < closes_ax[76]:
            volume_ax[75] += ticker_volumes[i]

        elif closes_ax[76] <= ticker_closes[i] < closes_ax[77]:
            volume_ax[76] += ticker_volumes[i]

        elif closes_ax[77] <= ticker_closes[i] < closes_ax[78]:
            volume_ax[77] += ticker_volumes[i]

        elif closes_ax[78] <= ticker_closes[i] < closes_ax[79]:
            volume_ax[78] += ticker_volumes[i]

        else:
            volume_ax[79] += ticker_volumes[i]

    return volume_ax