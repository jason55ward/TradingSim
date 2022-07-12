# !/usr/bin/python

from enums import TradeMode, OHLC
from trade_state import TradeState
from load_data import LoadData
from config import Config
from settings import Settings
from constants import *
from text_display import TextDisplay
from helpers import draw_horizontal_dashed_line
import sys
from dateutil import parser
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
        self.data = LoadData()
        data = self.data.load_data()
        self.settings = Settings(data=data)   
        self.trade_state = TradeState()  
        self.config = Config(self.settings.config_file, self.settings.history_file, self.trade_state)
        
        pygame.init()
        self.screen = pygame.display.set_mode(size=(
            1920, 1080), flags=pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE, depth=32, display=0)
        pygame.display.set_caption("Trading Practice App")
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.price_level_font = pygame.font.SysFont('Comic Sans MS', 15)
        
        self.settings.screen_width, self.settings.screen_height = pygame.display.get_surface().get_size()
        
        self.text_display = TextDisplay(font=self.font, screen=self.screen, trade_state=self.trade_state, 
                                        settings=self.settings)
        self.config.read_config()

    def main_loop(self):
        """
        The loop that runs the app
        """
        try:
            while not self.settings.done:
                self.do_events()
                self.screen.fill((45, 45, 45))
                self.check_orders()
                self.text_display.draw_info_text()
                if self.settings.showing_help:
                    self.text_display.displayHelp()
                self.draw_chart()
                pygame.display.flip()
                self.first_run = False
        except:
            print("Unexpected error:", sys.exc_info())

    def draw_chart(self):
        """
        Draws the chart
        """
        if self.settings.last_candle < self.settings.max_candles:
            self.settings.last_candle = self.settings.max_candles
        self.settings.max_height = 0
        self.settings.min_height = 9999
        for x in range(0, self.settings.max_candles):
            offset = self.settings.last_candle-x
            high = float(self.settings.bid[offset].split(',')[OHLC.HIGHINDEX.value])
            if high > self.settings.max_height:
                self.settings.max_height = high
            low = float(self.settings.bid[offset].split(',')[OHLC.LOWINDEX.value])
            if low < self.settings.min_height:
                self.settings.min_height = low
        self.settings.factor = (self.settings.screen_height - CHART_TOP_Y_OFFSET) / \
            self.settings.chart_pip_height * 10000
        # Draw Price Lines
        for x in range(0, self.settings.chart_pip_height+100, 10):
            val = float("%.3f" % self.settings.max_height) - (x-50)*0.0001
            line_ypos = int(self.settings.screen_height - (val-self.settings.min_height)
                            * self.settings.factor) - CHART_TOP_Y_OFFSET
            pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (0, line_ypos),
                             (self.settings.screen_width - CHART_RIGHT_SPACING - 5, line_ypos), 1)
            text = self.price_level_font.render(
                str(val).ljust(7, '0'), 1, (BEAR_CANDLE_COLOUR))
            self.screen.blit(text, (self.settings.screen_width -
                             CHART_RIGHT_SPACING, line_ypos - 13))
        for val in self.settings.support:
            line_ypos = int(self.settings.screen_height - (float(val) -
                            self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            pygame.draw.line(self.screen, BULL_CANDLE_COLOUR, (0, line_ypos),
                             (self.settings.screen_width - CHART_RIGHT_SPACING - 5, line_ypos), 1)
        # Draw Chart Data
        for x in range(0, self.settings.max_candles):
            offset = self.settings.last_candle-x
            xpos = self.settings.candle_spacing + \
                (self.settings.candle_spacing + self.settings.candle_width) * (self.settings.max_candles-x)
            open_price = float(self.settings.bid[offset].split(',')[
                               OHLC.OPENINDEX.value])
            high_price = float(self.settings.bid[offset].split(',')[
                               OHLC.HIGHINDEX.value])
            low_price = float(self.settings.bid[offset].split(',')[OHLC.LOWINDEX.value])
            close_price = float(self.settings.bid[offset].split(',')[
                                OHLC.CLOSEINDEX.value])
            candle_open_ypos = int(
                self.settings.screen_height - (open_price-self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            candle_high_ypos = int(
                self.settings.screen_height - (high_price-self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            candle_low_ypos = int(
                self.settings.screen_height - (low_price-self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            candle_close_ypos = int(
                self.settings.screen_height - (close_price-self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            candle_close_distance = int(
                abs(open_price-close_price) * self.settings.factor)
            if candle_open_ypos < candle_close_ypos:
                pygame.draw.rect(self.screen, BEAR_CANDLE_COLOUR, (xpos,
                                 candle_open_ypos, self.settings.candle_width, candle_close_distance))
                # Draw Candle Wick
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (xpos+int(self.settings.candle_width/2),
                                 candle_high_ypos), (xpos+int(self.settings.candle_width/2), candle_open_ypos), 1)
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (xpos+int(self.settings.candle_width/2),
                                 candle_low_ypos), (xpos+int(self.settings.candle_width/2), candle_close_ypos), 1)
            elif candle_open_ypos > candle_close_ypos:
                pygame.draw.rect(self.screen, BULL_CANDLE_COLOUR, (xpos,
                                 candle_close_ypos, self.settings.candle_width, candle_close_distance))
                # Draw Candle Wick
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (xpos+int(self.settings.candle_width/2),
                                 candle_high_ypos), (xpos+int(self.settings.candle_width/2), candle_close_ypos), 1)
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (xpos+int(self.settings.candle_width/2),
                                 candle_low_ypos), (xpos+int(self.settings.candle_width/2), candle_open_ypos), 1)
            # Draw Candle Body
            pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (xpos,
                             candle_open_ypos), (xpos+self.settings.candle_width, candle_open_ypos), 1)
            pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (xpos+self.settings.candle_width,
                             candle_open_ypos), (xpos+self.settings.candle_width, candle_close_ypos), 1)
            pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (xpos,
                             candle_close_ypos), (xpos+self.settings.candle_width, candle_close_ypos), 1)
            pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR,
                             (xpos, candle_open_ypos), (xpos, candle_close_ypos), 1)
        # Draw open position and stop loss
        if (self.trade_state.trade_mode != TradeMode.CLOSED):
            order_ypos = int(self.settings.screen_height - (self.trade_state.order_price -
                             self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            stop_ypos = int(self.settings.screen_height - (self.trade_state.stop_loss_price -
                            self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            draw_horizontal_dashed_line(self.screen, ORDER_COLOUR, (
                0, order_ypos), (self.settings.screen_width - CHART_RIGHT_SPACING, order_ypos))
            draw_horizontal_dashed_line(self.screen, STOP_LOSS_COLOUR, (
                0, stop_ypos), (self.settings.screen_width - CHART_RIGHT_SPACING, stop_ypos))
        # Draw historical trades
        if self.settings.show_history:
            history_offset = self.settings.last_candle - self.settings.max_candles
            for hist in self.settings.history:
                if int(hist[2]) >= history_offset and int(hist[2]) <= self.settings.last_candle:
                    history_open_xpos = self.settings.candle_spacing + \
                        (self.settings.candle_spacing + self.settings.candle_width) * \
                        (self.settings.max_candles - (self.settings.last_candle - int(hist[0])))
                    history_open_trade_ypos = int(
                        self.settings.screen_height - (float(hist[1])-self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
                    history_close_xpos = self.settings.candle_spacing + \
                        (self.settings.candle_spacing + self.settings.candle_width) * \
                        (self.settings.max_candles - (self.settings.last_candle - int(hist[2])))
                    history_close_trade_ypos = int(
                        self.settings.screen_height - (float(hist[3])-self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
                    history_colour = BULL_CANDLE_COLOUR if int(
                        hist[4]) == TradeMode.BUY.value else BEAR_CANDLE_COLOUR
                    pygame.draw.line(self.screen, history_colour, (history_open_xpos,
                                     history_open_trade_ypos), (history_close_xpos, history_close_trade_ypos), 1)

    def check_orders(self):
        if (self.trade_state.trade_mode == TradeMode.BUY):
            self.trade_state.pips = 1 + (float(self.settings.bid[self.settings.last_candle].split(
                ',')[OHLC.CLOSEINDEX.value]) - self.trade_state.order_price) * 10000
            self.trade_state.profit = self.trade_state.pips * \
                abs(self.trade_state.position_size)
            if float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.LOWINDEX.value]) <= self.trade_state.stop_loss_price:
                logging.debug('close buy check')
                self.close(self.trade_state.stop_loss_price)

        if (self.trade_state.trade_mode == TradeMode.SELL):
            self.trade_state.pips = 1 + (self.trade_state.order_price - float(
                self.settings.bid[self.settings.last_candle].split(',')[OHLC.CLOSEINDEX.value])) * 10000
            self.trade_state.profit = self.trade_state.pips * \
                abs(self.trade_state.position_size)
            if float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.HIGHINDEX.value]) >= self.trade_state.stop_loss_price:
                logging.debug('close sell check')
                self.close(self.trade_state.stop_loss_price)

    def buy(self):
        if self.trade_state.trade_mode == TradeMode.SELL:
            return
        current_close_price = float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.CLOSEINDEX.value])
        if self.trade_state.order_price:
            self.trade_state.order_price = (self.trade_state.order_price*self.trade_state.position_size + current_close_price*self.settings.position_size) \
                                            / (self.trade_state.position_size+self.settings.position_size)
        else:
            self.trade_state.order_price = current_close_price
        self.trade_state.stop_loss_price = self.trade_state.order_price - TRADE_RISK_PIPS * 0.0001
        self.trade_state.position_size += self.settings.position_size
        self.trade_state.candle_number = self.settings.last_candle
        if self.trade_state.position_size > 0:
            self.trade_state.trade_mode = TradeMode.BUY
        else:
            self.trade_state.trade_mode = TradeMode.SELL
        if self.trade_state.position_size == 0:
            logging.debug('buy neutral close')
            self.close(self.trade_state.order_price)

    def sell(self):
        if self.trade_state.trade_mode == TradeMode.BUY:
            return
        current_close_price = float(self.settings.bid[self.settings.last_candle].split(',')[OHLC.CLOSEINDEX.value])
        if self.trade_state.order_price:
            self.trade_state.order_price = (self.trade_state.order_price*self.trade_state.position_size + current_close_price*self.settings.position_size*-1) \
                                            / (self.trade_state.position_size+self.settings.position_size*-1)
        else:
            self.trade_state.order_price = current_close_price
        
        self.trade_state.stop_loss_price = self.trade_state.order_price + TRADE_RISK_PIPS * 0.0001
        self.trade_state.position_size += self.settings.position_size*-1
        self.trade_state.candle_number = self.settings.last_candle
        if self.trade_state.position_size > 0:
            self.trade_state.trade_mode = TradeMode.BUY
        else:
            self.trade_state.trade_mode = TradeMode.SELL
        if self.trade_state.position_size == 0:
            logging.debug('sell neutral close')
            self.close(self.trade_state.order_price)

    def close(self, close_price=None):
        if self.trade_state.trade_mode != TradeMode.CLOSED:
            self.settings.history.append([
                self.trade_state.candle_number,
                self.trade_state.order_price,
                self.settings.last_candle,
                close_price or self.settings.bid[self.settings.last_candle].split(
                    ',')[OHLC.CLOSEINDEX.value],
                self.trade_state.trade_mode.value
            ])
            self.trade_state.trade_mode = TradeMode.CLOSED
            self.trade_state.equity += self.trade_state.profit
            self.trade_state.profit = 0
            self.trade_state.order_price = 0
            self.trade_state.position_size = 0
            self.trade_state.stop_loss_price = 0
            self.trade_state.pips = 0

    def do_events(self):
        """
        Query for quit and keypress events
        """
        events = pygame.event.get(pump=True)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.settings.last_candle = self.settings.temp_last_candle
                    self.config.write_config(self.settings.last_candle, self.settings.history)
                    self.settings.done = True
                if event.key == pygame.K_DOWN:
                    self.settings.chart_pip_height += 20
                if event.key == pygame.K_UP:
                    self.settings.chart_pip_height -= 20
                if event.key == pygame.K_LEFT:
                    self.settings.last_candle -= self.settings.minutes
                    self.settings.last_candle -= 1
                    if self.settings.last_candle < self.settings.max_candles:
                        self.settings.last_candle = self.settings.max_candles
                if event.key == pygame.K_RIGHT:
                    self.settings.last_candle += self.settings.minutes
                    self.settings.last_candle += 1
                if event.key == pygame.K_h:
                    self.settings.show_history = not self.settings.show_history
                if event.key == pygame.K_b:
                    self.buy()
                if event.key == pygame.K_s:
                    self.sell()
                if event.key == pygame.K_c:
                    self.close()
                if event.key == pygame.K_F1:
                    self.settings.showing_help = not self.settings.showing_help
                if event.key == pygame.K_1:
                    self.settings.last_candle = self.settings.last_candle
                    self.settings.minutes = 1
                    self.settings.last_candle = self.settings.last_candle//self.settings.minutes
                    self.settings.bid = self.settings.one_minute_data
                if event.key == pygame.K_2:
                    self.settings.last_candle = self.settings.last_candle
                    self.settings.minutes = 5
                    self.settings.last_candle = self.settings.last_candle//self.settings.minutes
                    current_datetime_string = self.settings.one_minute_data[self.settings.last_candle].split(',')[0]
                    current_datetime = parser.parse(current_datetime_string)
                    higher_datetime_string = self.settings.five_minute_data[self.settings.last_candle].split(',')[0]
                    higher_datetime = parser.parse(higher_datetime_string)
                    while higher_datetime < current_datetime:
                        self.settings.last_candle+=1
                        higher_datetime_string = self.settings.five_minute_data[self.settings.last_candle].split(',')[0]
                        higher_datetime = parser.parse(higher_datetime_string)
                    self.settings.last_candle-=1
                    self.settings.bid = self.settings.five_minute_data
                if event.key == pygame.K_3:
                    self.settings.last_candle = self.settings.last_candle
                    self.settings.minutes = 15
                    self.settings.last_candle = self.settings.last_candle//self.settings.minutes
                    current_datetime_string = self.settings.one_minute_data[self.settings.last_candle].split(',')[0]
                    current_datetime = parser.parse(current_datetime_string)
                    higher_datetime_string = self.settings.fifteen_minute_data[self.settings.last_candle].split(',')[0]
                    higher_datetime = parser.parse(higher_datetime_string)
                    while higher_datetime < current_datetime:
                        self.settings.last_candle+=1
                        higher_datetime_string = self.settings.fifteen_minute_data[self.settings.last_candle].split(',')[0]
                        higher_datetime = parser.parse(higher_datetime_string)
                    self.settings.last_candle-=1
                    self.settings.bid = self.settings.fifteen_minute_data
                if event.key == pygame.K_4:
                    self.settings.last_candle = self.settings.last_candle
                    self.settings.minutes = ONE_HOUR
                    self.settings.last_candle = self.settings.last_candle//self.settings.minutes
                    current_datetime_string = self.settings.one_minute_data[self.settings.last_candle].split(',')[0]
                    current_datetime = parser.parse(current_datetime_string)
                    higher_datetime_string = self.settings.one_hour_data[self.settings.last_candle].split(',')[0]
                    higher_datetime = parser.parse(higher_datetime_string)
                    while higher_datetime < current_datetime:
                        self.settings.last_candle+=1
                        higher_datetime_string = self.settings.one_hour_data[self.settings.last_candle].split(',')[0]
                        higher_datetime = parser.parse(higher_datetime_string)
                    self.settings.last_candle-=1
                    self.settings.bid = self.settings.one_hour_data
                if event.key == pygame.K_5:
                    self.settings.last_candle = self.settings.last_candle
                    self.settings.minutes = FOUR_HOUR
                    self.settings.last_candle = self.settings.last_candle//self.settings.minutes
                    current_datetime_string = self.settings.one_minute_data[self.settings.last_candle].split(',')[0]
                    current_datetime = parser.parse(current_datetime_string)
                    higher_datetime_string = self.settings.four_hour_data[self.settings.last_candle].split(',')[0]
                    higher_datetime = parser.parse(higher_datetime_string)
                    while higher_datetime < current_datetime:
                        self.settings.last_candle+=1
                        higher_datetime_string = self.settings.four_hour_data[self.settings.last_candle].split(',')[0]
                        higher_datetime = parser.parse(higher_datetime_string)
                    self.settings.last_candle-=1
                    self.settings.bid = self.settings.four_hour_data
                if event.key == pygame.K_6:
                    self.settings.last_candle = self.settings.last_candle
                    self.settings.minutes = ONE_DAY
                    self.settings.last_candle = self.settings.last_candle//self.settings.minutes
                    current_datetime_string = self.settings.one_minute_data[self.settings.last_candle].split(',')[0]
                    current_datetime = parser.parse(current_datetime_string)
                    higher_datetime_string = self.settings.daily_data[self.settings.last_candle].split(',')[0]
                    higher_datetime = parser.parse(higher_datetime_string)
                    while higher_datetime < current_datetime:
                        self.settings.last_candle+=1
                        higher_datetime_string = self.settings.daily_data[self.settings.last_candle].split(',')[0]
                        higher_datetime = parser.parse(higher_datetime_string)
                    self.settings.last_candle-=1
                    self.settings.bid = self.settings.daily_data
                if event.key == pygame.K_p:
                    price = (self.settings.screen_height - pygame.mouse.get_pos()[1] - CHART_TOP_Y_OFFSET)/self.settings.factor + self.settings.min_height
                    self.settings.support.append(price)
                if event.key == pygame.K_i:
                    self.settings.support.clear()
                if event.key == pygame.K_o:
                    self.settings.support.pop()
                if event.key == pygame.K_k:
                    price = (self.settings.screen_height - pygame.mouse.get_pos()[1] - CHART_TOP_Y_OFFSET)/self.settings.factor + self.settings.min_height
                    self.trade_state.stop_loss_price = price
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                rel = pygame.mouse.get_rel()[0]
                move = 0
                if rel > 0:
                    move = -15
                elif rel < 0:
                    move = +15
                self.settings.last_candle += move
            if event.type is QUIT:
                self.settings.last_candle = self.settings.temp_last_candle
                self.config.write_config(self.settings.last_candle, self.settings.history)
                self.settings.done = True

    

    


if __name__ == "__main__":
    app = Trading()
    app.main_loop()
