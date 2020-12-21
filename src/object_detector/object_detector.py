from absl import logging

from src.model.notation_graph import NotationGraph
from src.object_detector.music_object_detector import MusicObjectDetector
from src.object_detector.staffline_detector import StafflineDetector


class ObjectDetector(object):
    def __init__(self, flags):
        self.__flags = flags
        self.notation_graph = NotationGraph()

        self.__staffline_detector = StafflineDetector(self.__flags)
        self.__music_object_detector = MusicObjectDetector(self.__flags)
        self.__music_object_assembler = MusicObjectDetector(self.__flags)

    def run(self, image):
        if image is None:
            logging.warning("Image for object detector is not defined")
            return

        self.notation_graph.measures = self.__staffline_detector.run(image)
        self.notation_graph.draw_measures(image, self.__flags)

        stave_height = self.__staffline_detector.stave_height()
        objects = self.__music_object_detector.run(image, stave_height)
        return objects
