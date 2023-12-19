from shapely.geometry import mapping, Polygon, LineString, Point, MultiLineString
from shapely.ops import split, unary_union, linemerge, polygonize
import matplotlib.pyplot as plt
import numpy as np
import math
import triangle as tr
import itertools
import shapefile as shp
import fiona
from ortools.linear_solver import pywraplp
from shapely.plotting import plot_polygon, plot_points, plot_line
from tri.delaunay.helpers import ToPointsAndSegments
from tri.delaunay import triangulate
# from sect.triangulation import triangulation
import faulthandler

faulthandler.enable()

epsilon = 0.001
maxLength_triplet = 1000  # arbitrary value, change later
maxLength_overall = 40000  # arbitrary value, change later


def findBoundary(polygon):
    boundary = []
    boundary.append(polygon.exterior)
    for hole in polygon.interiors:
        boundary.append(hole)
    return boundary


def importData():
    # imports the data from the zipped shapefile and returns
    # a list of polygons contained in the shapefile, as shapely
    # Polygon objects.
    sf = shp.Reader("./El Dorado.zip")

    polygons = []
    shapes = sf.shapes()

    for i in range(len(shapes)):
        # for j in range(len(shapes[i].points)):
        polygon = Polygon(shapes[i].points)
        polygons.append(polygon)

    return polygons


def clusterMaker(polygons):
    # takes as input a collection of polygons, and combines them together
    # in as many was as are possible to create clusters of polygons
    # these clusters will overlap each other, but this is my understanding
    # of the process used in the paper. Also needs testing on the data.
    clusters = []
    for polygon_a in polygons:
        for polygon_b in polygons:
            if not polygon_b.equals(polygon_a):
                if polygon_a.touches(polygon_b) \
                        and (unary_union([polygon_a, polygon_b]).area <= 200000):
                    clusters.append(unary_union([polygon_a, polygon_b]))
                else:
                    clusters.append(polygon_a)
    for cluster in clusters:
        while (cluster.area <= 200000):
            for poly in polygons:
                if cluster.touches(poly):
                    if (unary_union([cluster, poly]).area <= 200000):
                        clusters.append(unary_union([cluster, poly]))

    return clusters


# def combinePolygons(polyA, polyB):
#     # combines two shapley polygons and returns a single polygon.
#     # has not been sufficiently tested yet
#     newList = ()
#     print(polyA.xy)
#     for i in range(len(polyB.xy)):
#         for j in range(len(polyB.xy)):
#             ()
#             if (polyB.xy):
#                 newList = newList + coordB
#                 newList = newList + coordA
#     combined = Polygon(newList)

#     return combined


def exportData(polygons):
    # takes in a collection of polygons and exports them to an ESRI
    # shapefile. Worked when tested on the El dorado data set that had
    # been converted into shapely polygons.
    schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int'},
    }

    with fiona.open('./testfile.shp',
                    'w', 'ESRI Shapefile', schema) as c:
        for poly in polygons:
            c.write({
                'geometry': mapping(poly),
                'properties': {'id': polygons.index(poly)}
            })


def importData():
    # imports the data from the zipped shapefile and returns a list of polygons.
    sf = shp.Reader("./El Dorado.zip")

    polygons = []
    shapes = sf.shapes()

    for i in range(len(shapes)):
        polygon = Polygon(shapes[i].points)
        polygons.append(polygon)

    return polygons


def findGates(p1, p2):

    # assumes edges of p1 are ordered sequentially
    intersection = p1.intersection(p2)
    if (not intersection.boundary or intersection.boundary.is_empty):
        return []
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
        if (sharedEdges and edge.touches(sharedEdges[0])):
            while (sharedEdges and
                   sharedEdges[0].touches(contiguousEdges[-1])):
                contiguousEdges.append(sharedEdges[0])
                sharedEdges.pop(0)
        elif (sharedEdges and edge.touches(sharedEdges[-1])):
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
            if isinstance(union, Polygon):
                partition = list(split(edge, union).geoms)
                for edge in partition:
                    gates.append(edge)
            # for i in range(len(partition)):
            #     gateUnion = partition[i]
            #     for j in range(i + 1, len(partition)):
            #         gateUnion = LineString(gateUnion.union(
            #             partition[j]).boundary.geoms)
            #         gates.append(gateUnion)
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
    ABKey = '{},{}'.format(A, B)
    if ABKey in gates:
        gates_1_2 = gates[ABKey]
    else:
        return []
    if (A != triplet[0]):
        temp = A
        A = B
        B = temp
    if (B > C):
        temp = B
        B = C
        C = temp
    BCKey = '{},{}'.format(B, C)
    if BCKey in gates:
        gates_2_3 = gates[BCKey]
    else:
        return []

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
    gatesDict = {}
    for i in range(len(polygons)):
        for j in range(i + 1, len(polygons)):
            gates = (findGates(polygons[i], polygons[j]))
            if gates:
                a, b = i, j
                if b < a:
                    a, b = b, a
                gateKey = '{},{}'.format(a, b)
                gatesDict[gateKey] = gates
    return gatesDict


