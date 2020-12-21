from absl import logging

from src.model.enum.pitch_step import PitchStep


class Pitch(object):
    def __init__(self, step: PitchStep, alteration=0, octave=4):
        if Pitch.__is_valid_step(step):
            self.step = step
        else:
            logging.error("Pitch step value \"{}\" is not valid".format(step))

        if Pitch.__is_valid_semitone(alteration):
            self.alteration = alteration
        else:
            logging.error("Pitch alteration value \"{}\" is not valid".format(alteration))

        self.octave = octave

    @staticmethod
    def __is_valid_step(step) -> bool:
        return isinstance(step, PitchStep)

    @staticmethod
    def __is_valid_semitone(alteration) -> bool:
        valid_alterations = [-1, 0, 1]
        return alteration in valid_alterations
