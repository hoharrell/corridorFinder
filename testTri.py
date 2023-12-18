from tri.delaunay.helpers import ToPointsAndSegments
from tri.delaunay import triangulate
from tri.delaunay.inout import output_triangles
from tri.delaunay.iter import TriangleIterator

# create points and segments for triangulation
pts_segs = ToPointsAndSegments()
# pts_segs.add_polygon([[(0, 0), (10, 0), (5, 10), (0, 0)],
#                       [(0, 0), (8, 2), (6, 4), (5, 7), (0, 0)]
#                       ],
#                      )
pts_segs.add_polygon([[(0, 0), (10, 0), (5, 10), (0, 0)]])

# triangulate the points and segments
dt = triangulate(pts_segs.points, pts_segs.infos, pts_segs.segments)
print(list(dt.triangles))
