import os
import datetime
from constants import *

class Config():
    def __init__(self, config_file, history_file):
        self.config_file = config_file
        self.history_file = history_file

    def read_config(self):
        date_time = DEFAULT_DATE_TIME
        equity = DEFAULT_EQUITY
        if os.path.exists(self.config_file):
            with open(self.config_file) as config_file:
                data = config_file.readlines()
                if data:
                    date_time = data[0].split('=')[1].rstrip()
                    equity = float(data[1].split('=')[1].rstrip())
            # if os.path.exists(self.history_file):
            #     with open(self.history_file) as config_file:
            #         data = config_file.readlines()
            #         self.history = list(hist.rstrip().split() for hist in data if hist != "")
        return date_time, equity

    def write_config(self, date_time, equity, history=[]):
        with open(self.config_file, "w") as config_file:
            config_file.write(f'date_time={date_time}\n')
            config_file.write(f'equity={equity:.2f}\n')
        # with open(self.history_file, "w") as history_file:
        #     for hist in history:
        #         history_file.write("{0} {1} {2} {3} {4}\n".format(
        #             hist[0], hist[1], hist[2], hist[3], hist[4]))
