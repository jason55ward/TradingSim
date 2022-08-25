import os
import glob
from constants import *


def load_data(date_time, minutes):
    """
    Reads the data from the files
    """
    def get_filename(file_list, file_search):
        for filename in file_list:
            if file_search in filename.lower():
                return filename

    def first_substring(the_list, substring):
        return [idx for idx, s in enumerate(the_list) if substring in s][0]

    currency_dir = os.path.join(DATA_DIR, CURRENCY_PAIR)
    path = os.path.join('.', currency_dir, "*")
    filenames = glob.glob(path)
    one_minute_index = first_substring(filenames, 'bid_1_m_2020-2022')
    five_minute_index = first_substring(filenames, 'bid_5_m_2020-2022')
    fifteen_minute_index = first_substring(filenames, 'bid_15_m_2020-2022')
    one_hour_index = first_substring(filenames, 'bid_1_hour_2020-2022')
    four_hour_index = first_substring(filenames, 'bid_4_hour_2020-2022')
    daily_index = first_substring(filenames, 'bid_1_d_2020-2022')

    with open(filenames[one_minute_index]) as bid_file:
        self.one_minute_data = tuple(bid_file.readlines())
    bid = self.one_minute_data
    ask = self.bid

    with open(filenames[five_minute_index]) as bid_file:
        five_minute_data = tuple(bid_file.readlines())
    with open(filenames[fifteen_minute_index]) as bid_file:
        fifteen_minute_data = tuple(bid_file.readlines())
    with open(filenames[one_hour_index]) as bid_file:
        one_hour_data = tuple(bid_file.readlines())
    with open(filenames[four_hour_index]) as bid_file:
        four_hour_data = tuple(bid_file.readlines())
    with open(filenames[daily_index]) as bid_file:
        daily_data = tuple(bid_file.readlines())

    return [one_minute_data, five_minute_data, self.fifteen_minute_data, self.one_hour_data, self.four_hour_data, self.daily_data]
