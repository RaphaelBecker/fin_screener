from dataclasses import dataclass
from dataclass_csv import DataclassReader, DataclassWriter, dateformat, accept_whitespaces
from datetime import datetime
import streamlit as st
from PIL import Image
import pathlib

st.write("# This is your Trading-Journal")

st.sidebar.success("Success rate: 65%. OK")


@dataclass
@dateformat('%d/%m/%Y')
class Trade:
    ticker: str
    entry_date: datetime
    entry_price: str
    entry_rule: str
    entry_strategy: str
    exit_date: datetime
    exit_price:str
    exit_rule: str
    exit_strategy: str
    haikin_ashi: bool
    close_at_supp: bool
    bull_div: bool
    tdi: bool
    bb_squeeze: bool
    target_gain: str
    gain: str
    tax: str
    fees: str


def load_trades_from_csv() -> [Trade]:
    trades_from_csv = [Trade]
    filepath = pathlib.Path().resolve().joinpath('trades.csv')
    with open(filepath) as trades_csv:
        trade_reader = DataclassReader(trades_csv, Trade)
        for trade in trade_reader:
            trades_from_csv.append(trade)
    return trades_from_csv


#trades = load_trades_from_csv()


def save_trades_to_csv(trades_to_save: [Trade]):
    filepath = pathlib.Path().resolve().joinpath('trades.csv')
    with open(filepath, 'w') as trades_csv:
        w = DataclassWriter(trades_csv, trades_to_save, Trade)
        w.write()


def remove_trade_from_csv(trade: Trade, trades: [Trade]):
    pass


def get_trade_table_str(trade: Trade) -> str:
    string = (
    f"""
    | ticker   | {trade.ticker} |  
    |----------|:-------------:|
    | entry_date |  {trade.entry_date} |
    | entry_price |    {trade.entry_price}   |   
    | entry_rule |  {trade.entry_rule} |   
    | entry_strategy  | {trade.entry_strategy}  | 
    | exit_date  | {trade.exit_date}  | 
    | exit_price  | {trade.exit_price}  | 
    | exit_rule  | {trade.exit_rule}  | 
    | exit_strategy  | {trade.exit_strategy}  | 
    | haikin_ashi  | {trade.haikin_ashi}  | 
    | close_at_supp  | {trade.close_at_supp}  | 
    | bull_div  | {trade.bull_div}  | 
    | tdi  | {trade.tdi}  | 
    | bb_squeeze  | {trade.bb_squeeze}  | 
    | target_gain  | {trade.target_gain}  | 
    | gain  | {trade.gain}  | 
    | tax  | {trade.tax}  | 
    | fees  | {trade.fees}  | 
    """
    )
    return string


# Set up sections of web page
header = st.container()
checklist_and_create = st.container()
journal_list = st.container()

with checklist_and_create:
    with st.expander("Trading Checklist"):
        if st.checkbox('Is the market in a trading range or trending?'):
            if st.checkbox('Is a support or resistance level nearby?'):
                if st.checkbox('Is the price action confirmed by indicators?'):
                    if st.checkbox('What is my risk and reward ratio?'):
                        if st.checkbox('How much captial am I risking?'):
                            if st.checkbox('Are there any significant economical releases?'):
                                if st.checkbox('What is my exit strategy?'):
                                    if st.checkbox('Am I following my trading plan?'):
                                        st.button('create trading journal entry')

#with journal_list:
#    for trade in trades:
 #       st.markdown(get_trade_table_str(trade))

        #image = Image.open('mocks/example_trade.png')
        #st.image(image, caption='Apple trade 0')
