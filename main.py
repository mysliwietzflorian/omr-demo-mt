from absl import app, flags, logging

from src.omr_tool import OmrTool

flags.DEFINE_boolean("image_outputs", False, "Write debug image outputs")
flags.DEFINE_boolean("image_resize", True, "Resize the image while reading")
flags.DEFINE_string("output_directory", "output", "Directory for image outputs")


def main(args):
    if len(args) <= 1:
        logging.error("Missing required positional argument (filename)")
        exit()
    else:
        inputfile: str = args[1]

        OmrTool(inputfile, flags.FLAGS).run()


if __name__ == "__main__":
    app.run(main)
