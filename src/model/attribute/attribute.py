from typing import Optional

from src.model.attribute.clef import Clef
from src.model.attribute.key import Key
from src.model.attribute.time import Time


class Attribute(object):
    def __init__(self, clef: Optional[Clef] = None, key: Optional[Key] = None, time: Optional[Time] = None):
        self.clef = clef
        self.key = key
        self.time = time
