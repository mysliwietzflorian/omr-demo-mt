import json
from typing import List, Optional

from src.helper.image_helper import ImageHelper
from src.helper.json_encoder import JsonEncoder
from src.model.attribute.attribute import Attribute
from src.model.attribute.clef import Clef
from src.model.attribute.key import Key
from src.model.attribute.time import Time
from src.model.object.measure import Measure
from src.model.object.primitive import Primitive


class NotationGraph(object):
    def __init__(self, clef: Optional[Clef] = None, key: Optional[Key] = None, time: Optional[Time] = None):
        self.attributes = Attribute(clef, key, time)
        self.measures: List[Measure] = []
        self.primitive_component: Optional[Primitive]

    def draw_measures(self, image, flags):
        primitives: List[Primitive] = []
        for measure in self.measures:
            primitives.append(measure.primitive_component)
        ImageHelper.draw_primitives(image, primitives, "Measure", 6, flags)

    def to_json(self):
        return json.dumps(self.__dict__, cls=JsonEncoder, indent=4, sort_keys=True)

    def to_midi(self):
        # todo implementation needed
        pass

    def to_music_xml(self):
        # todo implementation needed
        pass
