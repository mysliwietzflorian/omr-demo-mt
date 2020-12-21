import cv2
from absl import logging

from src.helper.image_helper import ImageHelper


class ImageLoader(object):
    def __init__(self, filename: str, flags):
        self.__filename = filename
        self.__flags = flags
        self.max_width = 1080
        if self.__filename.endswith(".pdf"):
            logging.warning("Use image files only. Transform PDF with pdf2img (using docker?)")

    def load_image(self):
        logging.debug("Load image {}".format(self.__filename))
        image = cv2.imread(self.__filename, cv2.IMREAD_GRAYSCALE)

        ImageHelper.write_image(image, "00_base", self.__flags)

        if self.__flags.image_resize:
            image = self.__resize_image(image)
            logging.debug("Resized image to ({} x {})".format(image.shape[1], image.shape[0]))
            ImageHelper.write_image(image, "01_resize", self.__flags)
        return image

    def __resize_image(self, image):
        height, width = image.shape

        if self.max_width < width:
            new_size = (self.max_width, round((height / width) * self.max_width))
            return cv2.resize(image, new_size)
        else:
            return image
