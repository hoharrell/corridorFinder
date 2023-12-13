############# Poly Code###################
#contains: polygons dict
#contains functions: getpolygon, getadjs, 
print "loading polycode..."

import matplotlib.pyplot as plt
from shapely.geometry import * 
import copy
import math as math
import time
import triangle
from shapely.ops import polygonize_full


# startunit = 3824
# endunit = 3825

# clustfile = "C:/rstjohn/SLU_Exp/polygons_2ha.txt"
# vertfile = "C:/rstjohn/SLU_Exp/polygon_2ha_verts.txt"
# tripfile = "C:/rstjohn/SLU_Exp/SLU_2ha_trips.txt"
####################### FUNCTIONS #########################################

def addlineverts(d1, d2):
	fixed = False
	while not fixed:
		fixed = True
		for e1 in d1: 
			line1 = LineString(d1[e1]).buffer(0.1)
			for e2 in d2:
				line2 = LineString(d2[e2]).buffer(0.1)
				if [x for x in d1[e1] if x in d2[e2]] ==[] and line1.intersects(line2):
					for p1 in d1[e1]:
						if distance(d2[e2][0], d2[e2][1]) + 0.05 > distance(p1, d2[e2][0]) + distance(p1, d2[e2][1]):  #Point(p1).within(line2):
							newe1 = [p1, d2[e2][0]]
							newe2 = [p1, d2[e2][1]]
							newe1.sort()
							newe2.sort()
							d2[str(newe1)] = newe1
							d2[str(newe2)] = newe2
							del d2[e2]
							fixed = False
							break
					if not fixed: 
						break
					for p2 in d2[e2]:
						if distance(d1[e1][0], d1[e1][1]) + 0.05 > distance(p2, d1[e1][0]) + distance(p2, d1[e1][1]):  #Point(p1).within(line2):
							newe1 = [p2, d1[e1][0]]
							newe2 = [p2, d1[e1][1]]
							newe1.sort()
							newe2.sort()
							d1[str(newe1)] = newe1
							d1[str(newe2)] = newe2	
							del d1[e1]
							fixed = False
							break
				if not fixed:
					break
						
			if not fixed:
				break
			
	return d1, d2
	
def correspondingpoly(d1, d2, d3, g12, g23):
	# #input: 3 poly dicts, 2 sets of gates
	# #output: dict of poly corresponding to gates
	# if len(g12) == 1 and len(g23) == 1:
		# if str(g12[0]) in d2 and str(g23[0]) in d2:
			# return d2
	dp = {}
	dall = copy.deepcopy(d2)
	wrapped = True
	for e in d2:
		if e not in d1 and e not in d3:
			wrapped = False
			break
	if wrapped:
		ends = getnewedges(g12)
		dp[str(ends)] = ends
		return dp
	for e in d1:
		if e in d2:
			del dall[e]
		else:
			dall[e] = d1[e]
	if d1 != d3:
		for e in d3:
			if e in d2:
				del dall[e]
			else:
				dall[e] = d3[e]
		# plotpoly(dall, 'r')
		# for i in g12+g23:
			# x = [i[0][0], i[1][0]]
			# y = [i[0][1], i[1][1]]
			# plt.plot(x, y)
		# plt.show()
		li = dtolist(dall)
		gates = g12+g23
	else:
		li = dtolist(dall)
		gates = g12
	tempd = mergepolys(d1, d2)
	tempd = mergepolys(tempd, d3)
	# plotpoly(tempd, 'k')
	# # plt.axis([0, 1, 0, 1])
	# plt.show()
	pall = getpolygon(tempd)
	bigp = pall.buffer(0.000002)
	if len(g12) == 1 and not bigp.contains(LineString(g12[0])):
		return 5
	elif len(g23) == 1 and not bigp.contains(LineString(g23[0])):
		# print "yupyupyup"
		return 5
	# for i in  li:
		# x = [i[0][0], i[1][0]]
		# y = [i[0][1], i[1][1]]
		# plt.plot(x, y, 'k')
	# for i in  gates:
		# x = [i[0][0], i[1][0]]
		# y = [i[0][1], i[1][1]]
		# plt.plot(x, y)
	# plt.show()
	li = fixdj(li, gates)
	if li == 66:
		return 5
	# for i in li:
		# for j in li:
			# if edgesintersect(i, j):
				# print "intersection!! "+str(i) +"   "+ str(j)
	polys, dangles, cuts, invalids = polygonize_full(li)
	newpolys = []
	for p in list(polys.geoms):
		templi = list(p.exterior.coords)
		pedges = []
		for v in range(0, len(templi)-1):
			pt1 = [templi[v][0], templi[v][1]]
			pt2 = [templi[v+1][0], templi[v+1][1]]
			tempedge = [pt1, pt2]
			tempedge.sort()
			pedges.append(tempedge)
		# for int in p.interiors:
            # interior_coords += i.coords[:]
		for i in p.interiors:
			tempholeli = list(i.coords)
			for v in range(0, len(tempholeli)-1):
				pt1 = [tempholeli[v][0], tempholeli[v][1]]
				pt2 = [tempholeli[v+1][0], tempholeli[v+1][1]]
				tempedge = [pt1, pt2]
				tempedge.sort()
				pedges.append(tempedge)	
		newpolys.append(pedges)
		# for i in pedges:
			# x = [i[0][0], i[1][0]]
			# y = [i[0][1], i[1][1]]
			# plt.plot(x, y)
		
	# plt.show()
					
	# print "There are new polys "+str(len(newpolys))
	for p in newpolys:
		# for i in p:
			# x = [i[0][0], i[1][0]]
			# y = [i[0][1], i[1][1]]
			# plt.plot(x, y)
		# plt.show()
		if [x for x in p if x in g12] != [] and [x for x in p if x in g23] != []:
			for e in p:
				# print "got the poly!!!"
				dp[str(e)] = e
			break
	# plt.axis([0, 1, 0, 1])
	# plt.show()
	
	return dp

