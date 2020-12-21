import math

import cv2
from absl import logging

from src.helper.image_helper import ImageHelper


class Preprocessor(object):
    def __init__(self, flags):
        self.__flags = flags
        self.filter_strength = 15
        self.canny_lower_threshold = 50

    def run(self, image):
        if image is None:
            logging.warning("Image for preprocessor is not defined")
            return

        image = self.__remove_noise(image, "02_noise_removal")
        image = self.__align_image(image, "03_aligning")
        image = self.__binarize_image(image, "04_binarization")
        return image

    def __remove_noise(self, image, title: str):
        logging.debug("Remove noise for image")
        cv2.fastNlMeansDenoising(image, image, self.filter_strength)
        return ImageHelper.write_image(image, title, self.__flags)

    def __align_image(self, image, title: str):
        logging.debug("Align image")
        angle = self.__compute_angle(image.copy())
        logging.debug("Rotating image by {} degrees".format(angle))

        if not math.isclose(angle, 0.0):
            image = self.__deskew(image.copy(), angle)
        return ImageHelper.write_image(image, title, self.__flags)

    def __compute_angle(self, image) -> float:
        height, width = image.shape

        edges = cv2.Canny(image, self.canny_lower_threshold, self.canny_lower_threshold * 3)
        lines = cv2.HoughLinesP(edges, 1, math.pi / 180, 200, minLineLength=width / 8, maxLineGap=width / 128)

        angle = 0.0
        if lines.any():
            for points in lines:
                x1, y1, x2, y2 = points[0]
                angle += math.atan2(y2 - y1, x2 - x1)
        return angle * 180 / math.pi

    def __deskew(self, image, angle: float):
        non_zero_pixels = cv2.findNonZero(image)
        center, wh, theta = cv2.minAreaRect(non_zero_pixels)

        root_mat = cv2.getRotationMatrix2D(center, angle, 1)
        rows, cols = image.shape
        rotated = cv2.warpAffine(image, root_mat, (cols, rows), cv2.INTER_CUBIC, borderValue=(255, 255, 255))
        return cv2.getRectSubPix(rotated, (cols, rows), center)

    def __binarize_image(self, image, title: str):
        logging.debug("Binarize image")
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return ImageHelper.write_image(image, title, self.__flags)
