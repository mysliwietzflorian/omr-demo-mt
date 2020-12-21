from typing import Optional

from absl import logging

from src.model.enum.clef_sign_type import ClefSignType


class Clef(object):
    def __init__(self, sign: Optional[ClefSignType] = ClefSignType.G, line: Optional[int] = None, octave_change=False):
        if Clef.__is_valid_sign(sign):
            self.sign = sign
        else:
            logging.error("Clef value \"{}\" is not valid".format(sign))

        self.line = line
        self.has_octave_change = octave_change

    @staticmethod
    def __is_valid_sign(sign) -> bool:
        return isinstance(sign, ClefSignType) or None
