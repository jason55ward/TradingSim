import logging, os, sys
from dateutil import parser
from constants import *
from enums import TradeMode, OHLC

class Orders():
    def __init__(self, state, settings):
        self.state = state
        self.settings = settings
        logging.basicConfig(level=logging.DEBUG)

    def trade(self, order_type=TradeMode.BUY):
        current_close_price = float(self.state.minute_data[self.state.minute_index].split(DATA_DELIMITER)[OHLC.CLOSEINDEX.value])
        self.state.order_prices.append(current_close_price)
        buy_or_sell = 1 if order_type==TradeMode.BUY else -1
        if self.state.average_price:
            if (self.state.position_size+self.settings.default_position_size*buy_or_sell) == 0:
                self.state.average_price = 0
            else:
                self.state.average_price = (self.state.average_price*self.state.position_size + current_close_price*self.settings.default_position_size*buy_or_sell) \
                                            / (self.state.position_size+self.settings.default_position_size*buy_or_sell)
        else:
            self.state.average_price = current_close_price
            self.state.stop_loss_price = self.state.average_price - (TRADE_RISK_PIPS * 0.0001)*buy_or_sell

        self.state.position_size += self.settings.default_position_size*buy_or_sell
        if self.state.position_size > 0:
            self.state.trade_mode = TradeMode.BUY
        else:
            self.state.trade_mode = TradeMode.SELL
        if self.state.position_size == 0:
            self.close(current_close_price)

    def close(self, close_price=None):
        if self.state.trade_mode != TradeMode.CLOSED:
            # self.state.history.append([
            #     self.state.candle_number,
            #     self.state.average_price,
            #     self.state.data_index,
            #     close_price or self.state.data[self.state.data_index].split(
            #         ',')[OHLC.CLOSEINDEX.value],
            #     self.state.trade_mode.value
            # ])
            self.state.trade_mode = TradeMode.CLOSED
            self.state.equity += self.state.profit
            self.state.profit = 0
            self.state.order_prices = []
            self.state.position_size = 0
            self.state.stop_loss_price = 0
            self.state.pips = 0
            self.state.average_price = 0

    def check_orders(self):
        try:
            current_close_price = float(self.state.minute_data[self.state.minute_index].split(DATA_DELIMITER)[OHLC.CLOSEINDEX.value])
            current_high_price = float(self.state.minute_data[self.state.minute_index].split(DATA_DELIMITER)[OHLC.HIGHINDEX.value])
            current_low_price = float(self.state.minute_data[self.state.minute_index].split(DATA_DELIMITER)[OHLC.LOWINDEX.value])
            if (self.state.trade_mode == TradeMode.BUY):
                self.state.pips = (current_close_price - self.state.average_price) * 10000-1
                self.state.profit = self.state.pips * abs(self.state.position_size)
                if current_low_price <= self.state.stop_loss_price:
                    logging.debug('close buy check')
                    self.close(self.state.stop_loss_price)

            if (self.state.trade_mode == TradeMode.SELL):
                self.state.pips = (self.state.average_price - current_close_price) * 10000-1
                self.state.profit = self.state.pips * abs(self.state.position_size)
                if current_high_price >= self.state.stop_loss_price:
                    logging.debug('close sell check')
                    self.close(self.state.stop_loss_price)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(sys.exc_info())
