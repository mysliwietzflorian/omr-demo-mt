from absl import logging

from src.model.notation_graph import NotationGraph


class Encoder(object):
    def __init__(self, flags):
        self.__flags = flags

    def run(self, notation_graph: NotationGraph):
        logging.debug("Encode notation graph")

        self.__json_encode(notation_graph)

    def __json_encode(self, notation_graph: NotationGraph):
        json_filename = "{}/{}.json".format(self.__flags.output_directory, "notation_graph")
        json_output_file = open(json_filename, "w")
        json_output_file.write(notation_graph.to_json())
        json_output_file.close()
