import copy
import polycode
from shapely.geometry import * 
import matplotlib.pyplot as plt
import math

newvertfile = "C:/rstjohn/SLU_Exp/parcel_verts_new.txt"
adjfile = "C:/rstjohn/SLU_Exp/polygon_2ha_adjs.txt"


def distance(a, b):
    y = b[1]-a[1]
    x = b[0]-a[0]
    ans=y*y+x*x*1.0000
    return math.sqrt(ans)


def fixverts(id):
	d = copy.deepcopy(polygons[id])
	if id not in adjs:
		return d
	done = False	
	while not done:
		done = True
		for ei in d:
			for j in adjs[i]:
				for ej in polygons[j]:
					for pt in polygons[j][ej]:
						# print pt
						# print id, j 
						if  distance(d[ei][0], pt) + distance(d[ei][1], pt) < distance(d[ei][0], d[ei][1]) +0.001 and pt not in d[ei]:
							newe1 = [pt, d[ei][0]]
							newe1.sort()
							d[str(newe1)] = newe1
							newe2 = [pt, d[ei][1]]
							newe2.sort()
							d[str(newe2)] = newe2
							del d[ei]
							print "Fixed one!"
							done = False
						if not done:
							break
					if not done:
						break
				if not done:
					break
			if not done:
				break
		
	return d

	
def pdicttoli(d1):
    #input: poly dict
    #output: polygon
    pli = []
    li = []
    d = copy.deepcopy(d1)
    while len(d) > 0:
		if pli == []:
			for e in d:
				pli = [d[e][0], d[e][1]]
				pt1 = d[e][0]
				pt2 = d[e][1]
				del d[e]
				break
		while pt1 != pt2:
			checkedall = True
			for e in d:
				if d[e][0] == pli[-1] and d[e][1] != pli[-2]:
					pli.append(d[e][1])
					pt2 = d[e][1]
					del d[e]
					checkedall = False
					break
				elif d[e][1] == pli[-1] and d[e][0] != pli[-2]:
					pli.append(d[e][0])
					pt2 = d[e][0]
					del d[e]
					checkedall = False
					break
			if checkedall:
				print "error in d to li conversion"
				return 0
		if pt1 == pt2:
			li.append(pli)
			pli = []
    if len(li) == 1:
		return li[0]
    else:
		big = []
		p0 = Polygon(li[0])
		for i in range(1, len(li)):
			if p0.contains(Polygon(li[i])):
				big = li[0]
				li.remove(big)
				break
			elif Polygon(li[i]).contains(p0):
				big = li[i]
				li.remove(big)
				break
		holes = []
		for h in li:
			holes = holes + h
		# print "has holes"
    return big + holes

		
polygons = polycode.polygons
triplets = polycode.triplets
ids = polygons.keys()
ids.sort()
fixed = 0


adjs = {} 

# fa = open(adjfile)
# for line in fa:
	# templi = line.split()
	# adjli = []
	# for i in templi[1:]:
		# if int(i) in polygons:
			# adjli.append(int(i))
	# adjs[int(templi[0])] = adjli
# fa.close()
# print "have adjs"



# f = open(newvertfile, 'a')
# badpolys = []
for i in ids:
	if i  != 3824:
		continue
	print "On polygon "+str(i) + " which is # " + str(ids.index(i)) + " out of " + str(len(ids))
	# edge = [[1621680.615,7094884.421], [1621703.189,7094861.227]]
	# edge.sort()
	# del polygons[i][str(edge)]
	# edge = [[1621680.615,7094884.421], [1621703.42, 7094860.996]]
	# edge.sort()
	# del polygons[i][str(edge)]
	
	polycode.plotpoly(polygons[i], 'r')
	plt.show()
	# d = fixverts(i)
	# print len(d)
	# polycode.plotpoly(d, 'k')
	# plt.show()
	# pli = pdicttoli(d)
	# if pli == 0:
		# badpolys.append(i)
	# else:	
		# for v in pli:
			# writeline = str(i) + "\t" + str(v[0]) + "\t" + str(v[1]) + '\n'
			# f.write(writeline)
	# print badpolys
	# print "written to file"
# f.close()


print "Done!"
	