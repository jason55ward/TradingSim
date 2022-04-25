from enum import Enum


class TradeMode(Enum):
    """Enum for selecting the mode of the trade"""
    BUY = 1
    SELL = 2
    CLOSED = 3


class TradeState:
    """"Keeps track of the current state"""
    equity = 10000
    profit = 0
    trade_mode = TradeMode.CLOSED
    order_price = 0
    position_size = 0
    stop_loss_price = 0
    pips = 0
    candle_number = 0


class OHLC(Enum):
    """Enum for picking Open High Low Close data from the bid and ask lists"""
    OPENINDEX = 1
    HIGHINDEX = 2
    LOWINDEX = 3
    CLOSEINDEX = 4