from constants import *
from enums import TradeMode, OHLC
import pygame

class Chart():
    def __init__(self, screen, trade_state, settings):
        self.screen = screen
        self.trade_state = trade_state
        self.settings = settings

    def calc_high_low_price(self):
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

    def draw_price_lines(self):
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
        
    def draw_chart_data(self):
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
    
    def draw_orders(self):
        if (self.trade_state.trade_mode != TradeMode.CLOSED):
            order_ypos = int(self.settings.screen_height - (self.trade_state.order_price -
                             self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            stop_ypos = int(self.settings.screen_height - (self.trade_state.stop_loss_price -
                            self.settings.min_height) * self.settings.factor) - CHART_TOP_Y_OFFSET
            draw_horizontal_dashed_line(self.screen, ORDER_COLOUR, (
                0, order_ypos), (self.settings.screen_width - CHART_RIGHT_SPACING, order_ypos))
            draw_horizontal_dashed_line(self.screen, STOP_LOSS_COLOUR, (
                0, stop_ypos), (self.settings.screen_width - CHART_RIGHT_SPACING, stop_ypos))
        
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
