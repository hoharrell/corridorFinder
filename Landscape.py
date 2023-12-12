from shapely.geometry import Polygon, LineString, MultiPoint
from shapely.ops import split, unary_union, linemerge, polygonize
import matplotlib.pyplot as plt
import numpy as np
import triangle as tr
import itertools
from shapely.plotting import plot_polygon, plot_points


class Landscape:
    def __init__(self, polygons):
        self.polygons = polygons


epsilon = 0.001


# p1 = Polygon([(1, 1), (-1, 2), (-2, -1), (0, 1)])
# p2 = Polygon([(-1, 1), (-2, 2), (-2, -2)])
# print(p1.intersects(p2))
# p3 = Polygon(
#     shell=[(0, 0), (0, 30), (30, 30), (30, 0), (0, 0)],
#     holes=[[(10, 10), (20, 10), (20, 20), (10, 20), (10, 10)]],
# )
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


# boundary = findBoundary(polygon)
# print(boundary)
polygons = []
polygons.append(Polygon([(2.5, 3.5), (5.5, 4.5), (6, 6),
                         (10, 6), (11, 4), (9.5, 4.5), (6, 2)]))
polygons.append(
    Polygon([(0, 1), (1, 5), (4, 4), (1.5, 3.5), (3.5, 2.5), (3, 1.5)]))
polygons.append(Polygon([(4, 4), (1.5, 3.5), (3.5, 2.5), (3, 1.5), (11, 0),
                        (11.5, 1.5), (11, 2), (12, 2.5), (11.5, 3.5), (11, 4),
                         (9.5, 4.5), (6, 2), (2.5, 3.5)]))
polygons.append(Polygon([(11, 0), (11.5, 1.5), (12.5, 2), (12, 2.5),
                         (11.5, 3.5), (11, 4), (11.5, 4.5), (14, 4),
                         (13.5, 1)]))
# for polygon in polygons:
#     x, y = polygon.exterior.xy
#     plt.plot(x, y)
# plt.show()


# Finds all valid gates for a pair
# (p1, p2) of polygons in the landscape


def findGates(p1, p2):

    # assumes edges of p1 are ordered sequentially

    if p1.intersection(p2).boundary.is_empty:
        return []
    sharedEdges = list(p1.intersection(p2).geoms)
    edgeList = []
    while sharedEdges:
        contiguousEdges = []
        edge = sharedEdges[0]
        contiguousEdges.append(edge)
        sharedEdges.pop(0)
        if (edge.touches(sharedEdges[0])):
            while (sharedEdges and
                   sharedEdges[0].touches(contiguousEdges[-1])):
                contiguousEdges.append(sharedEdges[0])
                sharedEdges.pop(0)
        elif (edge.touches(sharedEdges[-1])):
            while (sharedEdges and
                   sharedEdges[-1].touches(contiguousEdges[-1])):
                contiguousEdges.append(sharedEdges[-1])
                sharedEdges.pop()
        edgeList.append(contiguousEdges)
    pseudoEdges = []
    for edgeSet in edgeList:
        pseudoEdges.append(connectEdges(edgeSet))
    gates = []
    for edge in pseudoEdges:
        union = p1.union(p2)
        if union.contains(edge):
            gates.append(edge)
        elif union.crosses(edge):
            partition = list(split(edge, union).geoms)
            for edge in partition:
                gates.append(edge)
            for i in range(len(partition)):
                gateUnion = partition[i]
                for j in range(i + 1, len(partition)):
                    gateUnion = LineString(gateUnion.union(
                        partition[j]).boundary.geoms)
                    gates.append(gateUnion)
    return gates


def connectEdges(edgeSet):
    if len(edgeSet) == 1:
        return edgeSet[0]
    point1 = edgeSet[0].boundary.difference(edgeSet[1])
    point2 = edgeSet[-1].boundary.difference(edgeSet[-2])
    connection = LineString([point1, point2])
    return connection

# might have to do this as you go and store only gates / gate pairs
# that have already been computed


def computeGates(triplet, union, totalPolygons, gates):
    A = triplet[0]
    B = triplet[1]
    C = triplet[2]
    if (A > B):
        temp = A
        A = B
        B = temp
    gates_1_2 = gates[(int)((-1/2) * (A ** 2) + ((totalPolygons * 2 + 1)
                                                 * A)/2 - totalPolygons + (B - A - 1))]
    if (A != triplet[0]):
        temp = A
        A = B
        B = temp
    if (B > C):
        temp = B
        B = C
        C = temp
    gates_2_3 = gates[(int)((-1/2) * (B ** 2) + ((totalPolygons * 2 + 1)
                                                 * B)/2 - totalPolygons + (C - B - 1))]
    return findAllGatePairs(union, gates_1_2, gates_2_3)