def findGatePairs(polygons, triplet, gates):
    union = polygons[triplet[0]].union(
        polygons[triplet[1]]).union(polygons[triplet[2]])
    gatePairs = (computeGates(triplet, union, len(polygons), gates))
    return gatePairs


def findCorePolygon(polygons, triplet, gatePairs):
    union = polygons[triplet[0]].union(
        polygons[triplet[1]]).union(polygons[triplet[2]])
    # plot_polygon(union, add_points=False)
    # for gatePair in gatePairs:
    #     for gate in gatePair:
    #         plot_line(gate)
    # plt.show()
    lineSplitCollection = union.boundary
    gateCollection = gatePairs[0][0]
    for gatePair in gatePairs:
        for gate in gatePair:
            lineSplitCollection = lineSplitCollection.union(gate)
            gateCollection = gateCollection.union(gate)

    mergedLines = linemerge(lineSplitCollection)
    borderLines = unary_union(mergedLines)
    decomposition = list(polygonize(borderLines))
    # for polygon in list(decomposition):
    #     plot_polygon(polygon, add_points=False)
    # plt.show()
    corePolygon = False
    for polygon in list(decomposition):
        if (polygon.buffer(epsilon).covers(gateCollection) and
                polygon.boundary.buffer(epsilon).covers(gateCollection)):
            corePolygon = polygon
    # for gatePair in gatePairs:
    #     for gate in gatePair:
    #         plot_line(gate)
    # plt.show()
    # plot_polygon(corePolygon, add_points=False)
    # for gatePair in gatePairs:
    #     for gate in gatePair:
    #         plot_line(gate)
    # plt.show()
    return corePolygon


def findTriangulation(corePolygon, show):
    coreVertices = []
    for coordinate in list(corePolygon.exterior.coords):
        coreVertices.append(coordinate)
    holeVertices = []
    for hole in list(corePolygon.interiors):
        for coordinate in list(hole.coords):
            holeVertices.append(coordinate)
    pts_segs = ToPointsAndSegments()
    if holeVertices:
        pts_segs.add_polygon([coreVertices, holeVertices])
    else:
        pts_segs.add_polygon([coreVertices])
    triangulation = triangulate(
        pts_segs.points, pts_segs.infos, pts_segs.segments)
    triangles = []
    for triangle in triangulation.triangles:
        if triangle.is_finite:
            vertices = []
            for vertex in triangle.vertices:
                for i, point in enumerate(pts_segs.points):
                    if vertex.x == point[0] and vertex.y == point[1]:
                        vertices.append(i)
                        break
            triangles.append(vertices)
    triDict = {}
    triDict['triangles'] = triangles
    triDict['segments'] = pts_segs.segments
    triDict['vertices'] = pts_segs.points
    return triDict

    # # old library
    # coreVertices = []
    # for coordinate in list(corePolygon.exterior.coords):
    #     coreVertices.append(coordinate)
    # coreSegments = [(i, i+1) for i in range(len(coreVertices)-1)]
    # holeVertices = []
    # for hole in list(corePolygon.interiors):
    #     for coordinate in list(hole.coords):
    #         coreSegments.append((len(coreVertices), len(coreVertices) + 1))
    #         coreVertices.append(coordinate)
    #         holeVertices.append(coordinate)
    #     coreSegments.pop()
    # polygon = {
    #     "vertices": coreVertices,
    #     "segments": coreSegments
    # }
    # triangulation = tr.triangulate(polygon, 'p')
    # if (show):
    #     tr.compare(plt, polygon, triangulation)
    #     plt.show()
    # check1 = list(triangulation['triangles'])
    # check2 = list(triangulation['segments'])
    # check3 = list(triangulation['vertices'])
    # return triangulation


def midpoint(v1, v2):
    return [(v1[0]+v2[0]) / 2, (v1[1] + v2[1]) / 2]


