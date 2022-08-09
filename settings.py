import os
from datetime import datetime
from constants import *
import pygame

class Settings():
    def __init__(self, data):
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        if not os.path.exists(SETTINGS_DIR):
            os.mkdir(SETTINGS_DIR)
        self.config_file = os.path.join(SETTINGS_DIR, 'config.txt')
        self.history_file = os.path.join(SETTINGS_DIR, 'history.txt')
        self.font = pygame.font.SysFont('dejavuserif', 20)
        self.price_level_font = pygame.font.SysFont('dejavuserif', 15)
        self.done = False
        self.max_candles = 250
        self.candle_width = 5
        self.candle_spacing = 2
        self.chart_pip_height = 150
        self.factor = 0
        self.first_run = True
        self.showing_help = False
        self.history = list()
        self.show_history = False
        self.support = list()
        self.position_size = 1
        self.max_height = 0
        self.min_height = 9999
        self.minutes = 1
        self.last_candle = self.max_candles
        self.start_time = datetime.now()
        self.bid = data[0]
        self.data = data[0]
        self.one_minute_data = data[0]
        self.five_minute_data = data[1]
        self.fifteen_minute_data = data[2]
        self.one_hour_data = data[3]
        self.four_hour_data = data[4]
        self.daily_data = data[5]
