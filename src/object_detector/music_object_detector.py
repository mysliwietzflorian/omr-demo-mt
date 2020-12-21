import json
import math
from typing import List, Tuple, Dict, Optional, Any

import cv2
import numpy as np
from absl import logging

from src.model.object.primitive import Primitive


class MusicObjectDetector(object):
    def __init__(self, flags):
        self.__flags = flags
        self.__resize_ratio = 0.0
        self.template_locations = None

    def run(self, image, stave_height: int):
        logging.debug("Detect music objects")

        with open("resources/templates/templates.json") as json_file:
            self.template_locations = json.load(json_file)
            self.__resize_ratio = self.__calculate_stave_height_ratio(stave_height)

            attributes = self.__find_from_templates(image, "attributes")
            objects = self.__find_from_templates(image)

            return {
                "attributes": attributes,
                "objects": objects
            }

    def __calculate_stave_height_ratio(self, stave_height: int):
        return stave_height / self.template_locations["meta"]["stave_height"]

    def __find_from_templates(self, image, key: str = "objects") -> Dict[str, Dict[str, List[Primitive]]]:
        objects: Dict[str, Dict[str, List[Primitive]]] = {}

        for o in self.template_locations[key]:
            objects[o] = self.__find_music_objects(image, o, key, key != "objects")
        return objects

    def __find_music_objects(self, image, attr_type: str, key: str = "objects", validate_objects: bool = False) -> Dict[
        str, List[Primitive]]:

        objects: Dict[str, List[Primitive]] = {}

        for obj in self.template_locations[key][attr_type]:
            template = self.__get_template_image(obj["path"], "{}_{}".format(attr_type, obj["name"]))
            if template is None:
                continue

            candidate_primitives = self.__find_template_candidates(image, template, obj["threshold"])
            if validate_objects:
                candidate_primitives = self.__validate_primitives(candidate_primitives)

            if len(candidate_primitives) > 0:
                objects[obj["name"]] = candidate_primitives

        return objects

    def __get_template_image(self, path: str, template_name: str) -> Optional[Any]:
        template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            logging.warning("Image file for \"{}\" not found".format(template_name))
            return None
        height, width = template.shape

        # todo consider possibility for individual resizes for each template
        if math.isclose(self.__resize_ratio, 1.0):
            return template
        else:
            new_size = (int(width * self.__resize_ratio), int(height * self.__resize_ratio))
            return cv2.resize(template, new_size)

    def __find_template_candidates(self, image, template, threshold: float) -> List[Primitive]:
        primitives: List[Primitive] = []
        height, width = template.shape

        result = cv2.matchTemplate(image, template, cv2.TM_SQDIFF_NORMED)
        locations = np.where(result <= threshold)

        start_point: Tuple[int, int]
        for start_point in zip(*locations[::-1]):
            end_point = (start_point[0] + width, start_point[1] + height)
            primitives.append(Primitive(start_point, end_point))

        return primitives

    def __validate_primitives(self, candidate_primitives: List[Primitive]) -> List[Primitive]:
        if len(candidate_primitives) <= 0:
            return []

        valid_primitives: List[Primitive] = [candidate_primitives[0]]
        for prim in candidate_primitives[1:]:
            if prim.is_overlapping_any(valid_primitives):
                continue
            else:
                valid_primitives.append(prim)

        return valid_primitives
