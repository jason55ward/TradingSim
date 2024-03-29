from enums import TradeMode, OHLC
from data import load_ticks, load_minutes
from constants import *
from dateutil import parser
import datetime
import os, sys

class TradeState:
    """"Keeps track of the current state"""
    def __init__(self, date_time, equity, settings):
        self.settings = settings
        self.done = False
        self.paused = True
        self.date_time = parser.parse(date_time) #the datetime in the past
        self.equity = equity
        self.profit = 0
        self.trade_mode = TradeMode.CLOSED
        self.order_prices = []
        self.average_price = 0
        self.position_size = 0
        self.stop_loss_price = 0
        self.pips = 0
        self.time_frame = 5
        self.data = {}
        self.data_index = {}
        self.tick_data = []
        self.tick_index = None
        self.minute_data = []
        self.minute_index = None
        self.support = []
        self.history = []
        self.tick_data = load_ticks(self.date_time)
        self.tick_index = 0
        self.minute_index = 0
        timedelta = datetime.timedelta(days=365)
        self.minute_data = []
        for year in range(-3,3):
            self.minute_data.extend(load_minutes(self.date_time+year*timedelta))
        self.date_time = self.date_time - datetime.timedelta(minutes=self.date_time.minute % self.time_frame) \
                        - datetime.timedelta(seconds=self.date_time.second)

    def find_current_date_time_index(self):
        """
        Moves the tick and minute index to match the current datetime.
        If weekend or flats move datetime forwards
        """
        #minutes
        curr_record = self.minute_data[self.minute_index].split(DATA_DELIMITER)
        curr_date_time = parser.parse(curr_record[0])
        seconds_offset = datetime.timedelta(seconds=self.date_time.second) \
                        + datetime.timedelta(microseconds=self.date_time.microsecond) 
        #make the big jumps
        if self.date_time > curr_date_time:
            diff = self.date_time - curr_date_time
            minutes = diff.days*24*60*5//7
            self.minute_index += minutes
        elif self.date_time < curr_date_time:
            diff = curr_date_time - self.date_time
            minutes = diff.days*24*60*5//7
            self.minute_index -= minutes
            
        #now refine
        curr_record = self.minute_data[self.minute_index].split(DATA_DELIMITER)
        curr_date_time = parser.parse(curr_record[0])
        diff = self.date_time - curr_date_time

        while self.date_time > curr_date_time:
            self.minute_index += 1
            curr_record = self.minute_data[self.minute_index].split(DATA_DELIMITER)
            curr_date_time = parser.parse(curr_record[0])
        while self.date_time < curr_date_time:
            self.minute_index -= 1
            curr_record = self.minute_data[self.minute_index].split(DATA_DELIMITER)
            curr_date_time = parser.parse(curr_record[0])
        if self.date_time-seconds_offset > curr_date_time:
            self.minute_index += 1
            curr_record = self.minute_data[self.minute_index].split(DATA_DELIMITER)
            curr_date_time = parser.parse(curr_record[0])

        next_record = self.minute_data[self.minute_index+1].split(DATA_DELIMITER)
        next_date_time = parser.parse(next_record[0])

        if self.date_time + datetime.timedelta(minutes=5) < next_date_time:
            self.date_time -= datetime.timedelta(seconds=self.date_time.second)
            while self.date_time < next_date_time:
                self.date_time += datetime.timedelta(minutes=1)
    
    def prior_day(self):
        self.data = {}
        self.date_time -= datetime.timedelta(days=1) 
        self.date_time -= datetime.timedelta(minutes=self.date_time.minute)
        self.date_time -= datetime.timedelta(minutes=self.date_time.second)

    def next_bar(self):
        seconds_offset = datetime.timedelta(seconds=self.date_time.second) - datetime.timedelta(microseconds=self.date_time.microsecond)
        next_bar_minute_timedelta = self.time_frame-self.date_time.minute%self.time_frame
        if next_bar_minute_timedelta == 1:
            next_bar_minute_timedelta = self.time_frame
        elif next_bar_minute_timedelta != 1:
            next_bar_minute_timedelta-=1
        self.date_time += datetime.timedelta(minutes=next_bar_minute_timedelta) - seconds_offset

    def move_time_forward(self):
        frame_speed = datetime.timedelta(milliseconds=self.settings.time_delta/FRAME_RATE*100*self.settings.time_speed)
        self.date_time += frame_speed

    def manage(self):
        try:
            if not self.paused:
                self.move_time_forward()
            self.find_current_date_time_index()
            # curr_tick_record = self.tick_data[self.tick_index].split(DATA_DELIMITER)
            curr_record = self.minute_data[self.minute_index].split(DATA_DELIMITER)
            curr_date_time = parser.parse(curr_record[OHLC.DATETIMEINDEX.value])
            bar_open_dt = curr_date_time - datetime.timedelta(minutes=curr_date_time.minute % self.time_frame)

            #set up the draw list, create list if doesn't exist. Insert infront if exists and it's after the current data set.
            new_rec = False
            if self.time_frame not in self.data:
                new_rec = True
                self.data[self.time_frame] = [curr_record]
                self.data[self.time_frame][0][OHLC.DATETIMEINDEX.value] = bar_open_dt
            elif bar_open_dt > self.data[self.time_frame][0][OHLC.DATETIMEINDEX.value]:
                new_rec = True
                self.data[self.time_frame].insert(0, curr_record)
                self.data[self.time_frame][0][OHLC.DATETIMEINDEX.value] = bar_open_dt
            if new_rec:
                self.data[self.time_frame][0][OHLC.OPENINDEX.value] = float(self.data[self.time_frame][0][OHLC.OPENINDEX.value])
                self.data[self.time_frame][0][OHLC.HIGHINDEX.value] = float(self.data[self.time_frame][0][OHLC.HIGHINDEX.value])
                self.data[self.time_frame][0][OHLC.LOWINDEX.value] = float(self.data[self.time_frame][0][OHLC.LOWINDEX.value])
                self.data[self.time_frame][0][OHLC.CLOSEINDEX.value] = float(self.data[self.time_frame][0][OHLC.CLOSEINDEX.value])
            
            high = float(curr_record[OHLC.HIGHINDEX.value])
            low = float(curr_record[OHLC.LOWINDEX.value])
            close = float(curr_record[OHLC.CLOSEINDEX.value])
            
            candle_count = 0
            offset = 0
            insert_index = 1

            #work backwards from current minute to build the candle list up to the candle limit for the screen
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
                #add bar if we've moved to before the time of the current bar
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

                    #prevent inserting data that already exists. The first bar and the bar before it will be overwritten.
                    #Caters for NextBar() to cause the entire data set to enter the bucket
                    bar_open_dt = prev_dt - datetime.timedelta(minutes=prev_dt.minute % self.time_frame)
                    if insert_index < len(self.data[self.time_frame]):
                        if (insert_index == 3 and
                            bar_open_dt <= self.data[self.time_frame][insert_index][OHLC.DATETIMEINDEX.value]):
                                break
                    else:
                        self.data[self.time_frame].insert(insert_index, prev_record)

                    #setup new bar with close value, when bar complete we'll update it on next iteration with the OHLC as above
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
    # tick_index  = state.find_current_date_time_index(state.date_time, state.tick_data)
    # print(state.tick_data[tick_index])
    minute_index = state.find_current_date_time_index(state.date_time, state.one_minute_data)
    print(state.one_minute_data[minute_index])
    #state.generate_time_frames()