def distance(a, b):
    y = b[1]-a[1]
    x = b[0]-a[0]
    ans=y*y+x*x*1.0000
    return math.sqrt(ans)
        
def dtolist(d):
	#input: dictionary of edges
	#output: list of edges
	li = []
	for e in d:
		li.append(d[e])
	return li

def edgesintersect(e1, e2):
    #input: dict of edges
    #output: True if polygon edges intersect
	if listsintersect(e1, e2) == []:
		if LineString(e1).intersects(LineString(e2)):
			return True
		if Point(e1[0]).distance(LineString(e2)) < 0.000001 or Point(e1[1]).distance(LineString(e2)) < 0.000001:
			return True
	elif ifparallel(e1, e2):
		return  True  
	return False
	
def findgates(dict1, dict2):
	#input: 2 dicts
	#output: list of edges that are gates
	d1 = copy.deepcopy(dict1)
	d2 = copy.deepcopy(dict2)
	gates = []
	sharededges = [d1[x] for x in d1 if x in d2]
	# print sharededges
	# for e1 in d1:
		# if e1 in d2:
			# sharededges.append(d1[e1])
	# for i in sharededges:
		# x = [i[0][0], i[1][0]]
		# y = [i[0][1], i[1][1]]
		# plt.plot(x, y)
	if len(sharededges) == 1:
		sharededges[0].sort()
		return sharededges
	newedges = getnewedges(sharededges)
	# print newedges
	# for i in newedges:
		# x = [i[0][0], i[1][0]]
		# y = [i[0][1], i[1][1]]
		# plt.plot(x, y)
	# plt.show()
	dnew = mergepolys(d1, d2)
	# pnew = getpolygon(dnew)
	for e in newedges:
		myf = getfragments(e, dnew)
		if myf==66:
			return 66
		# print "myf is "+str(myf)
		for f in myf:
			f.sort()
			gates.append(f)
	return gates

def fixdj(li, gateli):
	#input: list of edges
	#output: fragmented edges
	stilldj = True
	d = {}
	for i in gateli:
		d[str(i)] = i
	starttime = time.time()
	while stilldj:
		currtime = time.time()
		if currtime - starttime > 20:
			return 66
		stilldj = False
		for e1 in li:
			for e2 in gateli:
				if edgesintersect(e1, e2) and ifparallel(e1, e2) == False:
					# print "e1 is " + str(e1)
					# print "e2 is "+str(e2)
					fli = getfragments(e1, d)
					if len(fli) == 1 and fli[0] == e1 or [x for x in fli if x in li] == fli:
						stilldj = False
					else:
						stilldj = True
						# print fli
						li.remove(e1)
						for f in fli:
							f.sort()
							li.append(f)
					break
			if stilldj:
				break
	for e in gateli:
		if e not in li:
			e.sort()
			li.append(e)
	return li

