import altair as alt
import streamlit as st
import pandas as pd

data_set = {
    'countries': ['India', 'Australia', 'Japan', 'America', 'Russia'],
    'values': [4500, 2500, 1053, 500, 3200]
}

df = pd.DataFrame(data_set)

line = alt.Chart(df).mark_line().encode(
    x = 'countries',
    y = 'values'
)

st.altair_chart(line.interactive(), use_container_width=True)