def computeAngle(a, b, c):
    input = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
    if input < -1:
        input = -1
    if input > 1:
        input = 1
    angle = math.degrees(math.acos(input))
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
    # if np.any(np.sum(np.abs(segments-c), axis=1) == 0) or np.any(np.sum(np.abs(segments-c[::-1]), axis=1) == 0):
    if c in segments or c[::-1] in segments:
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
    # if np.any(np.sum(np.abs(segments-c), axis=1) == 0) or np.any(np.sum(np.abs(segments-c[::-1]), axis=1) == 0):
    if c in segments or c[::-1] in segments:
        return Point(vertices[C]).distance(LineString([vertices[c[0]], vertices[c[1]]]))
    return searchWidth(vertices, triangles, segments, triangle, C, c, d)


def orderEdge(edge):
    if edge[0] > edge[1]:
        return edge[::-1]
    return edge


def findTriangleEdgePairs(triangulation, startingGates, endingGates):
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
        e1 = orderEdge([triangle[0], triangle[1]])
        e2 = orderEdge([triangle[1], triangle[2]])
        e3 = orderEdge([triangle[0], triangle[2]])
        if e2 in startingGates:
            e1, e2 = e2, e1
        if e3 in startingGates or e1 in endingGates:
            e1, e3 = e3, e1
        if e2 in endingGates:
            e2, e3 = e3, e2
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


def findMaxWidth(triangleEdgePairs):
    maxWidth = 0
    for edgePair in triangleEdgePairs:
        if edgePair[2] > maxWidth:
            maxWidth = edgePair[2]
    return maxWidth


def updateEdgeDict(edgeDict, e1, e2, var):
    # 0 indicates a var is leaving an edge
    # 1 indicates a var is entering an edge

    e1Key = '{},{}'.format(e1[0], e1[1])
    e2Key = '{},{}'.format(e2[0], e2[1])
    if e1Key in edgeDict:
        edgeDict[e1Key].append([var, 0])
    else:
        edgeDict[e1Key] = [[var, 0]]
    if e2Key in edgeDict:
        edgeDict[e2Key].append([var, 1])
    else:
        edgeDict[e2Key] = [[var, 1]]


def constructOptimalRoute(triangleEdgePairs, maxWidth, maxLength, gatePair):

    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return

    infinity = solver.infinity()

    # declare variables below
    Z = solver.NumVar(0.0, infinity, "Z")
    M = maxWidth
    vars = []
    edgeDict = {}
    for i, pair in enumerate(triangleEdgePairs):
        vars.append([solver.IntVar(
            0.0, 1.0, 'Edge Pair ({}, {}) to ({}, {})'.format(pair[0][0], pair[0][1], pair[1][0], pair[1][1])), pair[3]])
        updateEdgeDict(edgeDict, pair[0], pair[1], vars[i][0])
    print("Number of variables =", solver.NumVariables())

    # define constraints of variables

    # minimum width constraint
    for i, var in enumerate(vars):
        solver.Add(Z - M <= (triangleEdgePairs[i][2] - M) * var[0])
    print("Number of constraints =", solver.NumConstraints())

    # max length constraint
    constraint_expr = \
        [var[1] * var[0] for var in vars]
    solver.Add(sum(constraint_expr) <= maxLength)

    # starting gate constraint
    startGateKey = '{},{}'.format(gatePair[0][0], gatePair[0][1])
    leavingStartVars = []
    for edge in edgeDict[startGateKey]:
        if edge[1] == 0:
            leavingStartVars.append(edge[0])
    constraint_expr = \
        [var for var in leavingStartVars]
    solver.Add(sum(constraint_expr) == 1)

    # ending gate constraint

    endGateKey = '{},{}'.format(gatePair[1][0], gatePair[1][1])
    enteringEndVars = []
    for edge in edgeDict[endGateKey]:
        if edge[1] == 1:
            enteringEndVars.append(edge[0])
    constraint_expr = \
        [var for var in enteringEndVars]
    solver.Add(sum(constraint_expr) == 1)

    # connectivity constraint
    for edge, connections in edgeDict.items():
        if edge != endGateKey and edge != startGateKey:
            leaving = []
            entering = []
            for var in connections:
                if var[1] == 0:
                    leaving.append(var[0])
                else:
                    entering.append(var[0])
            leaving_expr = \
                [var for var in leaving]
            entering_expr = \
                [var for var in entering]
            solver.Add(sum(entering_expr) - sum(leaving_expr) == 0)
    print("Number of constraints =", solver.NumConstraints())

    solver.Maximize(Z)
    print(solver.ExportModelAsLpFormat(False).replace(
        '\\', '').replace(',_', ','), sep='\n')

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", solver.Objective().Value())
        print("Z =", Z.solution_value())
        includedEdgePairs = []
        length = 0
        for var in vars:
            if var[0].solution_value() == 1:
                includedEdgePairs.append(var)
                length += var[1]
        return [solver.Objective().Value(), length]
    else:
        print("The problem does not have an optimal solution.")


