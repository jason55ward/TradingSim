import pygame
from pygame.locals import *
from orders import Orders
from constants import *
from enums import TradeMode, OHLC

class Events():
    def __init__(self, trade_state, settings, config):
        self.settings = settings
        self.config = config
        self.trade_state = trade_state
        self.orders = Orders(trade_state=trade_state, settings=settings,)


    def process_events(self):
        events = pygame.event.get(pump=True)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.config.write_config(self.settings.last_candle, self.settings.history)
                    self.settings.done = True
                if event.key == pygame.K_DOWN:
                    self.settings.chart_pip_height += 20
                if event.key == pygame.K_UP:
                    self.settings.chart_pip_height -= 20
                if event.key == pygame.K_LEFT:
                    self.settings.last_candle -= self.settings.minutes
                    if self.settings.last_candle < self.settings.max_candles:
                        self.settings.last_candle = self.settings.max_candles
                if event.key == pygame.K_RIGHT:
                    self.settings.last_candle += self.settings.minutes
                if event.key == pygame.K_PAGEUP:
                    self.settings.last_candle += self.settings.minutes
                if event.key == pygame.K_PAGEDOWN:
                    self.settings.last_candle -= self.settings.minutes
                    if self.settings.last_candle < self.settings.max_candles:
                        self.settings.last_candle = self.settings.max_candles
                if event.key == pygame.K_h:
                    self.settings.show_history = not self.settings.show_history
                if event.key == pygame.K_b:
                    self.orders.trade(order_type=TradeMode.BUY)
                if event.key == pygame.K_s:
                    self.orders.trade(order_type=TradeMode.SELL)
                if event.key == pygame.K_c:
                    self.orders.close()
                if event.key == pygame.K_F1:
                    self.settings.showing_help = not self.settings.showing_help
                if event.key == pygame.K_1:
                    self.settings.minutes = ONE_MINUTE
                    self.data = self.settings.one_minute_data
                if event.key == pygame.K_2:
                    self.settings.minutes = FIVE_MINUTES
                    self.data = self.settings.five_minute_data
                if event.key == pygame.K_3:
                    self.settings.minutes = FIFTEEN_MINUTES
                    self.data = self.settings.fifteen_minute_data
                if event.key == pygame.K_4:
                    self.settings.minutes = ONE_HOUR
                    self.data = self.settings.one_hour_data
                if event.key == pygame.K_5:
                    self.settings.minutes = FOUR_HOUR
                    self.data = self.settings.four_hour_data
                if event.key == pygame.K_6:
                    self.settings.minutes = ONE_DAY
                    self.data = self.settings.daily_data
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
                self.config.write_config(self.settings.last_candle, self.settings.history)
                self.settings.done = True
