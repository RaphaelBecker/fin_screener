import streamlit as st
import datetime
from indicators.support_resistance import find_support_and_resistance_lines

from chart.chart import Chart
import data.db_connector as database
from data import helpers
from data import dataset

st.markdown("# Analyse assets")
st.sidebar.markdown("# Analyse assets")

# Select market:
stock_index_selector = st.sidebar.selectbox('Select index', sorted(dataset.market_index_list), index=0)

# Select ticker from choosen market:
tickers = dataset.get_tickers(stock_index_selector)
ticker_selector = None
if isinstance(tickers, list):
    ticker_selector = st.sidebar.selectbox('Select ticker', sorted(tickers), index=0)
elif isinstance(tickers, dict):
    ticker_selector = st.sidebar.selectbox('Select ticker', sorted(tickers.keys()), index=0)

# Set start and end point to fetch data:
start_date = st.sidebar.date_input('Start date', datetime.datetime(2021, 8, 1))
end_date = st.sidebar.date_input('End date', datetime.datetime.now().date())

# Fetch data from database
df_ticker = database.get_hlocv_from_db(ticker_selector, start_date, end_date)

# title of ticker:
if isinstance(tickers, list):
    st.header(f'{ticker_selector},  last: {df_ticker.tail(1).index.item().date()}')
elif isinstance(tickers, dict):
    st.header(f'[{ticker_selector}] {tickers[ticker_selector]}, last: {df_ticker.tail(1).index.item().date()}')


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(df_ticker)

chart = Chart(ticker_selector, df_ticker)

# Render plot using plotly_chart
st.plotly_chart(chart.fig)


# NEWS Feed:

# Import libraries
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Parameters
n = 5  # the # of article headlines displayed per ticker
tickers = [ticker_selector]

# Get Data
finwiz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}

if st.checkbox("Show News Sentiment Analysis:"):
    for ticker in tickers:
        url = finwiz_url + ticker
        req = Request(url=url, headers={'user-agent': 'Mozilla/5.0'})
        resp = urlopen(req)
        html = BeautifulSoup(resp, features="lxml")
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table


    # Iterate through the news
    parsed_news = []
    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text()
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]

            else:
                date = date_scrape[0]
                time = date_scrape[1]

            ticker = file_name.split('_')[0]

            parsed_news.append([ticker, date, time, text])

    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()

    columns = ['Ticker', 'Date', 'Time', 'Headline']
    news = pd.DataFrame(parsed_news, columns=columns)
    scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

    df_scores = pd.DataFrame(scores)
    news = news.join(df_scores, rsuffix='_right')

    # View Data
    news['Date'] = pd.to_datetime(news.Date).dt.date

    unique_ticker = news['Ticker'].unique().tolist()
    news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

    values = []
    for ticker in tickers:
        dataframe = news_dict[ticker]
        dataframe = dataframe.set_index('Ticker')
        dataframe = dataframe.drop(columns=['Headline'])
        st.write('\n')
        dataframe = dataframe.set_index("Date")
        table_dataframe = dataframe
        dataframe["zero"] = 0
        st.line_chart(dataframe[["compound", "zero"]])
        if st.checkbox("show raw"):
            st.table(table_dataframe.head())

        mean = round(dataframe['compound'].mean(), 2)
        values.append(mean)

    df = pd.DataFrame(list(zip(tickers, values)), columns=['Ticker', 'Mean Sentiment'])
    df = df.set_index('Ticker')
    df = df.sort_values('Mean Sentiment', ascending=False)
    col1, col2 = st.columns([4,1])
    col2.metric(label="Mean sentiment", value=str(df["Mean Sentiment"].values), delta="")

    try:
        for ticker in tickers:
            df = news_tables[ticker]
            df_tr = df.findAll('tr')

            col1.subheader('Recent News Headlines for {}: '.format(ticker))

            headlines = []
            for i, table_row in enumerate(df_tr):
                a_text = table_row.a.text
                td_text = table_row.td.text
                td_text = td_text.strip()
                headlines.append(f" *  {a_text} ({td_text})")
                if i == n - 1:
                    break
            for line in headlines:
                col1.write(line)
    except KeyError:
        pass