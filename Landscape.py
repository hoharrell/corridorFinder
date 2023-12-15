from shapely.geometry import Polygon, LineString, Point, MultiLineString
from shapely.ops import split, unary_union, linemerge, polygonize
import matplotlib.pyplot as plt
import numpy as np
import math
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
examplePolygons = []
examplePolygons.append(
    Polygon([(4, 0), (0, 3), (0, 15), (2, 16), (7, 16), (9, 8), (5, 5)]))
examplePolygons.append(Polygon([(13, 1), (9, 8), (7, 16), (9, 19), (14, 21), (
    17, 17), (18, 15), (15, 16), (15, 15), (17, 13), (14, 9), (19, 2)]))
examplePolygons.append(Polygon([(18, 15), (17, 17), (26, 20), (29.5, 19), (29, 16), (31, 12), (32, 10), (29, 6), (
    25, 0), (19, 2), (14, 9), (17, 13), (19, 11), (22, 14)], [[(22, 10), (23, 6), (28, 9), (26, 12), (24, 10)]]))
examplePolygons.append(Polygon(
    [(32, 10), (29, 16), (29.5, 19), (30, 21), (34, 20), (34, 18), (33, 17), (36, 15)]))
# for polygon in examplePolygons:
#     plot_polygon(polygon)
# plt.show()

# IMPORTING THE GIS DATA AS POLYGONS IN EL DORADO DATA SET
# sf = shp.Reader("/Users/r_busch/Documents/GitHub/corridorFinder/El Dorado.zip") #TODO redefine path

# shapes = sf.shapes()

# for shape in shapes:
#     polygons.append(shape)
# TODO COMMENT BACK IN WHEN READY

# Finds all valid gates for a pair
# (p1, p2) of polygons in the landscape


def findGates(p1, p2):

    # assumes edges of p1 are ordered sequentially

    if p1.intersection(p2).boundary.is_empty:
        return []
    intersection = p1.intersection(p2)
    if (isinstance(intersection, MultiLineString)):
        sharedEdges = list(intersection.geoms)
    else:
        return [intersection]
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


def midpoint(v1, v2):
    return [(v1[0]+v2[0]) / 2, (v1[1] + v2[1]) / 2]


def computeAngle(a, b, c):
    angle = math.degrees(math.acos(
        (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)))
    return angle


def triangleOpposite(triangles, edge, oppositeTriangle):
    for vertex in oppositeTriangle:
        if vertex not in edge:
            C = vertex
    for triangle in triangles:
        if (edge[0] in triangle) and (edge[1] in triangle) and C not in triangle:
            return triangle
    return []


def searchWidth(vertices, triangles, segments, triangle, C, edge, upperBound):
    U = edge[0]
    V = edge[1]
    u, v, c = [V, C], [U, C], edge
    length_u = math.dist(vertices[u[0]], vertices[u[1]])
    length_v = math.dist(vertices[v[0]], vertices[v[1]])
    length_c = math.dist(vertices[c[0]], vertices[c[1]])
    U_angle = computeAngle(length_c, length_u, length_v)
    V_angle = computeAngle(length_c, length_v, length_u)
    if (U_angle + epsilon >= 90) or (V_angle + epsilon >= 90):
        return upperBound
    d = Point(vertices[C]).distance(LineString([vertices[U], vertices[V]]))
    if d > upperBound:
        return upperBound
    # checks if edge is in segments
    if np.any(np.sum(np.abs(segments-c), axis=1) == 0) or np.any(np.sum(np.abs(segments-c[::-1]), axis=1) == 0):
        return d
    # can maybe compute this beforehand and store it
    newTriangle = triangleOpposite(triangles, edge, triangle)
    if len(newTriangle) > 0:
        for vertex in newTriangle:
            if vertex not in triangle:
                newVertex = vertex
                break
        e1 = [U, newVertex]
        e2 = [V, newVertex]
        upperBound = searchWidth(
            vertices, triangles, segments, newTriangle, C, e1, upperBound)
        return searchWidth(vertices, triangles, segments, newTriangle, C, e2, upperBound)
    return d


