import pandas as pd
import MetaTrader5 as mt5
from mt5 import initConection
from variable import *


def getData():
    initConection()
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, trainCandles)
    print('Download of data done!')
    mt5.shutdown()

    rates_frame = pd.DataFrame(rates)
    rates_frame.rename(columns={"time": "Date",
                                "open": "Open",
                                "high": "High",
                                "low": "Low",
                                "close": "Close",
                                "tick_volume": "Volume"},
                       inplace=True)

    rates_frame.drop(columns=["spread", "real_volume"], inplace=True)
    rates_frame.set_index("Date", inplace=True)
    rates_frame.index = pd.to_datetime(rates_frame.index, unit='s')

    return rates_frame


def downloadLastData():
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, stepsBack)
    rates_frame = pd.DataFrame(rates)
    rates_frame.rename(columns={"time": "Date",
                                "open": "Open",
                                "high": "High",
                                "low": "Low",
                                "close": "Close",
                                "tick_volume": "Volume"},
                       inplace=True)

    rates_frame.set_index("Date", inplace=True)
    rates_frame.drop(columns=["spread", "real_volume"], inplace=True)
    rates_frame.index = pd.to_datetime(rates_frame.index, unit='s')

    return rates_frame


def getDataBT(utc_from, utc_to, symbol=symbol):
    initConection()
    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, utc_from, utc_to)
    mt5.shutdown()

    rates_frame = pd.DataFrame(rates)
    rates_frame.rename(columns={"time": "Date",
                                "open": "Open",
                                "high": "High",
                                "low": "Low",
                                "close": "Close",
                                "tick_volume": "Volume"},
                       inplace=True)

    rates_frame.drop(columns=["spread", "real_volume"], inplace=True)
    rates_frame.set_index("Date", inplace=True)
    rates_frame.index = pd.to_datetime(rates_frame.index, unit='s')

    return rates_frame
