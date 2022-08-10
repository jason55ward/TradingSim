from constants import *
from enums import TradeMode, OHLC
import pygame
from helpers import draw_horizontal_dashed_line
import sys, os

class Chart():
    def __init__(self, screen, trade_state, settings):
        self.screen = screen
        self.trade_state = trade_state
        self.settings = settings

    def calc_high_low_price(self):
        try:
            self.settings.max_height = 0
            self.settings.min_height = 9999
            for x in range(0, self.settings.max_candles):
                offset = self.settings.last_candle//self.settings.minutes-x
                high = float(self.settings.data[offset].split(',')[OHLC.HIGHINDEX.value])
                if high > self.settings.max_height:
                    self.settings.max_height = high
                low = float(self.settings.data[offset].split(',')[OHLC.LOWINDEX.value])
                if low < self.settings.min_height:
                    self.settings.min_height = low
            self.settings.factor = (self.settings.screen_height - CHART_TOP_Y_OFFSET) / \
                self.settings.chart_pip_height * 10000
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(sys.exc_info())
            print(self.settings.last_candle)

    def draw_price_lines(self):
        try:
            for x in range(0, self.settings.chart_pip_height+100, 10):
                val = float("%.3f" % self.settings.max_height) - (x-50)*0.0001
                line_ypos = int(self.settings.screen_height - (val-self.settings.min_height)
                                * self.settings.factor) - CHART_TOP_Y_OFFSET
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (0, line_ypos),
                                (self.settings.screen_width - CHART_RIGHT_SPACING - 5, line_ypos), 1)
                text = self.settings.price_level_font.render(
                    str(val).ljust(7, '0'), 1, (BEAR_CANDLE_COLOUR))
                self.screen.blit(text, (self.settings.screen_width -
                                CHART_RIGHT_SPACING, line_ypos - 13))
            for val in self.settings.support:
                line_ypos = int(self.settings.screen_height - (float(val) -
                                self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
                pygame.draw.line(self.screen, BULL_CANDLE_COLOUR, (0, line_ypos),
                                (self.settings.screen_width - CHART_RIGHT_SPACING - 5, line_ypos), 1)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(sys.exc_info())
        
    def draw_chart_data(self):
        try:
            for x in range(-1, self.settings.max_candles):
                offset = self.settings.last_candle//self.settings.minutes-x
                if x == -1:
                    #currently not working because data is dirty and switching between timeframes doesn't correlate mathematically for line numbers
                    continue
                    minutes_outstanding = self.settings.last_candle % self.settings.minutes
                    print(minutes_outstanding)
                    if minutes_outstanding == 0: 
                        continue
                    offset+=2
                    xpos = self.settings.candle_spacing + \
                        (self.settings.candle_spacing + self.settings.candle_width) * (self.settings.max_candles+1)
                    open_price = float(self.settings.bid[offset].split(',')[
                                    OHLC.OPENINDEX.value])
                    close_price = float(self.settings.bid[offset+minutes_outstanding].split(',')[
                                        OHLC.CLOSEINDEX.value])
                    high_price=0
                    low_price=999999
                    for minute in range(minutes_outstanding):
                        temp_high_price = float(self.settings.bid[offset+minute].split(',')[OHLC.HIGHINDEX.value])
                        if temp_high_price > high_price:
                            high_price = temp_high_price
                        temp_low_price = float(self.settings.bid[offset+minute].split(',')[OHLC.LOWINDEX.value])
                        if temp_low_price < low_price:
                            low_price = temp_low_price
                        print(high_price)
                        print(low_price)
                    
                else:
                    xpos = self.settings.candle_spacing + \
                        (self.settings.candle_spacing + self.settings.candle_width) * (self.settings.max_candles-x)
                    open_price = float(self.settings.data[offset].split(',')[
                                    OHLC.OPENINDEX.value])
                    high_price = float(self.settings.data[offset].split(',')[
                                    OHLC.HIGHINDEX.value])
                    low_price = float(self.settings.data[offset].split(',')[OHLC.LOWINDEX.value])
                    close_price = float(self.settings.data[offset].split(',')[
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
                # Draw Candle Wick
                colour = BULL_CANDLE_COLOUR
                top_y_pos = candle_close_ypos
                bottom_y_pos = candle_open_ypos
                if candle_open_ypos < candle_close_ypos:
                    colour = BEAR_CANDLE_COLOUR
                    top_y_pos = candle_open_ypos
                    bottom_y_pos = candle_close_ypos
                    
                start_x_pos = xpos+int(self.settings.candle_width/2)
                end_x_pos = xpos+int(self.settings.candle_width/2)
                pygame.draw.rect(self.screen, colour, (xpos, top_y_pos, self.settings.candle_width, candle_close_distance))
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (start_x_pos, candle_high_ypos), (end_x_pos, top_y_pos), 1)
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (start_x_pos, candle_low_ypos), (end_x_pos, bottom_y_pos), 1)
                # Draw Candle Body
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (xpos,
                                candle_open_ypos), (xpos+self.settings.candle_width, candle_open_ypos), 1)
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (xpos+self.settings.candle_width,
                                candle_open_ypos), (xpos+self.settings.candle_width, candle_close_ypos), 1)
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR, (xpos,
                                candle_close_ypos), (xpos+self.settings.candle_width, candle_close_ypos), 1)
                pygame.draw.line(self.screen, DOJI_CANDLE_COLOUR,
                                (xpos, candle_open_ypos), (xpos, candle_close_ypos), 1)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(sys.exc_info())
            print(self.settings.last_candle)
            print(offset)
    
    def draw_orders(self):
        if (self.trade_state.trade_mode != TradeMode.CLOSED):
            average_price_ypos = int(self.settings.screen_height - (self.trade_state.average_price -
                             self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            pygame.draw.line(self.screen, ORDER_COLOUR, (
                0, average_price_ypos), (self.settings.screen_width - CHART_RIGHT_SPACING, average_price_ypos))
            stop_ypos = int(self.settings.screen_height - (self.trade_state.stop_loss_price -
                            self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            draw_horizontal_dashed_line(self.screen, STOP_LOSS_COLOUR, (
                0, stop_ypos), (self.settings.screen_width - CHART_RIGHT_SPACING, stop_ypos))
            for order_price in self.trade_state.order_prices:
                order_price_ypos = int(self.settings.screen_height - (order_price -
                             self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
                draw_horizontal_dashed_line(self.screen, ORDER_COLOUR, (
                0, order_price_ypos), (self.settings.screen_width - CHART_RIGHT_SPACING, order_price_ypos))

        
    def draw_history(self):
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