def findAllGatePairs(union, gates_1_2, gates_2_3):
    gatePairs = []
    for gateA in gates_1_2:
        if union.contains(gateA):
            for gateB in gates_2_3:
                if union.contains(gateB):
                    pair = []
                    pair.append(gateA)
                    pair.append(gateB)
                    gatePairs.append(pair)
    return gatePairs


def findAllGates(polygons):
    gates = []
    for i in range(len(polygons)):
        for j in range(i + 1, len(polygons)):
            gates.append(findGates(polygons[i], polygons[j]))
    return gates


def findGatePairs(polygons, triplet, gates):
    union = polygons[triplet[0] - 1].union(
        polygons[triplet[1] - 1]).union(polygons[triplet[2]-1])
    gatePairs = (computeGates(triplet, union, len(polygons), gates))
    return gatePairs


def findCorePolygon(polygons, triplet, gatePairs):
    union = polygons[triplet[0] - 1].union(
        polygons[triplet[1] - 1]).union(polygons[triplet[2] - 1])
    lineSplitCollection = union.boundary
    gateCollection = gatePairs[0][0]
    for gatePair in gatePairs:
        for gate in gatePair:
            lineSplitCollection = lineSplitCollection.union(gate)
            gateCollection = gateCollection.union(gate)

    mergedLines = linemerge(lineSplitCollection)
    borderLines = unary_union(mergedLines)
    decomposition = list(polygonize(borderLines))
    for polygon in list(decomposition):
        if polygon.buffer(epsilon).covers(gateCollection):
            corePolygon = polygon
    return corePolygon


# A = dict(vertices=np.array(((0, 0), (1, 0), (1, 1), (0, 1))))
# # A['segments'] = [[0, 1],]
# B = tr.triangulate(A)
# tr.compare(plt, A, B)
# plt.show()

triplet = [2, 3, 4]
allGates = findAllGates(polygons)
gatePairs = findGatePairs(polygons, triplet, allGates)
corePolygon = findCorePolygon(polygons, triplet, gatePairs)

ext = [(0, 4.5), (1.5, 7), (0, 8), (2, 9.5), (4.5, 8.5), (7.5, 8.5), (9.5, 9.5),
       (10, 8), (9, 7), (7.5, 4.5), (10, 2.5), (9, 0), (5, 0), (5.5, 1.5), (3.5, 1.5)]
int_1 = [(3.5, 3.5), (4, 5.5), (6.5, 6.5), (7.5, 5.5),
         (6, 5), (6, 3), (5.5, 3.5)][::-1]
int_2 = [(2, 5), (5, 7), (4, 8), (3, 8)]
polygonWithHole = Polygon(ext, [int_1, int_2])

# checkA = polygonWithHole.exterior
# checkB = polygonWithHole.boundary
# checkC = polygonWithHole.interiors
# checkD = list(checkC)


def triangulate(corePolygon, show):
    coreVertices = []
    for coordinate in list(corePolygon.exterior.coords):
        coreVertices.append(coordinate)
    coreSegments = [(i, i+1) for i in range(len(coreVertices)-1)]
    for hole in list(corePolygon.interiors):
        for coordinate in list(hole.coords):
            coreSegments.append((len(coreVertices), len(coreVertices) + 1))
            coreVertices.append(coordinate)
        coreSegments.pop()
    # will need to do a MultiLineString with the boundary and interior - might be different if it has holes - check
    # will need to do something different for coreSegments in the case when the polygon has holes
    # check = list(split(corePolygon.boundary, MultiPoint(coreVertices)).geoms)
    # for line in check:
    #     coreSegments.append(list(line.coords))
    # coreSegments.append([i, i+1] for i in range(len(corePolygon.interiors)))

    polygon = {
        "vertices": coreVertices,
        "segments": coreSegments
    }
    triangulation = tr.triangulate(polygon, 'p')
    if (show):
        tr.compare(plt, polygon, triangulation)
        plt.show()
    return triangulation
    # return tr.triangulate(polygon, 'p')
    # tr.compare(plt, C, B)
    # plt.show()


triangulation = triangulate(corePolygon, False)
vertices = triangulation['vertices']
for vertex in vertices:
    print(vertex)
triangles = triangulation['triangles']
triangulation2 = triangulate(polygonWithHole, True)

# triplets = list(itertools.combinations(polygons, 3))
