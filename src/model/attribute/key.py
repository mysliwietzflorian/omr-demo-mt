from absl import logging

from src.model.enum.mode_type import ModeType


class Key(object):
    def __init__(self, fifths=0, mode: ModeType = ModeType.MAJOR, cancel=0):
        if Key.__is_valid_mode(mode):
            self.mode = mode
        else:
            logging.error("Mode value \"{}\" is not valid".format(mode))

        self.fifths = fifths
        self.cancel = cancel

    @staticmethod
    def __is_valid_mode(mode) -> bool:
        return isinstance(mode, ModeType) or None
