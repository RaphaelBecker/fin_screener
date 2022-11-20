import datetime
from unittest import TestCase

from pages import trading_journal


class Test(TestCase):
    def test_load_trades_from_csv(self):
        trades = trading_journal.load_trades_from_csv()
        print(trades)
        for trade in trades:
            print(trade.ticker)

    def test_save_trades_to_csv(self):
        trade_a = trading_journal.Trade(
            ticker="ABC",
            entry_date="13/03/2022",
            entry_price="192",
            entry_rule="close SMA(200) AND RSI(14)<12",
            entry_strategy="MArk mInervini + TDI + Support EMA",
            exit_date="14/03/2022",
            exit_price="143",
            exit_rule="close SMA(100) AND RSI(14)<45",
            exit_strategy="Under SMA20, überkaufte Situaition ausnützen",
            haikin_ashi=True,
            close_at_supp=True,
            bull_div=True,
            tdi=True,
            bb_squeeze=True,
            target_gain="30pips",
            gain="132,2",
            tax="23",
            fees="23"
        )
        trades = [trade_a, trade_a]
        trading_journal.save_trades_to_csv(trades)

    def test_remove_trade_from_csv(self):
        self.fail()

    def test_get_trade_table_str(self):
        trade_a = trading_journal.Trade(
            ticker="ABC",
            entry_date="13/03/2022",
            entry_price="192",
            entry_rule="close SMA(200) AND RSI(14)<12",
            entry_strategy="MArk mInervini + TDI + Support EMA",
            exit_date="14/03/2022",
            exit_price="143",
            exit_rule="close SMA(100) AND RSI(14)<45",
            exit_strategy="Under SMA20, überkaufte Situaition ausnützen",
            haikin_ashi=True,
            close_at_supp=True,
            bull_div=True,
            tdi=True,
            bb_squeeze=True,
            target_gain="30pips",
            gain="132,2",
            tax="23",
            fees="23"
        )
        print(trading_journal.get_trade_table_str(trade_a))

        trades = trading_journal.load_trades_from_csv()
        for trade in trades:
            print(trading_journal.get_trade_table_str(trade))

    def test_trade(self):
        self.fail()