def ifparallel(e1, e2):
	#input: 2 edges
	#output: true if parallel and overlapping
	if e1 != e2 and Point(e1[0]).distance(LineString(e2)) < 0.000001 and Point(e1[1]).distance(LineString(e2)) < 0.000001:
		return  True 
	if e1 != e2 and Point(e2[0]).distance(LineString(e1)) < 0.000001 and Point(e2[1]).distance(LineString(e1)) < 0.000001:
		return  True  
	return False

def getadjs(id):
	#inputs: polyid
	# output: list of adj polys
	adjs = []
	for a in polygons.keys():
		for e in polygons[id]:
			if e in polygons[a] and  overlaps(a, id) == False:
				adjs.append(a)
				break
	return adjs

def getfragments(e, d):
	#input: edge and polydict
	#output: list of fragments of edge
	ptli = []
	frags = []
	for e1 in d:
		if e != e1 and e1[0] in e and Point(e1[1]).distance(LineString(e)) < 0.0001:
			otherpt = [x for x in e not in e1]
			e = [e1[1], otherpt]
			if e[0][0] > e[1][0]:
				e.sort()
		elif e != e1 and e1[1] in e and Point(e1[0]).distance(LineString(e)) < 0.0001:
			otherpt = [x for x in e not in e1]
			e = [e1[0], otherpt]
			if e[0][0] > e[1][0]:
				e.sort()
	for e1 in d:
		if edgesintersect(d[e1], e):
			temppt = getintersectionpt(d[e1], e)
			if temppt not in ptli:
				ptli.append(temppt)
				# print "temppt is " +str(temppt)
	if len(ptli) == 0:
		frags.append(e)
	elif len(ptli) == 1:
		frags.append([e[0], ptli[0]])
		frags.append([e[1], ptli[0]])
	else:
		endpt = e[0]
		newpt = e[1]
		st = time.time()
		# print "Starting newpt is "+str(newpt)
		while len(ptli) > 0:
			ct = time.time()
			if ct-st>20:
				return 66
			for p in ptli:
				if distance(endpt, newpt) > distance(endpt, p) or distance(newpt, p)< 0.0001:
					newpt = p
			# print ptli
			# print newpt
			frags.append([endpt, newpt])
			ptli.remove(newpt)
			endpt = newpt
			newpt = e[1]
		frags.append([endpt, newpt])
		# print frags
	for f in frags:
		if f[0][0] > f[1][0]:
			f.sort()
	return frags

	
def getintersectionpt(line1, line2):
    # fxn that returns the intersection point of two lines
	if line1 != line2:
		if Point(line1[0]).distance(LineString(line2)) < 0.000001 and Point(line1[1]).distance(LineString(line2)) < 0.000001:
			if line1[0] in line2:
				return line1[1]
			return line1[0]
		if Point(line2[0]).distance(LineString(line1)) < 0.000001 and Point(line2[1]).distance(LineString(line1)) < 0.000001:
			if line2[0] in line1:
				return line2[1]
			return line2[0]
	for p in line1:
		 if Point(p).distance(LineString(line2)) < 0.000001 and p not in line2:
			return p
	for p in line2:
		if Point(p).distance(LineString(line1)) < 0.000001 and p not in line1:
			return p
	temp1=line1[0][1]-line1[1][1]
	temp2=line1[0][0]-line1[1][0] 
	if temp2 != 0: 
		m1=temp1/temp2
	else:
		m1 = temp1 / 0.000000001
	temp1=line2[0][1]-line2[1][1] 
	temp2=line2[0][0]-line2[1][0] 
	if temp2 != 0: 
		m2=temp1/temp2
	else:
		m2 = temp1 / 0.000000001
	b1=line1[0][1]-m1*line1[0][0]
	b2=line2[0][1]-m2*line2[0][0]
	temp1=b2-b1
	temp2=m1-m2
	if temp2 != 0:
		newx=temp1/temp2
	else:
		newx=temp1/0.000000001
	newy=m1*newx+b1
	trnx=round(newx,9)
	trny=round(newy,9)
	mypt=[trnx, trny]
	return mypt
	
