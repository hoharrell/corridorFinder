class Landscape:
    x = 5

    def __init__(self, polygons):
        self.polygons = polygons


class Polygon:
    def __init__(self, edges):
        self.edges = edges


class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2


class Corridor:
    def __init__(self, polygons):
        self.polygons = polygons
        self.width = 0
        self.length = 0


class Agent:
    def __init__(self, diameter):
        self.diameter = diameter
