import streamlit as st


st.write("# This is the market screener")

# Set up sections of web page
header = st.container()
screen_settings = st.container()
result_list = st.container()

st.sidebar.markdown("# Market Screener")
st.sidebar.selectbox('Select index', sorted(['SMP500', 'DAX']), index=0)

with header:
    with st.expander("How does it worK?"):
        st.markdown(
        """
        1. Set up the screener settings
        2. screen the market
        """
        )

with screen_settings:
    with st.expander("Fundamental options"):
        col1, col2, col3 = st.columns(3)

        with col1:
            p_e = st.selectbox('P/E',
                ('select', 'ROdI', 'PEdG'))

        with col2:
            p_b = st.selectbox('P/B',
                ('select', 'R<OI', 'PvEG'))

        with col3:
            sales_grwth = st.selectbox('Sales growth',
                ('select', 'RwxOI', 'PEcwG'))

    with st.expander("Technical options"):
        col1, col2, col3 = st.columns(3)

        with col1:
            candle_stick_pattern = st.selectbox('Candlestick pattern',
                ('select', 'hammer', 'etc'))

        with col2:
            ema_price = st.selectbox('Bukowski pattern',
                ('select', 'swan', 'etc'))

        with col3:
            sma_price = st.selectbox('SMA-Price',
                ('select', 'SMA<price', 'etc'))


with result_list:
    st.button('search market')
    st.write("# This is the result list")


fundamental_values='''
P/E	
Forward P/E	
PEG	
P/S	
P/B	
Price/Cash	
Price/Free Cash Flow	
EPS growth
Sales growth
Return on Assets	
Return on Equity	
Return on Investment	
Current Ratio	
Quick Ratio	
LT Debt/Equity	
Debt/Equity	
Gross Margin	
Operating Margin	
Net Profit Margin	
Payout Ratio	
Insider Ownership	
Insider Transactions	
Institutional Ownership	
'''
