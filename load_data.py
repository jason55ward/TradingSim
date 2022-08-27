import os
import glob
from constants import *
import zipfile
from dateutil import parser

#20110131 235756;1286.000000;0
def load_ticks(date_time):
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

#20130102 060000;1423.000000;1442.750000;1423.000000;1440.000000;0
def load_minutes(date_time):
    currency_dir = os.path.join(DATA_DIR, CURRENCY_PAIR)
    minute_dir = os.path.join(currency_dir, ONE_MINUTE_DIR_NAME)
    minute_zip_files = glob.glob(os.path.join('.', minute_dir, "*"))

    minute_zip_filename = f"{CURRENCY_PAIR}_M1{date_time.year}.zip"
    minute_zip_file_path = os.path.join(minute_dir, minute_zip_filename)
    if not os.path.exists(minute_zip_file_path):
        raise FileNotFoundError((f"Cant't find file {minute_zip_file_path}"))
    prior_year_minute_zip_filename = f"{CURRENCY_PAIR}_M1{date_time.year-1}.zip"
    prior_year_minute_zip_file_path = os.path.join(minute_dir, prior_year_minute_zip_filename)
    if date_time.year != OLDEST_DATA_YEAR and not os.path.exists(prior_year_minute_zip_file_path):
        raise FileNotFoundError((f"Cant't find file {prior_year_minute_zip_file_path}"))

    prior_minute_file = f"DAT_NT_{CURRENCY_PAIR}_M1_{date_time.year-1}.csv"
    minute_file = f"DAT_NT_{CURRENCY_PAIR}_M1_{date_time.year}.csv"
    
    minutes = []
    if date_time.year != OLDEST_DATA_YEAR:
        with zipfile.ZipFile(prior_year_minute_zip_file_path) as thezip:
            with thezip.open(prior_minute_file, mode='r') as thefile:
                for line in thefile:
                    minutes.append(line.decode("utf-8"))

    with zipfile.ZipFile(minute_zip_file_path) as thezip:
        with thezip.open(minute_file, mode='r') as thefile:
            for line in thefile:
                minutes.append(line.decode("utf-8"))

    return minutes
