from enums import TradeMode, OHLC
from load_data import load_ticks, load_minutes
from constants import *
from dateutil import parser

class TradeState:
    """"Keeps track of the current state"""
    def __init__(self, date_time, equity):
        self.done = False
        self.date_time = parser.parse(date_time)
        self.equity = equity
        self.profit = 0
        self.trade_mode = TradeMode.CLOSED
        self.order_prices = []
        self.average_price = 0
        self.position_size = 0
        self.stop_loss_price = 0
        self.pips = 0
        self.time_frame = 1
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

        self.tick_data = load_ticks(self.date_time)
        self.tick_index = 0
        self.one_minute_data = load_minutes(self.date_time)
        self.one_minute_index = 0

    def find_current_date_time_index(self, date_time, data_stream):
        index = len(data_stream)
        last_index = 0
        differential = index//2
        index = 0
        while differential > 10000:
            last_index = index
            line_date_time = parser.parse(data_stream[index+differential].split(';', 1)[0])
            if date_time > line_date_time:
                index = differential + differential//2
            elif date_time < line_date_time:
                index = differential - differential//2
            print(index)

        print(index)
        # for i, line in enumerate(data_stream, start=index):
        #     line_date_time = parser.parse(line.split(';', 1)[0])
        #     # print(i-index)
        #     if line_date_time >= date_time:
        #         return i-index

    def manage(self):
        pass


datetime = '2015-05-03 000000'
state = TradeState(datetime, 50)
datetime = parser.parse(datetime)
# tick_line = state.find_current_date_time_index(datetime, state.tick_data)
# print(tick_line)
# print(state.tick_data[tick_line])
minute_line = state.find_current_date_time_index(datetime, state.one_minute_data)
# print(minute_line)
# print(state.one_minute_data[minute_line])