def getnewedges(sharededges):
	#input: list of edges
	#output: list of simplified edges
	newedges = []
	if len(sharededges) == 1:
		return sharededges
	endpts = sharededges[0]
	# print "endpts" +str(endpts)
	sharededges.remove(endpts)
	goagain = True
	while len(sharededges) > 0:
		while goagain:
			goagain = False
			for e in sharededges:
				if e[0] in endpts:
					endpts.remove(e[0])
					endpts.append(e[1])
					sharededges.remove(e)
					goagain = True
					break
				elif e[1] in endpts:
					endpts.remove(e[1])
					endpts.append(e[0])
					sharededges.remove(e)
					goagain = True
					break
			if goagain == False:
				newedges.append(endpts)
				# print endpts
				if len(sharededges) == 0 :
					break
				goagain = True
				endpts = sharededges[0]
				# print "endpts "+str(endpts)
				sharededges.remove(endpts)	
	for e in newedges:
		if e[0][0] > e[1][0]:
			e.sort()
	# print newedges
	return newedges

def getpolygon(d1):
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
			for e in d:
				if d[e][0] == pli[-1] and d[e][1] != pli[-2]:
					pli.append(d[e][1])
					pt2 = d[e][1]
					del d[e]
					break
				elif d[e][1] == pli[-1] and d[e][0] != pli[-2]:
					pli.append(d[e][0])
					pt2 = d[e][0]
					del d[e]
					break
		if pt1 == pt2:
			li.append(pli)
			pli = []
    if len(li) == 1:
		return Polygon(li[0])
    else:
		big = []
		p0 = Polygon(li[0])
		for i in range(1, len(li)):
			if p0.contains(Polygon(li[i])):
				big = li[0]
			elif Polygon(li[i]).contains(p0):
				big = li[i]
		holes = li
		holes.remove(big)
    return Polygon(big, holes)

def gettris(d):
    #input: dict of edges
    #output: dict of tris
	tprep = {}
	verts = []
	segs = []
	for e in d:   #get edges
		p1 = d[e][0]
		p2= d[e][1]
		if p1 not in verts:
			verts.append(p1)
		if p2 not in verts:
			verts.append(p2)
		templi=[verts.index(p1), verts.index(p2)]
		segs.append(templi)
	myp = getpolygon(d)
	if list(myp.interiors) != []: 
		holes = list(myp.interiors)
		for h in holes: 
			holepoly = Polygon(h)
			pt = holepoly.representative_point()
			tprep['holes'] = [[list(pt.coords)[0][0],  list(pt.coords)[0][1]]]
	tprep['vertices'] = verts
	tprep['segments'] = segs
	t = triangle.triangulate(tprep, 'p')
	tris = {}
	myind = 0
	for x in t['triangles']:
		p1 = [t['vertices'][x[0]][0], t['vertices'][x[0]][1]]
		p2 = [t['vertices'][x[1]][0], t['vertices'][x[1]][1]]
		p3 = [t['vertices'][x[2]][0], t['vertices'][x[2]][1]]
		e1 = [p1, p2]
		e1.sort()
		e2 = [p2, p3]
		e2.sort()
		e3 = [p3, p1]
		e3.sort()
		tris[myind] = [e1, e2, e3]
		myind += 1
	return tris

def listsintersect(a, b):
	#input: 2 lists
	#output: list of a intersect b
	li = []
	for x in a:
		if x in b:
			li.append(x)
	return li

# def makefrags(le):
	#input: 2 intersecting edges
	#output: their resulting lines
	newpt = getintersectionpt(le[0], le[1])
	frags = []
	for e in le:
		for i in e:
			a = [i, newpt]
			# print a
			if a[0] > a[1]:
				a.sort()
			if a[0] < a[1] and a not in le:
				frags.append(a)
	return frags
	
def mergepolys(d1, d2):
	#input: 2 poly dicts
	# output: dict of merged polys
	newd = copy.deepcopy(d1)
	d2t = copy.deepcopy(d2)		
	for e in d2t:
		if e in newd:
			del newd[e]
		else:
			newd[e] = d2t[e]
	return newd

def onecontained(d1, d2, d3):
	#input: 3 poly dicts
	#output: true if one contained in others:
	d1con = True
	d2con = True
	d3con = True
	for i in d2:
		if i not in d1 and i not in d3:
			d2con = False
	for i in d1:
		if i not in d2 and i not in d3:
			d1con = False
	for i in d3: 
		if i not in d2 and i not in d1:
			d3con = False
	if d1con or d3con or d2con:
		return True
	return False
		
