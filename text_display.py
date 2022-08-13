from constants import *

class TextDisplay():
    def __init__(self, screen, trade_state, settings):
        self.screen = screen
        self.trade_state = trade_state
        self.settings = settings

    def draw_info_text(self):
        last_candle_data_text = self.settings.font.render(
            self.settings.data[self.settings.last_candle].replace('\n',''), 1, (FONT_COLOUR))
        self.screen.blit(last_candle_data_text, (20, 20))
        equity_text = self.settings.font.render(f"Pre-Trade Balance: {'%.2f' % self.trade_state.equity}", 1, (FONT_COLOUR))
        self.screen.blit(equity_text, (20, 45))
        equity_text = self.settings.font.render(f"Equity: {'%.2f' % (self.trade_state.equity + self.trade_state.profit)}", 1, (FONT_COLOUR))
        self.screen.blit(equity_text, (20, 70))
        profit_text = self.settings.font.render(f"Profit: {'%.2f' % self.trade_state.profit}", 1, (FONT_COLOUR))
        self.screen.blit(profit_text, (20, 95))
        trade_mode_text = self.settings.font.render(f"Trade Mode: {self.trade_state.trade_mode.name}", 1, (FONT_COLOUR))
        self.screen.blit(trade_mode_text, (20, 120))
        position_size_text = self.settings.font.render(f"Position Size: {'%.2f' % self.trade_state.position_size}", 1, (FONT_COLOUR))
        self.screen.blit(position_size_text, (20, 145))
        help_text = self.settings.font.render("Press F1 to toggle help info ", 1, (FONT_COLOUR))
        self.screen.blit(help_text, (20, 170))
        average_price_text = self.settings.font.render(f"Average Price: {self.trade_state.average_price}", 1, (FONT_COLOUR))
        self.screen.blit(average_price_text, (20, 195))
        timeframe_text = self.settings.font.render(f"Timeframe: {self.settings.minutes}", 1, (FONT_COLOUR))
        self.screen.blit(timeframe_text, (20, 220))

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
