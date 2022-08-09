import logging
from dateutil import parser
from constants import *
from enums import TradeMode, OHLC


class Orders():
    def __init__(self, trade_state, settings):
        self.trade_state = trade_state
        self.settings = settings
        logging.basicConfig(level=logging.DEBUG)

    def trade(self, order_type=TradeMode.BUY):
        current_close_price = float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.CLOSEINDEX.value])
        self.trade_state.order_prices.append(current_close_price)
        buy_sell_position_size = self.settings.position_size if order_type==TradeMode.BUY else self.settings.position_size*-1
        if self.trade_state.average_price:
            self.trade_state.average_price = (self.trade_state.average_price*self.trade_state.position_size + current_close_price*buy_sell_position_size) \
                                            / (self.trade_state.position_size+buy_sell_position_size)
        else:
            self.trade_state.average_price = current_close_price
            self.trade_state.stop_loss_price = self.trade_state.average_price - TRADE_RISK_PIPS * 0.0001

        self.trade_state.position_size += buy_sell_position_size
        self.trade_state.candle_number = self.settings.last_candle
        if self.trade_state.position_size > 0:
            self.trade_state.trade_mode = TradeMode.BUY
        else:
            self.trade_state.trade_mode = TradeMode.SELL
        if self.trade_state.position_size == 0:
            self.close(current_close_price)

    def close(self, close_price=None):
        if self.trade_state.trade_mode != TradeMode.CLOSED:
            self.settings.history.append([
                self.trade_state.candle_number,
                self.trade_state.average_price,
                self.settings.last_candle,
                close_price or self.settings.bid[self.settings.last_candle].split(
                    ',')[OHLC.CLOSEINDEX.value],
                self.trade_state.trade_mode.value
            ])
            self.trade_state.trade_mode = TradeMode.CLOSED
            self.trade_state.equity += self.trade_state.profit
            self.trade_state.profit = 0
            self.trade_state.order_prices = []
            self.trade_state.position_size = 0
            self.trade_state.stop_loss_price = 0
            self.trade_state.pips = 0
            self.trade_state.average_price = 0

    def check_orders(self):
        current_close_price = float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.CLOSEINDEX.value])
        current_high_price = float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.HIGHINDEX.value])
        current_low_price = float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.LOWINDEX.value])
        if (self.trade_state.trade_mode == TradeMode.BUY):
            self.trade_state.pips = 1 + (current_close_price - self.trade_state.average_price) * 10000
            self.trade_state.profit = self.trade_state.pips * \
                abs(self.trade_state.position_size)
            if current_low_price <= self.trade_state.stop_loss_price:
                logging.debug('close buy check')
                self.close(self.trade_state.stop_loss_price)

        if (self.trade_state.trade_mode == TradeMode.SELL):
            self.trade_state.pips = 1 + (self.trade_state.average_price - current_close_price) * 10000
            self.trade_state.profit = self.trade_state.pips * \
                abs(self.trade_state.position_size)
            if current_high_price >= self.trade_state.stop_loss_price:
                logging.debug('close sell check')
                self.close(self.trade_state.stop_loss_price)
