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
        self.time_frame = 5
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

    def generate_time_frames(self):
        date_time = parser.parse(self.one_minute_data[0].split(DATA_DELIMITER)[0]).minute
        zeroed_date_time = date_time - datetime.timedelta(minutes=date_time.minute%FIVE_MINUTES)
        zeroed_record = self.one_minute_data[0].split(DATA_DELIMITER)
        zeroed_record[0] = zeroed_date_time
        self.five_minute_data.append(zeroed_record)
        self.fifteen_minute_data.append(zeroed_record)
        self.one_hour_data.append(zeroed_record)
        # self.four_hour_data.append(self.one_minute_data[0])
        # self.four_hour_data[0][0] = str(prev_date_time)
        # self.daily_data.append(self.one_minute_data[0])
        # self.daily_data[0][0] = str(prev_date_time)
        open_price = self.one_minute_data[0].split(DATA_DELIMITER)[OHLC.OPENINDEX.value]
        high_price = float(self.one_minute_data[0].split(DATA_DELIMITER)[OHLC.HIGHINDEX.value])
        low_price = float(self.one_minute_data[0].split(DATA_DELIMITER)[OHLC.LOWINDEX.value])
        open_5_min = open_15_min = open_hourly = open_price
        high_5_min = high_15_min = high_hourly = high_price
        low_5_min = low_15_min = low_hourly = low_price
        # open_four_hourly = open_price
        # high_four_hourly = high_price
        # low_four_hourly = low_price
        # open_daily = open_price
        # high_daily = high_price
        # low_daily = low_price
        for index, data in enumerate(self.one_minute_data):
            date_time = parser.parse(data.split(DATA_DELIMITER)[0])
            time_delta = date_time - prev_date_time
            if time_delta.days > 0:
                pass
            minute_diff = time_delta.seconds // 60
            high = float(data.split(DATA_DELIMITER)[OHLC.HIGHINDEX.value])
            low = float(data.split(DATA_DELIMITER)[OHLC.LOWINDEX.value])

            if high >= high_15_min:
                high_15_min = high
            if low <= low_15_min:
                low_15_min = low
            if high >= high_hourly:
                high_hourly = high
            if low <= low_hourly:
                low_hourly = low
            # if high >= high_four_hourly:
            #     high_four_hourly = high
            # if low <= low_four_hourly:
            #     low_four_hourly = low
            # if high >= high_daily:
            #     high_daily = high
            # if low <= low_daily:
            #     low_daily = low
            if minute_diff >= FIVE_MINUTES:
                record = self.one_minute_data[index].split(DATA_DELIMITER)
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
        try:
            self.data_index = 0
            next_date_time = parser.parse(self.minute_data[self.minute_index+1].split(DATA_DELIMITER)[0])
            self.date_time = datetime.datetime.now()-self.date_time_offset #adjusted date_time to program date_time
            #move to next if time surpasses but if the next is too far in the future, jump to the future
            #This filters out all the missing data
            if self.date_time >= next_date_time or self.date_time+datetime.timedelta(minutes=self.time_frame) < next_date_time:
                self.minute_index += 1
                self.date_time_offset = datetime.datetime.now() - next_date_time

            curr_record = self.minute_data[self.minute_index].split(DATA_DELIMITER)
            bar_open_dt = parser.parse(curr_record[0]) - datetime.timedelta(minutes=parser.parse(curr_record[0]).minute % self.time_frame)

            insert_index = 1
            #set up the draw list
            if self.time_frame not in self.data:
                self.data[self.time_frame] = [curr_record]
                self.data[self.time_frame][0][OHLC.DATETIMEINDEX.value] = bar_open_dt
            elif bar_open_dt > self.data[self.time_frame][0][OHLC.DATETIMEINDEX.value]:
                self.data[self.time_frame].insert(0, curr_record)
                self.data[self.time_frame][0][OHLC.DATETIMEINDEX.value] = bar_open_dt
            high = curr_record[OHLC.HIGHINDEX.value]
            low = curr_record[OHLC.LOWINDEX.value]
            close = curr_record[OHLC.CLOSEINDEX.value]

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
                if high < curr_record[OHLC.HIGHINDEX.value]:
                    high = curr_record[OHLC.HIGHINDEX.value]
                elif low > curr_record[OHLC.LOWINDEX.value]:
                    low = curr_record[OHLC.LOWINDEX.value]
                self.data[self.time_frame][insert_index-1][4] = curr_record[OHLC.CLOSEINDEX.value]
                #add bar
                if prev_dt < bar_open_dt:
                    #set OHL price before moving to next bar
                    open_value = curr_record[OHLC.OPENINDEX.value]
                    self.data[self.time_frame][insert_index-1][OHLC.OPENINDEX.value] = open_value
                    self.data[self.time_frame][insert_index-1][OHLC.CLOSEINDEX.value] = close
                    if open_value > high:
                        high = open_value
                    if open_value < low:
                        low = open_value
                    self.data[self.time_frame][insert_index-1][OHLC.HIGHINDEX.value] = high
                    self.data[self.time_frame][insert_index-1][OHLC.LOWINDEX.value] = low

                    bar_open_dt = prev_dt - datetime.timedelta(minutes=prev_dt.minute % self.time_frame)
                    if (insert_index < len(self.data[self.time_frame])
                        and bar_open_dt <= self.data[self.time_frame][insert_index][OHLC.DATETIMEINDEX.value]):
                            break
                    self.data[self.time_frame].insert(insert_index, prev_record) #close is implicitly fixed because we're currently at the last minute of bar
                    self.data[self.time_frame][insert_index][OHLC.DATETIMEINDEX.value] = bar_open_dt
                    insert_index+=1
                    high = prev_record[OHLC.HIGHINDEX.value]
                    low = prev_record[OHLC.LOWINDEX.value]
                    close = prev_record[OHLC.CLOSEINDEX.value]
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

