import streamlit as st
from page.layout import Layout

# Page Configuration
app_name = 'fin_screener'

st.set_page_config(
    page_title=app_name,
    layout="wide",
    initial_sidebar_state="expanded",
)

layout = Layout(app_name)
