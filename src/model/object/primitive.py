from __future__ import annotations

from typing import Tuple, List
import cv2


class Primitive(object):
    def __init__(self, start_point: Tuple[int, int], end_point: Tuple[int, int]):
        self.x1 = start_point[0]
        self.y1 = start_point[1]
        self.x2 = end_point[0]
        self.y2 = end_point[1]

    def get_width(self):
        return self.x2 - self.x1

    def get_height(self):
        return self.y2 - self.y1

    def get_center(self):
        return self.x1 + self.get_width() / 2, self.y1 + self.get_height() / 2

    def is_overlapping(self, other: Primitive) -> bool:
        return not (self.x1 >= other.x2 or self.x2 <= other.x1 or
                    self.y1 >= other.y2 or self.y2 <= other.y1)

    def is_overlapping_any(self, list: List[Primitive]) -> bool:
        for prim in list:
            if self.is_overlapping(prim):
                return True

        return False

    def draw(self, image, color: Tuple[int, int, int], thickness=1, label=""):
        if label:
            offset = 16
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_TRIPLEX, 1, 2)
            cv2.rectangle(image,
                          (self.x1 - 1, self.y1 - label_size[1] - 2 * offset),
                          (self.x1 + label_size[0] + 2 * offset + 1, self.y1), color, cv2.FILLED)

            cv2.putText(image, label, (self.x1 + offset, self.y1 - offset),
                        cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)

        cv2.rectangle(image,
                      (self.x1, self.y1), (self.x2, self.y2), color, thickness)
