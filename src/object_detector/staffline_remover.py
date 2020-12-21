from typing import List, Tuple

from absl import logging

from src.helper.image_helper import ImageHelper
from src.model.object.primitive import Primitive
from src.object_detector.stable_path_finder import StablePathFinder
from src.object_detector.staffline_detector import StafflineDetector


# todo EXPERIMENTAL!
class StafflineRemover(object):
    PIXEL_BLACK = 0
    PIXEL_WHITE = 255

    def __init__(self, flags):
        self.__flags = flags
        self.__staffline_detector = StafflineDetector(self.__flags)

        self.staffspace_height = 0
        self.staffline_height = 0
        self.run_length_encoding: List[List[int]]

        self.bounding_box: Primitive
        self.graph_weights: List[List[Tuple[int, int, int]]]
        self.stable_paths = None

    def run(self, image):
        logging.debug("(EXPERIMENTAL) Remove stafflines")
        self.__init_staffline_detector(image)

        # preprocessing
        self.__compute_graph_weights(image)

        # main cycle
        self.__compute_stable_paths(image)
        # todo self.__validate_paths()
        # todo self.__detect_staffline()

        # postprocessing
        # todo self.__uncross_stafflines()
        # todo self.__group_stafflines_in_staves()
        # todo self.__smooth_and_trim_stafflines()

    def __init_staffline_detector(self, image):
        self.__staffline_detector.run(image)
        self.staffspace_height = self.__staffline_detector.staffspace_height
        self.staffline_height = self.__staffline_detector.staffline_height
        self.run_length_encoding = self.__staffline_detector.run_length_encoding
        self.bounding_box = self.__staffline_detector.bounding_box

    def __compute_graph_weights(self, image):
        logging.debug("Compute graph weights")

        height, width = image.shape
        self.graph_weights = [[(0, 0, 0)] * width for i in range(height)]

        for x in range(width - 1):
            for y in range(height):
                horizontal = self.__weight_function(image, (x, y), (x + 1, y))
                upwards = float('inf') if y <= 0 else self.__weight_function(image, (x, y), (x + 1, y - 1))
                downwards = float('inf') if y >= height - 1 else self.__weight_function(image, (x, y), (x + 1, y + 1))

                self.graph_weights[y][x] = (upwards, horizontal, downwards)

    def __weight_function(self, image, point1: Tuple[int, int], point2: Tuple[int, int]) -> int:
        # todo evaluate further weight function from papers
        weight = 2  # base weight (black to black pixel)
        value1 = image[point1[1]][point1[0]]
        value2 = image[point2[1]][point2[0]]

        if value1 != value2:
            weight = 5  # black to white or white to black pixel
        elif value1 == self.PIXEL_WHITE:
            weight = 8  # white to white pixel

        if point1[1] != point2[1]:
            weight += 1  # diagonal path leading to bigger cost

        return weight

    def __compute_stable_paths(self, image):
        logging.debug("Compute stable paths")

        self.stable_paths: List[List[int]] = []
        height, width = image.shape

        goal = width - 1
        # todo use bounding_box as borders
        # goal = self.bounding_box.y2
        result = StablePathFinder(image, self.graph_weights).find_path((0, 13), goal)

        colored_image = ImageHelper.get_colored_image(image)
        for pixel in result:
            colored_image[pixel[1]][pixel[0]] = (0, 0, 255)
        ImageHelper.write_image(colored_image, "06b_stable_path", self.__flags)
