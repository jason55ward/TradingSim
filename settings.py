import os
from datetime import datetime
from constants import *
import pygame

class Settings():
    def __init__(self):
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        if not os.path.exists(SETTINGS_DIR):
            os.mkdir(SETTINGS_DIR)
        self.config_file = os.path.join(SETTINGS_DIR, 'config.txt')
        self.history_file = os.path.join(SETTINGS_DIR, 'history.txt')
        self.font = pygame.font.SysFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        self.price_level_font = pygame.font.SysFont(DEFAULT_FONT, DEFAULT_FONT_SIZE-5)
        self.candle_width = 5
        self.candle_spacing = 2
        self.chart_pip_height = 150
        self.factor = 0
        self.first_run = True
        self.showing_help = False
        self.show_history = False
        self.default_position_size = 1
        self.max_height = 0
        self.min_height = 9999999
