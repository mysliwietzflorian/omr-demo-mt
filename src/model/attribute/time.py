from typing import Optional

from absl import logging

from src.model.enum.time_symbol_type import TimeSymbolType


class Time(object):
    def __init__(self, beats=4, beats_type=4, time_symbol: Optional[TimeSymbolType] = None):
        self.beats = beats
        self.beats_type = beats_type

        if Time.__is_valid_time_symbol(time_symbol):
            self.time_symbol = time_symbol
        else:
            logging.error("Time-Symbol value \"{}\" is not valid".format(time_symbol))

    @staticmethod
    def __is_valid_time_symbol(time_symbol) -> bool:
        return isinstance(time_symbol, TimeSymbolType) or None
