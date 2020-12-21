import json
import sys

out_data = []


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PrimitiveComponent):
            return obj.__dict__
        return super(CustomEncoder, self).default(obj)


class PrimitiveComponent(object):
    def __init__(self, points):
        self.x1: int = round(points[0][0])
        self.y1: int = round(points[0][1])
        self.x2: int = round(points[1][0])
        self.y2: int = round(points[1][1])


def create_object(shape):
    return {
        "label": shape['label'],
        "primitive-component": PrimitiveComponent(shape["points"])
    }


if (len(sys.argv) - 1) < 1:
    print("Error: Input json file expected")
    exit()

with open(sys.argv[1]) as json_file:
    with open("output.json", 'w') as output_file:
        data = json.load(json_file)

        print("{} shape(s) found".format(len(data["shapes"])))

        for shape in data["shapes"]:
            new = create_object(shape)
            out_data.append(new)

        json.dump(out_data, output_file, cls=CustomEncoder, indent=4)
        print("Json file created (output.json)")
