import os
from datetime import datetime
from constants import *
import pygame
from load_data import load_data


class CacheManagement:
    def __init__(self, state):
        self.state = state
        data = load_data(self.state.date_time, 5)

    def manage(self):
        pass