def addKey(gateDict, gate1, gate2, routeVar):
    startKey = '{},{},{}'.format(gate1[0], gate1[1], gate1[2])
    if startKey in gateDict:
        gateDict[startKey].append([routeVar, 0])
    else:
        gateDict[startKey] = [[routeVar, 0]]
    endKey = '{},{},{}'.format(gate2[0], gate2[1], gate2[2])
    if endKey in gateDict:
        gateDict[endKey].append([routeVar, 1])
    else:
        gateDict[endKey] = [[routeVar, 1]]
    return gateDict


def doubleRoutes(optimalRoutes, startPolygon, endPolygon):
    newRoutes = []
    for route in optimalRoutes:
        if route[4][2] != startPolygon and route[4][0] != endPolygon:
            newRoutes.append(route)
        if route[4][0] != startPolygon and route[4][2] != endPolygon:
            newRoutes.append(
                [route[1], route[0], route[2], route[3], route[4][::-1]])
    return newRoutes


def solve(maxWidth, maxLength, optimalRoutes, startPolygon, endPolygon, parcels, polygons, costs, budget):
    # assuming route is [gate1[p1, p2, gate#], gate2[p1, p2, gate#], width, length, triplet]
    # assuming parcels is [parcel1[p1, p2, p3, ...], parcel2[p1, p2, p3, ...], ...]
    varDict = {}
    for polygon in polygons:
        varDict[polygon] = []
    gateDict = {}
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    infinity = solver.infinity()
    W = solver.NumVar(0.0, infinity, "W")
    D = maxWidth
    routeVars = []
    startingGates = []
    endingGates = []
    for i, route in enumerate(optimalRoutes):
        routeVars.append([solver.IntVar(
            0.0, 1.0, 'Gate {}-{}-{} to Gate {}-{}-{}'.format
            (route[0][0], route[0][1], route[0][2], route[1][0], route[1][1], route[1][2])),
            route[0], route[1], route[1][1], route[3], route[4]])
        varDict[route[4][0]].append([routeVars[i][0], 0])  # entry of triplet
        varDict[route[4][1]].append([routeVars[i][0], 1])  # middle of triplet
        varDict[route[4][2]].append([routeVars[i][0], 2])  # exit of triplet

        if route[4][0] == startPolygon:
            startingGates.append(routeVars[i][0])
        if route[4][2] == endPolygon:
            endingGates.append(routeVars[i][0])
        # removed gateDict = below
        addKey(gateDict, route[0], route[1], routeVars[i][0])
    # should be polygons + 1
    print("Number of variables =", solver.NumVariables())
    # minimum width constraint
    for i, routeVar in enumerate(routeVars):
        solver.Add(W - D <= (optimalRoutes[i][2] - D) * routeVar[0])
    print("Number of constraints =", solver.NumConstraints())
    # maximum length constraint
    constraint_expr = \
        [routeVar[4] * routeVar[0]
            for routeVar in routeVars]
    solver.Add(sum(constraint_expr) <= maxLength)
    print("Number of constraints =", solver.NumConstraints())
    # starting gates constraint
    constraint_expr = \
        [gate for gate in startingGates]
    solver.Add(sum(constraint_expr) == 1)
    print("Number of constraints =", solver.NumConstraints())
    # ending gates constraint
    constraint_expr = \
        [gate for gate in endingGates]
    solver.Add(sum(constraint_expr) == 1)
    print("Number of constraints =", solver.NumConstraints())

    # Connectivity constraints

    for gate, varList in gateDict.items():
        gatePolygons = gate.split(',')
        if '{}'.format(startPolygon) not in gatePolygons and '{}'.format(endPolygon) not in gatePolygons:
            starting = []
            ending = []
            for var in varList:
                if var[1] == 0:
                    starting.append(var)
                else:
                    ending.append(var)
            starting_expr = \
                [var[0] for var in starting]
            ending_expr = \
                [var[0] for var in ending]
            solver.Add(sum(starting_expr) - sum(ending_expr) == 0)
    print("Number of constraints =", solver.NumConstraints())

    # Parcel Constraints

    for parcel in parcels:
        starts = set()
        middle = set()
        ends = set()
        for polygon in parcel:
            for var in (varDict[polygon]):
                if var[1] == 0:
                    starts.add(var[0])
                elif var[1] == 1:
                    middle.add(var[0])
                else:
                    ends.add(var[0])
        starts_expr = \
            [var for var in starts]
        middle_expr = \
            [var for var in middle]
        ends_expr = \
            [var for var in ends]
        solver.Add(sum(starts_expr) <= 1)
        solver.Add(sum(middle_expr) <= 1)
        solver.Add(sum(ends_expr) <= 1)
    print("Number of constraints =", solver.NumConstraints())

    # Budget Constraints
    constraint_expr = \
        [costs[routeVar[5][1]] * routeVar[0] for routeVar in routeVars]
    solver.Add(sum(constraint_expr) <= budget)
    print("Number of constraints =", solver.NumConstraints())

    # Maximize W
    solver.Maximize(W)
    print(solver.ExportModelAsLpFormat(False).replace(
        '\\', '').replace(',_', ','), sep='\n')

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", solver.Objective().Value())
        print(f"Problem solved in {solver.wall_time():d} milliseconds")
        print(f"Problem solved in {solver.iterations():d} iterations")
        print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")
        includedTriplets = []
        length = 0
        for routeVar in routeVars:
            if routeVar[0].solution_value() == 1:
                includedTriplets.append(routeVar)
                length += routeVar[4]
        width = solver.Objective().Value()
        return [includedTriplets, width, length]

    else:
        print("The problem does not have an optimal solution.")
        return []


