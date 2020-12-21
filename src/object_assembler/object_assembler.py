from absl import logging

from src.model.notation_graph import NotationGraph


class ObjectAssembler(object):
    def __init__(self, flags):
        self.__flags = flags

    def run(self, objects, notation_graph: NotationGraph) -> NotationGraph:
        logging.debug("Assemble music objects")

        for group in objects:
            self.handle_symbols(group, objects[group])

        return notation_graph

    def handle_symbols(self, group: str, objects):
        for obj in objects:
            if len(objects[obj]) > 0:

                if (obj == "note"):
                    self.handle_note(objects[obj])

    def handle_note(self, notes):
        # note in notes:
        pass
