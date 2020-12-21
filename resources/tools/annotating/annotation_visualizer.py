import json
from typing import List, Tuple

import cv2

version = "0.1.0"
license_disclaimer = """

OMR Annotation Visualizer (OMR-AV) version {}
Copyright 2020 Florian Mysliwietz.

There is NO warranty.  Redistribution of this software is
covered by the Lesser GNU General Public License.

"""


def get_all_graph_paths() -> List[str]:
    paths = []
    for i in range(1, 7):
        paths.append("byrd_{:02d}_graph.json".format(i))
    return paths


def load_graph_data(path: str):
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def load_image(filename):
    return cv2.imread(filename, cv2.IMREAD_COLOR)


def write_image(image, title: str):
    image_path = "visualizations/{}.png".format(title)
    print("Writing image {}".format(image_path))
    cv2.imwrite(image_path, image)


def draw_rect(image, rect, color: Tuple[int, int, int], width, label=""):
    offset = int(width / 100)
    thickness = int(width / 500)
    font_scale = width / 1000

    cv2.rectangle(image, (rect["x1"], rect["y1"]), (rect["x2"], rect["y2"]), color, thickness)

    if label is not None and label != "":
        cv2.putText(image, label, (rect["x1"], rect["y1"] - offset),
                    cv2.FONT_HERSHEY_TRIPLEX, font_scale, color, thickness)


def get_music_object_label(obj) -> str:
    label = ""

    if obj["type-component"]["type"] == "note":
        pitch = obj["type-component"]["pitch"]
        if pitch is not None:
            label = pitch["step"]
            if "alteration" in pitch:
                if pitch["alteration"] < 0:
                    label += "b" * abs(pitch["alteration"])
                elif pitch["alteration"] > 0:
                    label += "#" * abs(pitch["alteration"])
            label += str(pitch["octave"])

    elif obj["type-component"]["type"] == "rest":
        pass

    return label


def annotate_image(image, annotation):
    high_level_objects = image.copy()

    width = annotation["imageWidth"]
    graph = annotation["notation-graph"]

    bounding_box = graph["primitive-component"]
    draw_rect(high_level_objects, bounding_box, (200, 50, 50), width, "bounding")
    for measure in graph["measures"]:
        rect = measure["primitive-component"]
        draw_rect(high_level_objects, rect, (50, 50, 180), width, str(measure["number"]))

    image_path = annotation["imagePath"].split(".")[0]
    write_image(high_level_objects, "{}-{}".format(image_path, "high_level"))

    low_level_objects = image.copy()
    for measure in graph["measures"]:
        for obj in measure["objects"]:
            rect = obj["primitive-component"]
            label = get_music_object_label(obj);
            draw_rect(low_level_objects, rect, (180, 50, 50), width, label)

    image_path = annotation["imagePath"].split(".")[0]
    write_image(low_level_objects, "{}-{}".format(image_path, "low_level"))


def main():
    print(license_disclaimer.format(version))

    paths = get_all_graph_paths()
    for path in paths:
        annotation = load_graph_data(path)
        filename = annotation["imagePath"]
        image = load_image("../{}".format(filename))

        if image is None:
            print("Warning: image {} not found".format(filename))
            continue

        annotate_image(image, annotation)


if __name__ == "__main__":
    main()
