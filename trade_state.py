from enums import TradeMode, OHLC
from load_data import load_ticks, load_minutes
from constants import *
from dateutil import parser
import datetime
import os

class TradeState:
    """"Keeps track of the current state"""
    def __init__(self, date_time, equity):
        self.done = False
        self.date_time = parser.parse(date_time)
        self.date_time_offset = datetime.datetime.now() - self.date_time
        self.equity = equity
        self.profit = 0
        self.trade_mode = TradeMode.CLOSED
        self.order_prices = []
        self.average_price = 0
        self.position_size = 0
        self.stop_loss_price = 0
        self.pips = 0
        self.time_frame = 1
        self.data = []
        self.data_index = None
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
        self.tick_index = self.find_current_date_time_index(self.date_time, self.tick_data)
        self.one_minute_data = load_minutes(self.date_time)
        self.one_minute_index = self.find_current_date_time_index(self.date_time, self.one_minute_data)
        self.data = self.one_minute_data
        self.data_index = self.one_minute_index

    def find_current_date_time_index(self, date_time, data_stream):
        index = 0
        increment = len(data_stream)//50
        while index < len(data_stream):
            line_date_time = parser.parse(data_stream[index].split(';', 1)[0])
            if date_time < line_date_time:
                index -= increment
                line_date_time = parser.parse(data_stream[index].split(';', 1)[0])
                break
            index += increment

        for i, line in enumerate(data_stream[index:], start=index):
            line_date_time = parser.parse(line.split(';', 1)[0])
            if date_time <= line_date_time:
                return i-1

    def generate_time_frames(self):
        base_minute = parser.parse(self.one_minute_data[0].split(DATA_DELIMITER)[0]).minute
        open_price = self.one_minute_data[0].split(DATA_DELIMITER)[OHLC.OPENINDEX.value]
        high_price = float(self.one_minute_data[0].split(DATA_DELIMITER)[OHLC.HIGHINDEX.value])
        low_price = float(self.one_minute_data[0].split(DATA_DELIMITER)[OHLC.LOWINDEX.value])
        base_5_min = base_minute
        open_5_min = open_price
        high_5_min = high_price
        low_5_min = low_price
        base_15_min = base_minute
        open_15_min = open_price
        high_15_min = high_price
        low_15_min = low_price
        base_hourly = base_minute
        open_hourly = open_price
        high_hourly = high_price
        low_hourly = low_price
        base_four_hourly = base_minute
        open_four_hourly = open_price
        high_four_hourly = high_price
        low_four_hourly = low_price
        base_daily = base_minute
        open_daily = open_price
        high_daily = high_price
        low_daily = low_price
        for index, minute in enumerate(self.one_minute_data):
            date_time = parser.parse(minute.split(DATA_DELIMITER)[0])
            high = float(minute.split(DATA_DELIMITER)[OHLC.HIGHINDEX.value])
            low = float(minute.split(DATA_DELIMITER)[OHLC.LOWINDEX.value])
            if high >= high_5_min:
                high_5_min = high
            if low <= low_5_min:
                low_5_min = low
            if high >= high_15_min:
                high_15_min = high
            if low <= low_15_min:
                low_15_min = low
            if high >= high_hourly:
                high_hourly = high
            if low <= low_hourly:
                low_hourly = low
            if high >= high_four_hourly:
                high_four_hourly = high
            if low <= low_four_hourly:
                low_four_hourly = low
            if high >= high_daily:
                high_daily = high
            if low <= low_daily:
                low_daily = low
            if (date_time.minute - base_5_min) > (FIVE_MINUTES - 1):
                record = self.one_minute_data[index-1].split(DATA_DELIMITER)
                record[0] = str(date_time - datetime.timedelta(minutes=date_time.minute%FIVE_MINUTES+FIVE_MINUTES))
                record[1] = open_5_min
                record[2] = str(high_5_min)
                record[3] = str(low_5_min)
                self.five_minute_data.append(";".join(record))
                base_5_min = date_time.minute
                open_5_min = self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.OPENINDEX.value]
                high_5_min = float(self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.HIGHINDEX.value])
                low_5_min = float(self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.LOWINDEX.value])
            if (date_time.minute - base_15_min) > (FIFTEEN_MINUTES - 1):
                record = self.one_minute_data[index-1].split(DATA_DELIMITER)
                record[0] = date_time - datetime.timedelta(minutes=date_time.minute%FIFTEEN_MINUTES+FIFTEEN_MINUTES)
                record[1] = open_15_min
                record[2] = high_15_min
                record[3] = low_15_min
                self.fifteen_minute_data.append(record)
                base_15_min = date_time.minute
                open_15_min = self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.OPENINDEX.value]
                high_15_min = float(self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.HIGHINDEX.value])
                low_15_min = float(self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.LOWINDEX.value])
            if (date_time.minute - base_hourly) > (ONE_HOUR - 1):
                record = self.one_minute_data[index-1].split(DATA_DELIMITER)
                record[0] = date_time - datetime.timedelta(minutes=date_time.minute%ONE_HOUR+ONE_HOUR)
                record[1] = open_hourly
                record[2] = high_hourly
                record[3] = low_hourly
                self.one_hour_data.append(record)
                base_hourly = date_time.minute
                open_hourly = self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.OPENINDEX.value]
                high_hourly = float(self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.HIGHINDEX.value])
                low_hourly = float(self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.LOWINDEX.value])
            if (date_time.minute - base_four_hourly) > (FOUR_HOUR - 1):
                break
                record = self.one_minute_data[index-1].split(DATA_DELIMITER)
                record[0] = date_time - datetime.timedelta(minutes=date_time.minute%FOUR_HOUR+FOUR_HOUR)
                record[1] = open_four_hourly
                record[2] = high_four_hourly
                record[3] = low_four_hourly
                self.four_hour_data.append(record)
                base_four_hourly = date_time.minute
                open_four_hourly = self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.OPENINDEX.value]
                high_four_hourly = float(self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.HIGHINDEX.value])
                low_four_hourly = float(self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.LOWINDEX.value])
            if (date_time.minute - base_daily) > (ONE_DAY - 1):
                record = self.one_minute_data[index-1].split(DATA_DELIMITER)
                record[0] = date_time - datetime.timedelta(minutes=date_time.minute%ONE_DAY+ONE_DAY)
                record[1] = open_daily
                record[2] = high_daily
                record[3] = low_daily
                self.daily_data.append(record)
                base_daily = date_time.minute
                open_daily = self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.OPENINDEX.value]
                high_daily = float(self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.HIGHINDEX.value])
                low_daily = float(self.one_minute_data[index].split(DATA_DELIMITER)[OHLC.LOWINDEX.value])
        data_dir = os.path.join(DATA_DIR,CURRENCY_PAIR)
        five_min_data = os.path.join(data_dir,"5min.csv")
        with open(five_min_data, 'w') as data:
            for item in self.five_minute_data:
                data.write(f"{item}")

    def manage(self):
        next_date_time = parser.parse(self.data[self.data_index+1].split(DATA_DELIMITER)[0])
        next_tick_date_time = parser.parse(self.tick_data[self.tick_index+1].split(DATA_DELIMITER)[0])
        next_one_min_date_time = parser.parse(self.one_minute_data[self.one_minute_index+1].split(DATA_DELIMITER)[0])
        # next_five_min_date_time = parser.parse(self.five_minute_data[self.five_minute_index+1].split(DATA_DELIMITER)[0])
        # next_fifteen_min_date_time = parser.parse(self.fifteen_minute_data[self.fifteen_minute_index+1].split(DATA_DELIMITER)[0])
        # next_one_hour_date_time = parser.parse(self.one_hour_data[self.one_hour_index+1].split(DATA_DELIMITER)[0])
        # next_four_hour_date_time = parser.parse(self.four_hour_data[self.four_hour_index+1].split(DATA_DELIMITER)[0])
        # next_daily_date_time = parser.parse(self.daily_data[self.daily_index+1].split(DATA_DELIMITER)[0])
        # self.date_time = datetime.now()-self.date_time_offset
        if self.date_time >= next_date_time:
            self.data_index += 1
        if self.date_time >= next_tick_date_time:
            self.tick_index += 1
        if self.date_time >= next_one_min_date_time:
            self.one_minute_index += 1
        # if self.date_time >= next_five_min_date_time:
        #     self.five_minute_index += 1
        # if self.date_time >= next_fifteen_min_date_time:
        #     self.fifteen_minute_index += 1
        # if self.date_time >= next_one_hour_date_time:
        #     self.one_hour_index += 1
        # if self.date_time >= next_four_hour_date_time:
        #     self.four_hour_index += 1
        # if self.date_time >= next_daily_date_time:
        #     self.daily_index += 1
        


if __name__ == "__main__":
    date_time = '2009-01-01 190000'
    state = TradeState(date_time, 50)
    tick_index  = state.find_current_date_time_index(state.date_time, state.tick_data)
    print(state.tick_data[tick_index])
    minute_index = state.find_current_date_time_index(state.date_time, state.one_minute_data)
    print(state.one_minute_data[minute_index])
    state.generate_time_frames()

