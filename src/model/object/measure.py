from typing import List, Optional

from src.model.attribute.attribute import Attribute
from src.model.attribute.clef import Clef
from src.model.attribute.key import Key
from src.model.attribute.time import Time
from src.model.object.music_object import MusicObject
from src.model.object.primitive import Primitive


class Measure(object):
    def __init__(self, number: int, primitive_component: Optional[Primitive] = None,
                 clef: Optional[Clef] = None, key: Optional[Key] = None, time: Optional[Time] = None):
        self.number: int = number
        self.attributes = Attribute(clef, key, time)
        self.objects: List[MusicObject] = []
        self.primitive_component = primitive_component