def convertGates(gatePairs, vertices, segments):
    check1 = list(vertices)
    allSegments = list(segments)
    for segment in segments:
        allSegments.append(list(segment)[::-1])
    newGatePair = []
    for gatePair in gatePairs:
        newPoints = []
        for gate in gatePair:
            coords = list(gate.coords)
            for segment in allSegments:
                # comparison1 = vertices[segment[0]] == coords[0]
                # comparison2 = vertices[segment[1]] == coords[1]
                if vertices[segment[0]] == coords[0] and vertices[segment[1]] == coords[1]:
                    newPoints.append(list(orderEdge(segment)))
                    break
        newGatePair.append(newPoints)
    return newGatePair


def doubleEdgePairs(triangleEdgePairs, gatePair):
    startGate = gatePair[0]
    endGate = gatePair[1]
    newEdgePairs = []
    for edgePair in triangleEdgePairs:
        if (not ((edgePair[0][0] == startGate[0] and edgePair[0][1] == startGate[1])
                 or (edgePair[1][0] == endGate[0] and edgePair[1][1] == endGate[1]))):
            newEdgePair = [edgePair[1], edgePair[0], edgePair[2], edgePair[3]]
            newEdgePairs.append(newEdgePair)
    return triangleEdgePairs + newEdgePairs


def groupGates(optimalRoutes):
    gateDict = {}
    newOptimalRoutes = []
    for optimalRoute in optimalRoutes:
        gate1Polygons = orderEdge(optimalRoute[0])
        gate2Polygons = orderEdge(optimalRoute[1])
        gate1Coords = optimalRoute[2]
        gate2Coords = optimalRoute[3]
        gate1Number = 0
        gate2Number = 0
        g1Key = '{},{}'.format(gate1Polygons[0], gate1Polygons[1])
        g2Key = '{},{}'.format(gate2Polygons[0], gate2Polygons[1])
        if g1Key not in gateDict:
            gateDict[g1Key] = [gate1Coords]
        else:
            for i, coords in enumerate(gateDict[g1Key]):
                if gate1Coords.equals(coords):
                    gate1Number = i
                    found = True
            if not found:
                gate1Number = len(gateDict[g1Key])
                gateDict[g1Key].append(gate1Coords)
        found = False
        if g2Key not in gateDict:
            gateDict[g2Key] = [gate2Coords]
        else:
            for i, coords in enumerate(gateDict[g2Key]):
                if gate2Coords.equals(coords):
                    gate2Number = i
                    found = True
            if not found:
                gate2Number = len(gateDict[g2Key])
                gateDict[g2Key].append(gate2Coords)
        gate1Polygons.append(gate1Number)
        gate2Polygons.append(gate2Number)
        newOptimalRoutes.append([gate1Polygons,
                                gate2Polygons,
                                optimalRoute[4],
                                optimalRoute[5],
                                [optimalRoute[0][0], optimalRoute[0][1], optimalRoute[1][1]]])
    return newOptimalRoutes


