from typing import Union, Optional

from absl import logging

from src.model.enum.duration_type import DurationType
from src.model.object.note_component import NoteComponent
from src.model.object.primitive import Primitive
from src.model.object.rest_component import RestComponent


class MusicObject(object):
    def __init__(self, duration: DurationType, voice: int = 1,
                 type_component: Optional[Union[NoteComponent, RestComponent]] = None,
                 primitive_component: Optional[Primitive] = None):

        if MusicObject.__is_valid_duration(duration):
            self.duration = duration
        else:
            logging.error("Duration value \"{}\" is not valid".format(duration))

        self.voice = voice

        self.type_component = type_component
        self.primitive_component = primitive_component

    @staticmethod
    def __is_valid_duration(duration) -> bool:
        return isinstance(duration, DurationType)
