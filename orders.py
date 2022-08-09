import logging
from dateutil import parser
from constants import *
from enums import TradeMode, OHLC


class Orders():
    def __init__(self, trade_state, settings):
        self.trade_state = trade_state
        self.settings = settings
        logging.basicConfig(level=logging.DEBUG)


    def buy(self):
        if self.trade_state.trade_mode == TradeMode.SELL:
            return
        current_close_price = float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.CLOSEINDEX.value])
        if self.trade_state.order_price:
            self.trade_state.order_price = (self.trade_state.order_price*self.trade_state.position_size + current_close_price*self.settings.position_size) \
                                            / (self.trade_state.position_size+self.settings.position_size)
        else:
            self.trade_state.order_price = current_close_price
        self.trade_state.stop_loss_price = self.trade_state.order_price - TRADE_RISK_PIPS * 0.0001
        self.trade_state.position_size += self.settings.position_size
        self.trade_state.candle_number = self.settings.last_candle
        if self.trade_state.position_size > 0:
            self.trade_state.trade_mode = TradeMode.BUY
        else:
            self.trade_state.trade_mode = TradeMode.SELL
        if self.trade_state.position_size == 0:
            logging.debug('buy neutral close')
            self.close(self.trade_state.order_price)

    def sell(self):
        if self.trade_state.trade_mode == TradeMode.BUY:
            return
        current_close_price = float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.CLOSEINDEX.value])
        if self.trade_state.order_price:
            self.trade_state.order_price = (self.trade_state.order_price*self.trade_state.position_size + current_close_price*self.settings.position_size*-1) \
                                            / (self.trade_state.position_size+self.settings.position_size*-1)
        else:
            self.trade_state.order_price = current_close_price
        
        self.trade_state.stop_loss_price = self.trade_state.order_price + TRADE_RISK_PIPS * 0.0001
        self.trade_state.position_size += self.settings.position_size*-1
        self.trade_state.candle_number = self.settings.last_candle
        if self.trade_state.position_size > 0:
            self.trade_state.trade_mode = TradeMode.BUY
        else:
            self.trade_state.trade_mode = TradeMode.SELL
        if self.trade_state.position_size == 0:
            logging.debug('sell neutral close')
            self.close(self.trade_state.order_price)

    def close(self, close_price=None):
        if self.trade_state.trade_mode != TradeMode.CLOSED:
            self.settings.history.append([
                self.trade_state.candle_number,
                self.trade_state.order_price,
                self.settings.last_candle,
                close_price or self.settings.bid[self.settings.last_candle].split(
                    ',')[OHLC.CLOSEINDEX.value],
                self.trade_state.trade_mode.value
            ])
            self.trade_state.trade_mode = TradeMode.CLOSED
            self.trade_state.equity += self.trade_state.profit
            self.trade_state.profit = 0
            self.trade_state.order_price = 0
            self.trade_state.position_size = 0
            self.trade_state.stop_loss_price = 0
            self.trade_state.pips = 0

    def check_orders(self):
        if (self.trade_state.trade_mode == TradeMode.BUY):
            self.trade_state.pips = 1 + (float(self.settings.bid[self.settings.last_candle].split(
                ',')[OHLC.CLOSEINDEX.value]) - self.trade_state.order_price) * 10000
            self.trade_state.profit = self.trade_state.pips * \
                abs(self.trade_state.position_size)
            if float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.LOWINDEX.value]) <= self.trade_state.stop_loss_price:
                logging.debug('close buy check')
                self.close(self.trade_state.stop_loss_price)

        if (self.trade_state.trade_mode == TradeMode.SELL):
            self.trade_state.pips = 1 + (self.trade_state.order_price - float(
                self.settings.bid[self.settings.last_candle].split(',')[OHLC.CLOSEINDEX.value])) * 10000
            self.trade_state.profit = self.trade_state.pips * \
                abs(self.trade_state.position_size)
            if float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.HIGHINDEX.value]) >= self.trade_state.stop_loss_price:
                logging.debug('close sell check')
                self.close(self.trade_state.stop_loss_price)
