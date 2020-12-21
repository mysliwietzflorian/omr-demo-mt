from src.encoder.encoder import Encoder
from src.image_loader.image_loader import ImageLoader
from src.object_assembler.object_assembler import ObjectAssembler
from src.object_detector.object_detector import ObjectDetector
from src.preprocessor.preprocessor import Preprocessor


class OmrTool(object):
    def __init__(self, filename: str, flags):
        self.__image = None

        self.image_loader = ImageLoader(filename, flags)
        self.preprocessor = Preprocessor(flags)
        self.object_detector = ObjectDetector(flags)
        self.object_assembler = ObjectAssembler(flags)
        self.encoder = Encoder(flags)

    def run(self):
        self.load_image()
        self.preprocess_image()
        objects = self.detect_objects()
        notation_graph = self.assemble(objects)
        self.encode(notation_graph)

    def load_image(self):
        self.__image = self.image_loader.load_image()

    def preprocess_image(self):
        self.__image = self.preprocessor.run(self.__image)

    def detect_objects(self):
        return self.object_detector.run(self.__image)

    def assemble(self, objects):
        return self.object_assembler.run(objects, self.object_detector.notation_graph)

    def encode(self, notation_graph):
        self.encoder.run(notation_graph)
