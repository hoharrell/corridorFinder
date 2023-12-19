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


polygons = importData()

a = polygons[0]
b = polygons[1]
print(a.exterior.coords)
print(a.area)
print("\n")
print(b.exterior.coords)
print(b.area)
c = unary_union([a,b])

