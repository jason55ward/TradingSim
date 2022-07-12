from constants import *

class TextDisplay():
    def __init__(self, screen, font, trade_state, settings):
        self.screen = screen
        self.font = font
        self.trade_state = trade_state
        self.settings = settings

    def draw_info_text(self):
        last_candle_data_text = self.font.render(
            self.settings.bid[self.settings.last_candle], 1, (FONT_COLOUR))
        self.screen.blit(last_candle_data_text, (20, 20))
        equity_text = self.font.render(
            "Pre-Trade Balance: " + str("%.2f" % (self.trade_state.equity)), 1, (FONT_COLOUR))
        self.screen.blit(equity_text, (20, 45))
        equity_text = self.font.render("Equity: " + str("%.2f" % (
            self.trade_state.equity + self.trade_state.profit)), 1, (FONT_COLOUR))
        self.screen.blit(equity_text, (20, 70))
        profit_text = self.font.render(
            "Profit: " + str("%.2f" % self.trade_state.profit), 1, (FONT_COLOUR))
        self.screen.blit(profit_text, (20, 95))
        trade_mode_text = self.font.render(
            "Trade Mode: " + str(self.trade_state.trade_mode.name), 1, (FONT_COLOUR))
        self.screen.blit(trade_mode_text, (20, 120))
        pips_text = self.font.render(
            "Pips: " + str("%.1f" % self.trade_state.pips), 1, (FONT_COLOUR))
        self.screen.blit(pips_text, (20, 145))
        position_size_text = self.font.render(
            "Position Size: " + str("%.2f" % self.trade_state.position_size), 1, (FONT_COLOUR))
        self.screen.blit(position_size_text, (20, 170))
        help_text = self.font.render(
            "Press F1 to toggle help info ", 1, (FONT_COLOUR))
        self.screen.blit(help_text, (20, 195))

    def displayHelp(self):
        text1 = "Move 1 candle: use left and right arrow."
        text2 = "Move multiple candles: use PageUp and PageDown."
        text3 = "Buy/Sell: b/s."
        text5 = "Change Zoom: 1-4."
        text6 = "Exit: Escape."
        text1_text = self.font.render(text1, 1, (FONT_COLOUR))
        text2_text = self.font.render(text2, 1, (FONT_COLOUR))
        text3_text = self.font.render(text3, 1, (FONT_COLOUR))
        text4_text = self.font.render(text4, 1, (FONT_COLOUR))
        text5_text = self.font.render(text5, 1, (FONT_COLOUR))
        text6_text = self.font.render(text6, 1, (FONT_COLOUR))
        self.screen.blit(text1_text, (700, 60))
        self.screen.blit(text2_text, (700, 85))
        self.screen.blit(text3_text, (700, 110))
        self.screen.blit(text4_text, (700, 135))
        self.screen.blit(text5_text, (700, 160))
        self.screen.blit(text6_text, (700, 185))
