import streamlit as st


st.write("# This is the market screener")

# Set up sections of web page
header = st.container()
screen_settings = st.container()
result_list = st.container()

with header:
    with st.expander("How does it worK?"):
        st.markdown(
        """
        1. Set up the screener settings
        2. screen the market
        """
        )

with screen_settings:
    col1, col2, col3 = st.columns(3)

    with col1:
        option1 = st.selectbox(
            'technical indaicator A',
            ('EBIdTDA', 'ROdI', 'PEdG'))
        option2 = st.selectbox(
            'technical indaicator A',
            ('EByITDA', 'RbOI', 'PvEG'))
        option3 = st.selectbox(
            'technical indaicator A',
            ('EBsITDA', 'RfOI', 'PzEG'))
        option4 = st.selectbox(
            'technical indaicator A',
            ('EBITDA', 'ROI', 'PEG'))

    with col2:
        option1 = st.selectbox(
            'technical indaicator A',
            ('EBITsdDA', 'R<OI', 'PvEG'))
        option2 = st.selectbox(
            'technical indaicator A',
            ('EBIThgDA', 'RhOI', 'PEjG'))
        option3 = st.selectbox(
            'technical indaicator A',
            ('EBITzm,DA', 'RO,kjI', 'PEGj,'))
        option4 = st.selectbox(
            'technical indaicator A',
            ('EBITDA', 'RbgOI', 'PEgG'))

    with col3:
        option1 = st.selectbox(
            'technical indaicator A',
            ('EBIqTDA', 'RwxOI', 'PEcwG'))
        option2 = st.selectbox(
            'technical indaicator A',
            ('EBwcITDA', 'RcOI', 'PEwG'))
        option3 = st.selectbox(
            'technical indaicator A',
            ('EBIcTDA', 'ROyxI', 'PEGx'))
        option4 = st.selectbox(
            'technical indaicator A',
            ('EBIyxcTDA', 'ROyxcI', 'PExG'))



with result_list:
    st.button('search market')
    st.write("# This is the result list")