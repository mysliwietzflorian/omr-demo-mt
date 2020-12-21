from typing import List, Optional

from absl import logging

from src.helper.image_helper import ImageHelper
from src.model.object.measure import Measure
from src.model.object.primitive import Primitive


class StafflineDetector(object):
    PIXEL_BLACK = 0
    PIXEL_WHITE = 255

    def __init__(self, flags):
        self.__flags = flags

        self.staffspace_height = 0
        self.staffline_height = 0
        self.run_length_encoding: Optional[List[List[int]]]
        self.bounding_box: Optional[Primitive]

        self.lines_per_staff = 5
        self.fuzzy_pattern_threshold = 2
        self.same_staff_beginning_threshold = 25
        self.max_nr_of_staffs = 30

    def run(self, image) -> List[Measure]:
        logging.debug("Detect stafflines")

        self.__get_reference_lengths(image)
        valid_staves = self.__find_stave_locations(image)
        staves = self.__construct_stave_primitives(valid_staves)
        return staves

    def stave_height(self) -> int:
        return self.lines_per_staff * self.staffline_height + (self.lines_per_staff - 1) * self.staffspace_height

    def __get_reference_lengths(self, image):
        self.run_length_encoding = self.__compute_vertical_run_length(image)

        self.staffspace_height, self.staffline_height = \
            self.__run_consecutive_pairs_algorithm(image)

        self.bounding_box = self.__compute_bounding_box(image)

        ImageHelper.draw_primitives(image, [self.bounding_box], "Bounding Box", 5, self.__flags)

    def __compute_vertical_run_length(self, image) -> List[List[int]]:
        logging.debug("Compute run-length encoding")
        height, width = image.shape
        run_length_encoding = [[]] * width

        for j in range(width):
            counter = 0
            last_pixel_value = self.PIXEL_WHITE
            run_length_encoding[j] = []

            for i in range(height):
                value = image[i, j]

                if value != last_pixel_value:
                    (run_length_encoding[j]).append(counter)
                    last_pixel_value = value
                    counter = 0

                counter += 1

            (run_length_encoding[j]).append(counter)

        return run_length_encoding

    def __run_consecutive_pairs_algorithm(self, image):
        logging.debug("Compute reference lengths")

        height, _ = image.shape
        consecutive_pairs_hist = [0] * height
        lineheight_hist = [0] * height

        for vertical_run in self.run_length_encoding:
            if vertical_run:
                for first, second in zip(vertical_run, vertical_run[1:]):
                    consecutive_pairs_hist[first + second] += 1

                for element in vertical_run[1::2]:
                    lineheight_hist[element] += 1

        staff_element_height = consecutive_pairs_hist.index(max(consecutive_pairs_hist))
        staffline_height = lineheight_hist.index(max(lineheight_hist))
        staffspace_height = staff_element_height - staffline_height
        logging.debug("Reference staffspace_height = {}".format(staffspace_height))
        logging.debug("Reference staffline_height = {}".format(staffline_height))

        return staffspace_height, staffline_height

    def __compute_bounding_box(self, image):
        logging.debug("Compute bounding box")

        height, width = image.shape
        left = 0
        top = height - 1
        right = width - 1
        bottom = 0
        bottom_is_black = False

        while left < width and len(self.run_length_encoding[left]) == 1:
            left += 1

        while right >= 0 and len(self.run_length_encoding[right]) == 1:
            right -= 1

        for element in self.run_length_encoding:
            if element:
                top = min(top, element[0])

                if not bottom_is_black:
                    if len(element) % 2 == 0:
                        # run-length encoding has black pixel in last row
                        # therefore, is bottom = cols-1
                        bottom_is_black = True
                        bottom = width - 1

                    if len(element) == 1:
                        # only white pixels are in this vertical line
                        # therefore is this column ignored
                        continue

                    else:
                        bottom = max(bottom, height - element[-1])

        return Primitive((left, top), (right, bottom))

    def __find_stave_locations(self, image) -> List[Primitive]:
        logging.debug("Find stave locations")

        stave_begin_hist = self.__find_stave_patterns(image)
        found_staves = self.__find_most_probable_staves(stave_begin_hist)
        valid_staves = self.__validate_staves(found_staves)
        valid_staves.sort(key=lambda x: x.y1)
        return valid_staves

    def __find_stave_patterns(self, image) -> List[int]:
        stave_begin_hist = [0] * image.shape[0]

        for vertical_run in self.run_length_encoding:
            if len(vertical_run) <= 2 * self.lines_per_staff:
                continue

            y_marker = 0
            i = 0
            while i < len(vertical_run) - 1:

                comparing = vertical_run[i] + vertical_run[i + 1]
                y_offset = 0
                counter = 0
                while self.__is_staffspace_within_limits(comparing) and counter < self.lines_per_staff - 1:
                    y_offset += comparing
                    counter += 1
                    if i + 2 * counter + 1 < len(vertical_run):
                        comparing = vertical_run[i + 2 * counter] + vertical_run[i + 2 * counter + 1]

                if counter >= self.lines_per_staff - 2:
                    stave_begin_hist[y_marker] += 1
                    i += 8
                    y_marker += y_offset

                if i < len(vertical_run):
                    y_marker += vertical_run[i]
                i += 1
        return stave_begin_hist

    def __is_staffspace_within_limits(self, comparing: int) -> bool:
        comparator = self.staffspace_height + self.staffline_height
        return comparator - self.fuzzy_pattern_threshold <= comparing <= comparator + self.fuzzy_pattern_threshold

    def __find_most_probable_staves(self, stave_begin_counter: List[int]) -> List[int]:
        number = max(stave_begin_counter)
        found_staves: List[int] = []

        while number > self.same_staff_beginning_threshold and len(found_staves) < self.max_nr_of_staffs:
            y_marker = stave_begin_counter.index(number)
            stave_begin_counter[y_marker] = 0
            found_staves.append(y_marker)
            number = max(stave_begin_counter)

        return found_staves

    def __validate_staves(self, found_staves: List[int]) -> List[Primitive]:
        logging.debug("Validate and filter found stave primitives")

        valid_staves: List[Primitive] = \
            [self.__construct_primitive_from_starting_y(found_staves[0])]

        for starting_y in found_staves[1:]:
            prim = self.__construct_primitive_from_starting_y(starting_y)
            if not prim.is_overlapping_any(valid_staves):
                valid_staves.append(prim)

        return valid_staves

    def __construct_primitive_from_starting_y(self, y1: int) -> Primitive:
        return Primitive((self.bounding_box.x1, y1),
                         (self.bounding_box.x2, y1 + self.stave_height()))

    def __construct_stave_primitives(self, valid_staves: List[Primitive]) -> List[Measure]:
        staves: List[Measure] = []

        for idx in range(len(valid_staves)):
            staves.append(Measure(idx, valid_staves[idx]))
        return staves
