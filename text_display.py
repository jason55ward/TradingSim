from constants import *

class TextDisplay():
    def __init__(self, screen, state, settings):
        self.screen = screen
        self.state = state
        self.settings = settings

    def draw_info_text(self):
        y_pos = 20
        y_increment = 25
        data_text = self.settings.font.render(
            self.state.minute_data[self.state.minute_index].replace('\n',''), 1, (FONT_COLOUR))
        self.screen.blit(data_text, (20, y_pos))
        y_pos+=y_increment
        date_time_text = self.settings.font.render(
            str(self.state.date_time), 1, (FONT_COLOUR))
        self.screen.blit(date_time_text, (20, y_pos))
        y_pos+=y_increment
        equity_text = self.settings.font.render(f"Pre-Trade Balance: {'%.2f' % self.state.equity}", 1, (FONT_COLOUR))
        self.screen.blit(equity_text, (20, y_pos))
        y_pos+=y_increment
        equity_text = self.settings.font.render(f"Equity: {'%.2f' % (self.state.equity + self.state.profit)}", 1, (FONT_COLOUR))
        self.screen.blit(equity_text, (20, y_pos))
        y_pos+=y_increment
        profit_text = self.settings.font.render(f"Profit: {'%.2f' % self.state.profit}", 1, (FONT_COLOUR))
        self.screen.blit(profit_text, (20, y_pos))
        y_pos+=y_increment
        trade_mode_text = self.settings.font.render(f"Trade Mode: {self.state.trade_mode.name}", 1, (FONT_COLOUR))
        self.screen.blit(trade_mode_text, (20, y_pos))
        y_pos+=y_increment
        position_size_text = self.settings.font.render(f"Position Size: {'%.2f' % self.state.position_size}", 1, (FONT_COLOUR))
        self.screen.blit(position_size_text, (20, y_pos))
        y_pos+=y_increment
        help_text = self.settings.font.render("Press F1 to toggle help info ", 1, (FONT_COLOUR))
        self.screen.blit(help_text, (20, y_pos))
        y_pos+=y_increment
        average_price_text = self.settings.font.render(f"Average Price: {self.state.average_price}", 1, (FONT_COLOUR))
        self.screen.blit(average_price_text, (20, y_pos))
        y_pos+=y_increment
        timeframe_text = self.settings.font.render(f"Timeframe: {self.state.time_frame}", 1, (FONT_COLOUR))
        self.screen.blit(timeframe_text, (20, y_pos))

    def displayHelp(self):
        text1 = "Move 1 candle: use left and right arrow."
        text2 = "Move 3 candles: use PageUp and PageDown."
        text3 = "Buy/Sell: b/s."
        text4 = "Change Timeframe: 1-6."
        text5 = "Exit: Escape."
        text1_text = self.settings.font.render(text1, 1, (FONT_COLOUR))
        text2_text = self.settings.font.render(text2, 1, (FONT_COLOUR))
        text3_text = self.settings.font.render(text3, 1, (FONT_COLOUR))
        text4_text = self.settings.font.render(text4, 1, (FONT_COLOUR))
        text5_text = self.settings.font.render(text5, 1, (FONT_COLOUR))
        self.screen.blit(text1_text, (700, 60))
        self.screen.blit(text2_text, (700, 85))
        self.screen.blit(text3_text, (700, 110))
        self.screen.blit(text4_text, (700, 135))
        self.screen.blit(text5_text, (700, 160))
