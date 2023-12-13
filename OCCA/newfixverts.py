import matplotlib.pyplot as plt
import polycode
import copy
import math
from shapely.geometry import * 


vertfile = "C:/rstjohn/SLU_Exp/polygon_2ha_verts.txt"
newfile = "C:/rstjohn/SLU_Exp/polygon_2ha_verts_now.txt"

def addverts(d1, d2):
	fixed = False
	while not fixed:
		fixed = True
		for e1 in d1: 
			# line1 = LineString(d1[e1]).buffer(0.1)
			for e2 in d2:
				# line2 = LineString(d2[e2]).buffer(0.1)
				if [x for x in d1[e1] if x in d2[e2]] ==[]: # and line1.intersects(line2):
					for p2 in d2[e2]:
						if distance(d1[e1][0], d1[e1][1]) + 0.002 > distance(p2, d1[e1][0]) + distance(p2, d1[e1][1]):  #Point(p1).within(line2):
							newe1 = [p2, d1[e1][0]]
							newe2 = [p2, d1[e1][1]]
							newe1.sort()
							newe2.sort()
							d1[str(newe1)] = newe1
							d1[str(newe2)] = newe2	
							del d1[e1]
							fixed = False
							# print "fixing..."
							# print p2
							break
				if not fixed:
					break
						
			if not fixed:
				break		
	return d1

def distance(a, b):
    y = b[1]-a[1]
    x = b[0]-a[0]
    ans=y*y+x*x*1.0000
    return math.sqrt(ans)

	
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
###########################################################
	
	
	
	
	

polygons = polycode.polygons



ids = polygons.keys()
ids.sort()
badpolys = [1400, 3824, 10076, 10081, 10084, 10086, 10091,10094, 10105, 10106, 10107, 10117, 10119, 10121, 10130, 10131, 10138, 10146 ]
fw = open(newfile, 'a')
fixli = [] #111, 128, 405, 407, 568, 569, 593, 596, 650, 651, 669, 706, 708, 849, 850, 1160, 1162, 1163]
cc = 0
for p in ids:
	if p not in badpolys:
		continue
	# cc=cc+1
	# if cc == 10:
		# print "Bad polys are "+str(badpolys)
		# print "Fixed polys are " + str(fixli)
		# cc = 0
	print "On polygon "+str(p) + " which is # " + str(ids.index(p)) + " out of " + str(len(ids))
	# print badpolys
	newp = copy.deepcopy(polygons[p])	
	# polycode.plotpoly(newp, 'g')
	# plt.show()
	changed = False
	# adjli = polycode.getadjs(p)
	
	# print "There are " + str(len(adjli))+" adjs."
	# print str(p) + "   ,  "+ str(len(adjli))
	# for a in adjli:
		# print a
		# newp= addverts(newp, polygons[a])
	if newp != polygons[p]:
		# print" fixed poly "+ str(p)
		fixli.append(p)
		# polycode.plotpoly(newp, 'g')
		# plt.show()
		pli = pdicttoli(newp)
		if pli == 0:
			badpolys.append(p)
			print "BAD POLY!!!"
			# break
		else:	
			
			for v in pli:
				writeline = str(p) + "\t" + str(v[0]) + "\t" + str(v[1]) + '\n'
				fw.write(writeline)
	else:
		print "poly unchanged."
		f = open(vertfile)
		gotpol = False
		for line in f:
			myarr = line.split()
			if int(myarr[0]) == p:
				fw.write(line)
				gotpoly = True
			elif gotpol:
				break
		f.close()
fw.close

print "THE END"