import datetime
import unittest

import numpy as np
import data.db_connector as database
import volume_profile.vol_profile as vol_profile
from plotly.subplots import make_subplots
import plotly.graph_objects as go


class TestVolProfile(unittest.TestCase):

    def test_get_vol_axes(self):
        # Set start and end point to fetch data:
        start_date = datetime.datetime(2021, 8, 1)
        end_date = datetime.datetime.now().date()
        ticker = "A"

        # Fetch data from database
        df_ticker = database.get_hlocv_from_db(ticker, start_date, end_date)
        print(df_ticker)

        closes = df_ticker['close']
        volumes = df_ticker['volume']
        lower = closes.min()
        upper = closes.max()
        closes_ax = np.linspace(lower, upper, num=20)
        vol_ax = vol_profile.get_vol_axes(closes, volumes, closes_ax)

        print(closes_ax)
        print(vol_ax)

        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.2, 0.8],
            specs=[[{}, {}]],
            horizontal_spacing=0.01)

        fig.add_trace(
            go.Bar(
                x=vol_ax,
                y=closes_ax,
                text=np.around(closes_ax, 2),
                textposition='auto',
                orientation='h'
            ),

            row=1, col=1
        )

        dateStr = df_ticker.index.strftime("%d-%m-%Y %H:%M:%S")

        fig.add_trace(
            go.Candlestick(x=dateStr,
                           open=df_ticker['open'],
                           high=df_ticker['high'],
                           low=df_ticker['low'],
                           close=df_ticker['close'],
                           yaxis="y2"

                           ),

            row=1, col=2
        )

        fig.update_layout(
            title_text='Market Profile Chart (US S&P 500)',  # title of plot
            bargap=0.01,  # gap between bars of adjacent location coordinates,
            showlegend=False,

            xaxis=dict(
                showticklabels=False
            ),
            yaxis=dict(
                showticklabels=False
            ),

            yaxis2=dict(
                title="Price (USD)",
                side="right"

            )

        )

        fig.update_yaxes(nticks=20)
        fig.update_yaxes(side="right")
        fig.update_layout(height=800)

        config = {
            'modeBarButtonsToAdd': ['drawline']
        }

        fig.show()