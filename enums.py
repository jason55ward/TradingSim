from enum import Enum


class TradeMode(Enum):
    """Enum for selecting the mode of the trade"""
    BUY = 1
    SELL = 2
    CLOSED = 3


class OHLC(Enum):
    """Enum for picking Open High Low Close data from the bid and ask lists"""
    OPENINDEX = 1
    HIGHINDEX = 2
    LOWINDEX = 3
    CLOSEINDEX = 4
