from typing import List

import cv2
from absl import logging

from src.model.object.primitive import Primitive


class ImageHelper(object):
    @staticmethod
    def write_image(image, title: str, flags):
        if flags.image_outputs:
            image_path = "{}/{}.jpg".format(flags.output_directory, title)
            logging.debug("Writing image {}".format(image_path))
            cv2.imwrite(image_path, image)
        return image

    @staticmethod
    def draw_primitives(image, primitives: List[Primitive], title: str, number: int, flags):
        colored_image = ImageHelper.get_colored_image(image)
        for prim in primitives:
            prim.draw(colored_image, (255, 127, 127), 2, title)

        filename = "{}_{}".format("{:02d}".format(number), title.lower().replace(" ", "_"))
        ImageHelper.write_image(colored_image, filename, flags)

    @staticmethod
    def get_colored_image(image):
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
