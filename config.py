import os

class Config():
    def __init__(self, config_file, history_file, trade_state):
        self.config_file = config_file
        self.history_file = history_file
        self.trade_state = trade_state

    def read_config(self):
        equity = 0.0
        last_candle = 0
        if os.path.exists(self.config_file):
            with open(self.config_file) as config_file:
                data = config_file.readlines()
                if len(data) == 2:
                    equity = float(data[0].split('=')[1].rstrip())
                    last_candle = int(data[1].split('=')[1].rstrip())
            if os.path.exists(self.history_file):
                with open(self.history_file) as config_file:
                    data = config_file.readlines()
                    self.history = list(hist.rstrip().split() for hist in data if hist != "")
        return equity, last_candle

    def write_config(self, last_candle, history):
        with open(self.config_file, "w") as config_file:
            config_file.write(f'equity={self.trade_state.equity:.2f}\n')
            config_file.write(f'last_candle={last_candle}\n')
        with open(self.history_file, "w") as history_file:
            for hist in history:
                history_file.write("{0} {1} {2} {3} {4}\n".format(
                    hist[0], hist[1], hist[2], hist[3], hist[4]))
