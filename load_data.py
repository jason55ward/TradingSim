import os
import glob
from constants import *
import zipfile
from dateutil import parser


def load_ticks(date_time):
    date_time = parser.parse(date_time)
    currency_dir = os.path.join(DATA_DIR, CURRENCY_PAIR)
    tick_dir = os.path.join(currency_dir, TICK_DIR_NAME)
    tick_zip_files = glob.glob(os.path.join('.', tick_dir, "*"))
    tick_zip_filename = f"{CURRENCY_PAIR}_T_BID{date_time.year}{str(date_time.month).rjust(2,'0')}.zip"
    tick_zip_file_path = os.path.join(tick_dir, tick_zip_filename)
    if not os.path.exists(tick_zip_file_path):
        raise FileNotFoundError((f"Cant't find file {tick_zip_file_path}"))

    tick_file = f"DAT_NT_{CURRENCY_PAIR}_T_BID_{date_time.year}{str(date_time.month).rjust(2,'0')}.csv"
    
    ticks = []
    with zipfile.ZipFile(tick_zip_file_path) as thezip:
        with thezip.open(tick_file, mode='r') as thefile:
            for line in thefile:
                ticks.append(line.decode("utf-8"))

    return ticks

def load_minutes(date_time):
    date_time = parser.parse(date_time)
    currency_dir = os.path.join(DATA_DIR, CURRENCY_PAIR)
    one_minute_dir = os.path.join(currency_dir, ONE_MINUTE_DIR_NAME)
    one_minute_zip_files = glob.glob(os.path.join('.', one_minute_dir, "*"))

    one_min_zip_filename = f"{CURRENCY_PAIR}_M1{date_time.year}.zip"
    one_min_zip_file_path = os.path.join(one_minute_dir, one_min_zip_filename)
    if not os.path.exists(one_min_zip_file_path):
        raise FileNotFoundError((f"Cant't find file {one_min_zip_file_path}"))
    prior_one_min_zip_filename = f"{CURRENCY_PAIR}_M1{date_time.year-1}.zip"
    prior_one_min_zip_file_path = os.path.join(one_minute_dir, prior_one_min_zip_filename)
    if date_time.year != OLDEST_DATA_YEAR and not os.path.exists(prior_one_min_zip_file_path):
        raise FileNotFoundError((f"Cant't find file {prior_one_min_zip_file_path}"))

    prior_one_min_file = f"DAT_NT_{CURRENCY_PAIR}_M1_{date_time.year-1}.csv"
    one_min_file = f"DAT_NT_{CURRENCY_PAIR}_M1_{date_time.year}.csv"
    
    minutes = []
    if date_time.year != OLDEST_DATA_YEAR:
        with zipfile.ZipFile(prior_one_min_zip_file_path) as thezip:
            with thezip.open(prior_one_min_file, mode='r') as thefile:
                for line in thefile:
                    minutes.append(line.decode("utf-8"))

    with zipfile.ZipFile(one_min_zip_file_path) as thezip:
        with thezip.open(one_min_file, mode='r') as thefile:
            for line in thefile:
                minutes.append(line.decode("utf-8"))

    return minutes