def findWidth(vertices, triangles, segments, triangle, e1, e2, e3):
    for vertex in triangle:
        if vertex not in e3:
            C = vertex
            break
    a, b, c = e1, e2, e3
    # could change to be more efficient if necessary
    length_a = math.dist(vertices[a[0]], vertices[a[1]])
    length_b = math.dist(vertices[b[0]], vertices[b[1]])
    length_c = math.dist(vertices[c[0]], vertices[c[1]])
    A_angle = computeAngle(length_c, length_a, length_b)
    B_angle = computeAngle(length_c, length_b, length_a)
    d = min(length_a, length_b)
    if (A_angle + epsilon >= 90) or (B_angle + epsilon >= 90):
        return d
    # if c is a constrained edge

    # checks if c is in segments
    if np.any(np.sum(np.abs(segments-c), axis=1) == 0) or np.any(np.sum(np.abs(segments-c[::-1]), axis=1) == 0):
        return Point(vertices[C]).distance(LineString([vertices[c[0]], vertices[c[1]]]))
    return searchWidth(vertices, triangles, segments, triangle, C, c, d)


def findTriangleEdgePairs(triangulation):
    vertices = triangulation['vertices']
    triangles = triangulation['triangles']
    segments = triangulation['segments']
    triangleEdgePairs = []
    for triangle in triangles:
        v1 = vertices[triangle[0]]
        v2 = vertices[triangle[1]]
        v3 = vertices[triangle[2]]
        v_1_2 = midpoint(v1, v2)
        v_2_3 = midpoint(v2, v3)
        v_1_3 = midpoint(v1, v3)
        e1 = [triangle[0], triangle[1]]
        e2 = [triangle[1], triangle[2]]
        e3 = [triangle[0], triangle[2]]
        edgePairs = []
        # edge 1, edge 2, width, length
        edgePairs.append([e1, e2, findWidth(vertices, triangles,
                                            segments, triangle, e1, e2, e3), math.dist(v_1_2, v_2_3)])
        edgePairs.append([e2, e3, findWidth(vertices, triangles,
                                            segments, triangle, e2, e3, e1), math.dist(v_2_3, v_1_3)])
        edgePairs.append([e1, e3, findWidth(vertices, triangles,
                                            segments, triangle, e1, e3, e2), math.dist(v_1_2, v_1_3)])
        # maybe should group by triangle instead
        for pair in edgePairs:
            triangleEdgePairs.append(pair)
    return triangleEdgePairs


def removeHoleTriangles(corePolygon, triangulation):
    vertices = triangulation['vertices']
    keptTriangles = []
    for triangle in triangulation['triangles']:
        polygon = Polygon([vertices[vertex]
                          for vertex in triangle])
        if corePolygon.buffer(epsilon).covers(polygon):
            keptTriangles.append(triangle)
    triangulation['triangles'] = np.array(keptTriangles)
    return triangulation


triplet = [2, 3, 4]
allGates = findAllGates(examplePolygons)
gatePairs = findGatePairs(examplePolygons, triplet, allGates)
corePolygon = findCorePolygon(examplePolygons, triplet, gatePairs)
triangulation = removeHoleTriangles(
    corePolygon, triangulate(corePolygon, True))
triangleEdgePairs = findTriangleEdgePairs(triangulation)

triplet = [2, 3, 4]
allGates = findAllGates(polygons)
gatePairs = findGatePairs(polygons, triplet, allGates)
corePolygon = findCorePolygon(polygons, triplet, gatePairs)
triangulation = removeHoleTriangles(
    corePolygon, triangulate(corePolygon, False))
triangleEdgePairs = findTriangleEdgePairs(triangulation)

ext = [(0, 4.5), (1.5, 7), (0, 8), (2, 9.5), (4.5, 8.5), (7.5, 8.5), (9.5, 9.5),
       (10, 8), (9, 7), (7.5, 4.5), (10, 2.5), (9, 0), (5, 0), (5.5, 1.5), (3.5, 1.5)]
int_1 = [(3.5, 3.5), (4, 5.5), (6.5, 6.5), (7.5, 5.5),
         (6, 5), (6, 3), (5.5, 3.5)][::-1]
int_2 = [(2, 5), (5, 7), (4, 8), (3, 8)]
polygonWithHole = Polygon(ext, [int_1, int_2])


triangulation2 = triangulate(polygonWithHole, False)
triangulation2 = removeHoleTriangles(polygonWithHole, triangulation2)

triangleEdgePairs2 = findTriangleEdgePairs(triangulation2)
# triplets = list(itertools.combinations(polygons, 3))
