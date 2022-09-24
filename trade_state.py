from enums import TradeMode, OHLC
from load_data import load_ticks, load_minutes
from constants import *
from dateutil import parser
import datetime
import os, sys

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
        self.time_frame = 60
        self.data = {}
        self.data_index = {}
        self.tick_data = []
        self.tick_index = None
        self.minute_data = []
        self.minute_index = None
        self.support = []
        self.history = []

        # self.tick_data = load_ticks(self.date_time)
        # self.tick_index = self.find_current_date_time_index(self.date_time, self.tick_data)
        self.minute_data = load_minutes(self.date_time)
        self.minute_index = self.find_current_date_time_index(self.date_time, self.minute_data)

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

    def manage(self):
        try:
            curr_record = self.minute_data[self.minute_index].split(DATA_DELIMITER)
            bar_open_dt = parser.parse(curr_record[OHLC.DATETIMEINDEX.value]) - datetime.timedelta(minutes=parser.parse(curr_record[0]).minute % self.time_frame)
            while bar_open_dt+datetime.timedelta(minutes=self.time_frame-1) > parser.parse(curr_record[OHLC.DATETIMEINDEX.value]):
                self.minute_index+=1
                curr_record = self.minute_data[self.minute_index].split(DATA_DELIMITER)
            insert_index = 1
            #set up the draw list
            if self.time_frame not in self.data:
                self.data[self.time_frame] = [curr_record]
                self.data[self.time_frame][0][OHLC.DATETIMEINDEX.value] = bar_open_dt
            elif bar_open_dt > self.data[self.time_frame][0][OHLC.DATETIMEINDEX.value]:
                self.data[self.time_frame].insert(0, curr_record)
                self.data[self.time_frame][0][OHLC.DATETIMEINDEX.value] = bar_open_dt
            self.data[self.time_frame][0][OHLC.OPENINDEX.value] = float(self.data[self.time_frame][0][OHLC.OPENINDEX.value])
            self.data[self.time_frame][0][OHLC.HIGHINDEX.value] = float(self.data[self.time_frame][0][OHLC.HIGHINDEX.value])
            self.data[self.time_frame][0][OHLC.LOWINDEX.value] = float(self.data[self.time_frame][0][OHLC.LOWINDEX.value])
            self.data[self.time_frame][0][OHLC.CLOSEINDEX.value] = float(self.data[self.time_frame][0][OHLC.CLOSEINDEX.value])
            high = float(curr_record[OHLC.HIGHINDEX.value])
            low = float(curr_record[OHLC.LOWINDEX.value])
            close = float(curr_record[OHLC.CLOSEINDEX.value])

            candle_count = 0
            offset = 0
            while candle_count < MAX_CANDLES:
                curr_record = self.minute_data[self.minute_index-offset].split(DATA_DELIMITER)
                curr_dt = parser.parse(curr_record[OHLC.DATETIMEINDEX.value])
                prev_record = self.minute_data[self.minute_index-offset-1].split(DATA_DELIMITER)
                prev_dt = parser.parse(prev_record[OHLC.DATETIMEINDEX.value])
                dt_diff = (curr_dt - prev_dt).total_seconds() // 60
                if dt_diff < 1:
                    raise Exception("DT DIFF IS TOO SMALL")
                if high < float(curr_record[OHLC.HIGHINDEX.value]):
                    high = float(curr_record[OHLC.HIGHINDEX.value])
                elif low > float(curr_record[OHLC.LOWINDEX.value]):
                    low = float(curr_record[OHLC.LOWINDEX.value])
                #add bar
                if prev_dt < bar_open_dt:
                    #set OHLC price before moving to next bar
                    open_value = float(curr_record[OHLC.OPENINDEX.value])
                    if open_value > high:
                        high = open_value
                    if open_value < low:
                        low = open_value
                    self.data[self.time_frame][insert_index-1][OHLC.OPENINDEX.value] = open_value
                    self.data[self.time_frame][insert_index-1][OHLC.HIGHINDEX.value] = high
                    self.data[self.time_frame][insert_index-1][OHLC.LOWINDEX.value] = low
                    self.data[self.time_frame][insert_index-1][OHLC.CLOSEINDEX.value] = close

                    #setup new bar with close value, when bar complete we'll update it on next iteration with the OHLC as above
                    bar_open_dt = prev_dt - datetime.timedelta(minutes=prev_dt.minute % self.time_frame)
                    if (insert_index < len(self.data[self.time_frame])
                        and bar_open_dt <= self.data[self.time_frame][insert_index][OHLC.DATETIMEINDEX.value]):
                            break
                    self.data[self.time_frame].insert(insert_index, prev_record)
                    self.data[self.time_frame][insert_index][OHLC.DATETIMEINDEX.value] = bar_open_dt
                    high = float(prev_record[OHLC.HIGHINDEX.value])
                    low = float(prev_record[OHLC.LOWINDEX.value])
                    close = float(prev_record[OHLC.CLOSEINDEX.value])
                    insert_index+=1
                    candle_count+=1
                offset+=1
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(sys.exc_info())

        


if __name__ == "__main__":
    date_time = '2009-01-01 190000'
    state = TradeState(date_time, 50)
    tick_index  = state.find_current_date_time_index(state.date_time, state.tick_data)
    print(state.tick_data[tick_index])
    minute_index = state.find_current_date_time_index(state.date_time, state.one_minute_data)
    print(state.one_minute_data[minute_index])
    #state.generate_time_frames()

