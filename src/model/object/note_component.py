from typing import Optional

from src.model.enum.component_type import ComponentType
from src.model.enum.stem_direction import StemDirection
from src.model.enum.sustain_type import SustainType
from src.model.object.pitch import Pitch


class NoteComponent(object):
    def __init__(self, pitch: Optional[Pitch],
                 is_chord=False, is_grace=False, is_dotted=False,
                 stem: Optional[StemDirection] = None,
                 beam: Optional[SustainType] = None,
                 tie: Optional[SustainType] = None):
        self.type = ComponentType.NOTE
        self.pitch = pitch

        self.is_chord = is_chord
        self.is_grace = is_grace
        self.is_dotted = is_dotted

        self.stem = stem
        self.beam = beam
        self.tie = tie
