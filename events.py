import pygame
from pygame.locals import *
from orders import Orders
from constants import *
from enums import TradeMode, OHLC
import datetime

class Events():
    def __init__(self, state, settings, config):
        self.settings = settings
        self.config = config
        self.state = state
        self.orders = Orders(state=state, settings=settings,)


    def process_events(self):
        events = pygame.event.get(pump=True)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.config.write_config(self.state.date_time, self.state.equity)
                    self.state.done = True
                if event.key == pygame.K_DOWN:
                    self.settings.chart_pip_height += 20
                if event.key == pygame.K_UP:
                    self.settings.chart_pip_height -= 20
                if event.key == pygame.K_LEFT:
                    self.state.prior_day()
                if event.key == pygame.K_RIGHT:
                    self.state.next_bar()
                if event.key == pygame.K_l:
                    self.state.date_time += datetime.timedelta(days=1)
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
                    self.state.time_frame = ONE_MINUTE
                    #self.state.data = self.settings.one_minute_data
                if event.key == pygame.K_2:
                    self.state.time_frame = FIVE_MINUTES
                    #self.state.data = self.settings.five_minute_data
                if event.key == pygame.K_3:
                    self.state.time_frame = FIFTEEN_MINUTES
                    #self.state.data = self.settings.fifteen_minute_data
                if event.key == pygame.K_4:
                    self.state.time_frame = ONE_HOUR
                    #self.state.data = self.settings.one_hour_data
                if event.key == pygame.K_5:
                    self.state.time_frame = FOUR_HOUR
                    #self.state.data = self.settings.four_hour_data
                if event.key == pygame.K_6:
                    self.state.time_frame = ONE_DAY
                    #self.state.data = self.state.daily_data
                if event.key == pygame.K_p:
                    price = (self.settings.screen_height - pygame.mouse.get_pos()[1] - CHART_TOP_Y_OFFSET)/self.settings.factor + self.settings.min_height
                    self.state.support.append(price)
                if event.key == pygame.K_i:
                    self.state.support.clear()
                if event.key == pygame.K_o:
                    self.state.support.pop()
                if event.key == pygame.K_k:
                    price = (self.settings.screen_height - pygame.mouse.get_pos()[1] - CHART_TOP_Y_OFFSET)/self.settings.factor + self.settings.min_height
                    self.state.stop_loss_price = price
                if event.key == pygame.K_KP_PLUS:
                    self.settings.candle_width += 1
                if event.key == pygame.K_KP_MINUS:
                    self.settings.candle_width -= 1
                if event.key == pygame.K_EQUALS:
                    self.settings.time_speed += 10
                if event.key == pygame.K_MINUS:
                    self.settings.time_speed -= 10
                    if self.settings.time_speed < 1:
                        self.settings.time_speed = 1
                if event.key == pygame.K_PAUSE:
                    self.state.paused = not self.state.paused
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                rel = pygame.mouse.get_rel()[0]
                move = 0
                if rel > 0:
                    move = -15
                elif rel < 0:
                    move = +15
                #self.state.data_index += move
            if event.type is QUIT:
                self.config.write_config(self.state.date_time, self.state.equity, self.state.history)
                self.state.done = True
