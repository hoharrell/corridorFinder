from shapely.geometry import *
import matplotlib.pyplot as plt
from shapely.ops import polygonize_full


lines = [((0.1, 0), (1, 1)),((0, 0), (0.1, 1)), ((0.1, 1), (1, 1)), ((1, 1), (1, 0)),
 ((1, 0), (0.1, 0)) ]  #((5, 5), (5, 6)),  ((1, 1), (10, 10))

for e in lines:
	x = [e[0][0], e[1][0] ]
	y = [e[0][1], e[1][1] ]
	plt.plot(x,y, "b")
plt.show()

polys, dangles, cuts, invalids = polygonize_full(lines)

print len(polys)
print list(polys.geoms)