def overlaps(x1, x2):
	#inputs: 2 poly ids
	#outputs: True if overlapping
	li1 = []
	li2 = []
	if x1 in clusters.keys():
		li1 = clusters[x1]
	li1.append(x1)
	if x2 in clusters.keys():
		li2 = clusters[x2]
	li2.append(x2)	
	if listsintersect(li1, li2) == []:
		return False
	return True

def plotpoly(d, c):
    #input: poly dict, color string
    #output: plot of polygon
	for e in d:
		x = [d[e][0][0], d[e][1][0] ]
		y =  [d[e][0][1], d[e][1][1] ]
		plt.plot(x,y, c)
	return "poly plotted"

def simplifyedges(li):
	#input: list of edges
	#output: list of nonfragmented edges
	stillfragged = True
	while stillfragged:
		stillfragged = False
		for i in li:
			for j in li:
				if i != j and i[0] in j:
					enew = [j[0], j[1], i[1]]
					enew.remove(i[0])
					if Point(i[0]).distance(LineString(enew)) < 0.0001:
						stillfragged = True
						li.remove(i)
						li.remove(j)
						if enew[0][0] > enew[1][0]:
							enew.sort()
						li.append(enew)
						break
				elif i!= j and i[1] in j:
					enew = [j[0], j[1], i[0]]
					enew.remove(i[1])
					if Point(i[1]).distance(LineString(enew)) < 0.0001:
						stillfragged = True
						li.remove(i)
						li.remove(j)
						li.append(enew)
						break
			if stillfragged:
				break
	return li

	
	
# ############################ Polygons Dict ################################################

# #get polygons
# f = open(vertfile, 'r')
# x = f.readlines()
# lastline= x[-1]
# polygons = {}  #dict of [polyid] edges
# temparr = x[0].split()
# pastid = int(temparr[0])
# templi = []
# ptsgot = []
# hasholeli = []

# for e in x:
	# mysplit = e.split()
	# # print mysplit
	# if pastid != int( mysplit[0] ) or e == lastline:  #if starting new poly
		# polygons[pastid] = {}
		# addedge = [templi[0], templi[-1]]
		# addedge.sort()
		# hashole = False
		# for p in range(0, len(templi) - 1):
			# if p > 0 and templi[p] in templi[0:p-1] and templi[p] != templi[-1]:
				# hashole = True
				# if pastid not in hasholeli:
					# hasholeli.append(pastid)
			# else:
				# myedge = [templi[p], templi[p + 1]]
				# myedge.sort()            
				# polygons[pastid][str(myedge)] = myedge   
		# if addedge not in templi and [addedge[1], addedge[0]] not in templi and addedge[0] != addedge[1] and hashole == False:
			# polygons[pastid][str(addedge)] = addedge                   
		# templi = []
        # pastid = int( mysplit[0] )
	# a = [ float( mysplit[1] ), float( mysplit[2] ) ]
	# templi.append(a)

# bad = [487, 10072, 10092]
# for b in bad:
	# if b in polygons:
		# del polygons[b]


# #get clusters
# clusters = {}
# ff = open(clustfile, 'r')
# for line in ff:
	# strli=line.split()
	# id=int(strli[0])
	# # if id not in polygons.keys():
		# # continue
	# templi=[]
	# for i in range(1, len(strli)):
		# x=int(strli[i])
		# if x in polygons.keys():
			# templi.append(x)
	# clusters[id] = templi
# ff.close()



# #get triplets
# triplets = []
# ff=open(tripfile)
# count = 0
# last = 0
# for line in ff:
	# s = line.split()
	# temptrip = [int(s[0]), int(s[1]), int(s[2])] 
	# if [x for x in temptrip if x in [487, 10072, 10092]] == []:
		# triplets.append(temptrip)
# ff.close() 


# for e in polygons[17]:
	# if e in polygons[3139]:
		# print e
# d = mergepolys(polygons[17], polygons[3139])
# plotpoly(d, 'g')
# print hasholeli
# plotpoly(polygons[487], 'g')
# plotpoly(polygons[1536], 'b')
# plt.show()


print "polycode imported"