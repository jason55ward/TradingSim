import os
from datetime import datetime
from constants import *

class Settings():
    def __init__(self, data):
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        if not os.path.exists(SETTINGS_DIR):
            os.mkdir(SETTINGS_DIR)
        self.config_file = os.path.join(SETTINGS_DIR, 'config.txt')
        self.history_file = os.path.join(SETTINGS_DIR, 'history.txt')
        self.done = False
        self.max_candles = 350
        self.candle_width = 3
        self.candle_spacing = 2
        self.chart_pip_height = 200
        self.factor = 0
        self.first_run = True
        self.showing_help = False
        self.history = list()
        self.show_history = False
        self.support = list()
        self.position_size = 0.5
        self.max_height = 0
        self.min_height = 9999
        self.temp_last_candle = 0
        self.minutes = 1
        self.last_candle = self.max_candles
        self.start_time = datetime.now()
        self.bid = (data)
        self.one_minute_data = (data)
        self.five_minute_data = ()
        self.fifteen_minute_data = ()
        self.one_hour_data = ()
        self.four_hour_data = ()
        self.daily_data = ()
