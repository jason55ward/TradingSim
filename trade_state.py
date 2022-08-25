from enums import TradeMode, OHLC

class TradeState:
    """"Keeps track of the current state"""
    def __init__(self):
        self.done = False
        self.equity = 100
        self.profit = 0
        self.trade_mode = TradeMode.CLOSED
        self.order_prices = []
        self.average_price = 0
        self.position_size = 0
        self.stop_loss_price = 0
        self.pips = 0
        self.date_time = date_time
        self.time_frame = 1
        self.date_time = None
        self.tick_data = []
        self.tick_index = None
        self.one_minute_data = []
        self.one_minute_index = None
        self.five_minute_data = []
        self.five_minute_index = None
        self.fifteen_minute_data = []
        self.fifteen_minute_index = None
        self.one_hour_data = []
        self.one_hour_index = None
        self.four_hour_data = []
        self.four_hour_index = None
        self.daily_data = []
        self.daily_index = None
        self.support = []
        self.history = []