def removeInvalidPolygons(polygons):
    validPolygons = []
    for polygon in polygons:
        if polygon.is_valid:
            validPolygons.append(polygon)
    return validPolygons


def createTriplets(polygons):
    triplets = []
    for i, p1 in enumerate(polygons):
        touching = []
        for j, p2 in enumerate(polygons):
            if p1.touches(p2):
                touching.append(j)
        surrounding = list(itertools.combinations(touching, 2))
        for pair in surrounding:
            triplet = [pair[0], i, pair[1]]
            triplets.append(triplet)
    return triplets


def corridorConstructor():
    allLand = importData()
    # allLand = clusterMaker(allLand) TODO: implement cluster maker if possible
    allLand = removeInvalidPolygons(allLand)
    totalArea = 0
    costs = []
    for landItem in allLand:
        totalArea = landItem.area + totalArea
        costs.append(landItem.area)

    # according to the problem specifications, define the budget according to land area.
    budget = totalArea * 0.15

    allGates = findAllGates(allLand)
    allOptimalRoutes = []
    polygons = [i for i in range(len(allLand))]
    triplets = createTriplets(allLand)
    for triplet in triplets:
        print(triplet)
        # for polygon in triplet:
        #     plot_polygon(allLand[polygon], add_points=False)
        gatePairs = findGatePairs(allLand, triplet, allGates)
        if gatePairs:
            optimalRoutes = []
            corePolygon = findCorePolygon(allLand, triplet, gatePairs)
            if not corePolygon:
                continue
            triangulation = removeHoleTriangles(
                corePolygon, findTriangulation(corePolygon, False))
            triangulationGatePairs = convertGates(
                gatePairs, triangulation['vertices'], triangulation['segments'])
            startingGates = []
            endingGates = []
            for gatePair in triangulationGatePairs:
                if len(gatePair) < 2:
                    optimalRoutes.append([[triplet[0], triplet[1]],
                                          [triplet[1], triplet[2]],
                                          gatePairs[0][0], gatePairs[0][1],
                                          LineString(gatePairs[0][0]).length, 0.0],)
                    continue
                startingGates.append(gatePair[0])
                endingGates.append(gatePair[1])
            triangleEdgePairs = findTriangleEdgePairs(
                triangulation, startingGates, endingGates)
            maxWidth = findMaxWidth(triangleEdgePairs)
            for i, gatePair in enumerate(triangulationGatePairs):
                if len(gatePair) == 2:
                    optimalRoute = constructOptimalRoute(
                        doubleEdgePairs(triangleEdgePairs, gatePair), maxWidth, maxLength_triplet, gatePair)
                    if optimalRoute:
                        optimalRoutes.append(
                            [[triplet[0], triplet[1]],
                                [triplet[1], triplet[2]],
                                gatePairs[i][0], gatePairs[i][1],
                                optimalRoute[0], optimalRoute[1]])
            allOptimalRoutes += optimalRoutes

    optimalRoutes = groupGates(allOptimalRoutes)
    testParcels = [[i] for i in range(len(allLand))]

    # quick and simple way of specifying start and end polygons.
    # simply use the start and end parcels found in the original paper,
    # as opposed to the separate habitats defined in the paper, because
    # those exist outside of the land in question.
    for i, polygon in enumerate(allLand):
        if polygon.contains(Point([713183, 4297612])):
            testStartPolygon = i
        if polygon.contains(Point([740410, 4282598])):
            testEndPolygon = i

    resultArray = solve(maxWidth, maxLength_overall, doubleRoutes(optimalRoutes, testStartPolygon, testEndPolygon), testStartPolygon,
                        testEndPolygon, testParcels, polygons, costs, budget)

    # get result of pathing solution, with binary decision variable.
    # TODO: write to shapefile
    finalPath = set()
    for decision in resultArray[0]:
        for poly in decision[5]:
            finalPath.add(allLand[poly])
    width = resultArray[1]  # optimal value
    length = resultArray[2]  # total length

    w = shp.Writer('./testfile')
    w.field('name', 'C')
    for shape in finalPath:
        w.poly(shape)


corridorConstructor()
