from ground.base import get_context
from sect.triangulation import Triangulation
context = get_context()
Contour, Point = context.contour_cls, context.point_cls
print(Triangulation.delaunay([Point(0, 0), Point(1, 0), Point(0, 1)], context=context).triangles(
) == [Contour([Point(0, 0), Point(1, 0), Point(0, 1)])])
Polygon = context.polygon_cls
triangulation = (Triangulation.constrained_delaunay(Polygon(Contour(
    [Point(0, 0), Point(1, 0), Point(0, 1)]), []), context=context))
print(triangulation)
print(triangulation.triangles())
