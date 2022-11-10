# !/usr/bin/python

from enums import TradeMode, OHLC
from trade_state import TradeState
from events import Events
from orders import Orders
from chart import Chart
from config import Config
from settings import Settings
from constants import *
from text_display import TextDisplay
from helpers import draw_horizontal_dashed_line
import sys
import os
import logging
import pygame
from pygame.locals import *
logging.basicConfig(level=logging.DEBUG)

"""
App for testing out trading ideas
"""


class Trading():
    """
    Trading Practice App
    """

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.settings = Settings()
        
        self.config = Config(self.settings.config_file, self.settings.history_file)
        date_time, equity = self.config.read_config()
        self.state = TradeState(date_time=date_time, equity=equity, settings=self.settings)
        
        self.screen = pygame.display.set_mode(size=SCREEN_SIZE, flags=pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE, depth=32, display=0)
        pygame.display.set_caption(APP_NAME)
        self.settings.screen_width, self.settings.screen_height = pygame.display.get_surface().get_size()
        
        self.text_display = TextDisplay(screen=self.screen, state=self.state, 
                                        settings=self.settings)
        
        self.chart = Chart(screen=self.screen, state=self.state, settings=self.settings)
        self.events = Events(state=self.state, settings=self.settings, config=self.config)
        self.orders = Orders(state=self.state, settings=self.settings)

    def main_loop(self):
        """
        The loop that runs the app
        """
        try:
            clock = pygame.time.Clock()
            while not self.state.done:
                self.settings.time_delta = clock.tick(FRAME_RATE)
                self.events.process_events()
                self.screen.fill(SCREEN_RGB)
                self.state.manage()
                self.orders.check_orders()
                self.text_display.draw_info_text()
                if self.settings.showing_help:
                    self.text_display.displayHelp()
                self.draw_chart()
                pygame.display.flip()
                self.settings.first_run = False
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(sys.exc_info())

    def draw_chart(self):
        """
        Draws the chart
        """
        try:
            self.chart.calc_high_low_price()
            self.chart.draw_price_lines()
            self.chart.draw_chart_data()
            self.chart.draw_orders()
            if self.settings.show_history:
                self.chart.draw_history()
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(sys.exc_info())


if __name__ == "__main__":
    app = Trading()
    app.main_loop()
