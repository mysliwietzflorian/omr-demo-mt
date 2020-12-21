from src.helper.path_finding_helper import AStar


class StablePathFinder(AStar):
    def __init__(self, image, graph_weights):
        self.__height, _ = image.shape

        self.__graph_weights = graph_weights

    def is_goal_reached(self, current, goal):
        return current[0] >= goal

    def heuristic_cost_estimate(self, current, goal):
        return goal - current[0]

    def distance_between(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        y_offset = y2 - y1
        return self.__graph_weights[y1][x1][y_offset + 1]

    def neighbors(self, node):
        neighbors = []
        x, y = node

        if node[1] > 0:
            neighbors.append((x + 1, y - 1))

        if node[1] < self.__height - 1:
            neighbors.append((x + 1, y + 1))

        neighbors.append((x + 1, y))

        return neighbors
