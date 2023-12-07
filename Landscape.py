import math
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


class Landscape:
    def __init__(self, polygons):
        self.polygons = polygons


# class Polygon:
#     def __init__(self, edges, cost):
#         self.edges = edges
#         self.cost = cost
#     # def union(self, others):

#     def intersect(self, other):
#         x = 5


class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.length = math.sqrt((v1 + v2)**2)


class Corridor:
    def __init__(self, polygons):
        self.polygons = polygons
        self.width = 0
        self.length = 0
        self.totalCost = 0
        for polygon in polygons:
            self.totalCost += polygon.cost


class Agent:
    def __init__(self, diameter):
        self.diameter = diameter


p1 = Polygon([(1, 1), (-1, 2), (-2, -1), (0, 1)])
p2 = Polygon([(-1, 1), (-2, 2), (-2, -2)])
print(p1.intersects(p2))
p3 = Polygon(
    shell=[(0, 0), (0, 30), (30, 30), (30, 0), (0, 0)],
    holes=[[(10, 10), (20, 10), (20, 20), (10, 20), (10, 10)]],
)
# print(p3.exterior)
# for hole in p3.interiors:
#     for coordinate in hole.coords:
#         print(coordinate)
# x, y = p3.exterior.xy
# plt.plot(x, y)
# plt.show()
ext = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
int_1 = [(0.5, 0.25), (1.5, 0.25), (1.5, 1.25), (0.5, 1.25), (0.5, 0.25)]
int_2 = [(0.5, 1.25), (1, 1.25), (1, 1.75), (0.5, 1.75)]
polygon = Polygon(ext, [int_1, int_2])
# for hole in polygon.interiors:
#     for coordinate in hole.coords:
#         print(coordinate)
#     print()


def findBoundary(polygon):
    boundary = []
    boundary.append(polygon.exterior)
    for hole in polygon.interiors:
        boundary.append(hole)
    return boundary


boundary = findBoundary(polygon)
print(boundary)
p1 = Polygon([(2.5, 3.5), (5.5, 4.5), (6, 6),
             (10, 6), (11, 4), (9.5, 4.5), (6, 2)])
p2 = Polygon([(0, 1), (1, 5), (4, 4), (1.5, 3.5), (3.5, 2.5), (3, 1.5)])
p3 = Polygon([(4, 4), (1.5, 3.5), (3.5, 2.5), (3, 1.5), (11, 0), (11.5, 1.5),
             (11, 2), (12, 2.5), (11.5, 3.5), (11, 4),
             (9.5, 4.5), (6, 2), (2.5, 3.5)])
p4 = Polygon([(11, 0), (11.5, 1.5), (12.5, 2), (12, 2.5),
             (11.5, 3.5), (11, 4), (11.5, 4.5), (14, 4), (13.5, 1)])
x, y = p1.exterior.xy
plt.plot(x, y)
x, y = p2.exterior.xy
plt.plot(x, y)
x, y = p3.exterior.xy
plt.plot(x, y)
x, y = p4.exterior.xy
plt.plot(x, y)
plt.show()
# Finds a valid gate pair for a pair
# (p1, p2) of polygons in the landscape


def findGates(p1, p2):
    # Step 1: Let # E_c be a set of continuous edges
    # between p1 and p2
    intersect = p1.intersection(p2)
    if intersect.boundary.is_empty:
        return
    edges = list(intersect.geoms)
    print(edges)
    print()


findGates(p1, p2)
findGates(p1, p3)
findGates(p1, p4)
findGates(p2, p3)
findGates(p2, p4)
findGates(p3, p4)
