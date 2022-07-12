from enums import TradeMode, OHLC

class TradeState:
    """"Keeps track of the current state"""
    def __init__(self):
        self.equity = 100
        self.profit = 0
        self.trade_mode = TradeMode.CLOSED
        self.order_price = 0
        self.position_size = 0
        self.stop_loss_price = 0
        self.pips = 0
        self.candle_number = 0
