# fix SLU verts
from shapely.geometry import * 
import copy
import matplotlib.pyplot as plt

vertfile = "C:/rstjohn/SLU_Exp/parcel_verts.txt"
adjfile = "C:/rstjohn/SLU_Exp/parcel_adjs.txt"



	
	

# parcels = polycode.polygons

def getvertlist(d):
    #input: poly dict
    #output: polygon
    pli = []
    li = []
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
		return li[0]
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
		return big + holes

def fixverts(p):
	#input: poly id
	#output: fixed polydict
	d = copy.deepcopy(polygons[p])
	if p not in adjs:
		return polygons[p]
	for q in adjs[p]:
		# print len(parcels[q])
		# print len(parcels[p])
		qecount = 0
		for qe in polygons[q]:
			qecount = qecount + 1
			# print "On qe edge " + str(qecount) + " of " + str(len(parcels[q]))
			qedge = polygons[q][qe]
			keepgoing = True
			while keepgoing:
				keepgoing = False
				pecount = 0 
				for pe in d:
					pecount = pecount + 1
					# print "On pe edge " + str(pecount)
					pedge = d[pe]
					if qedge[0] not in pedge and Point(qedge[0]).distance(LineString(pedge)) < 0.0001:
						# print "in forst"
						for i in pedge:
							newe = [qedge[0], i]
							d[str(newe)] = newe
							print newe
						del d[pe]
						keepgoing = True
						break
					elif qedge[1] not in pedge and Point(qedge[1]).distance(LineString(pedge)) < 0.0001:
						# print "in second"
						for i in pedge:
							newe = [qedge[1], i]
							d[str(newe)] = newe
							print newe
						del d[pe]
						keepgoing = True
						break
	return d

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
	print "got list"
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
	return big + holes

#get adjs
adjs = {}
ff = open(adjfile)
for line in ff:
	strarr = line.split()
	if int(strarr[0]) not in adjs:
		adjs[int(strarr[0])] = [int(strarr[1])]
	elif int(strarr[1]) not in adjs[int(strarr[0])]:
		adjs[int(strarr[0])].append(int(strarr[1]))
	if int(strarr[1]) not in adjs:
		adjs[int(strarr[1])] = [int(strarr[0])]
	elif int(strarr[0]) not in adjs[int(strarr[1])]:
		adjs[int(strarr[1])].append(int(strarr[0]))
ff.close()

#get polygons
f = open(vertfile, 'r')
x = f.readlines()
lastline= x[-1]
polygons = {}  #dict of [polyid] edges
temparr = x[0].split()
pastid = int(temparr[0])
templi = []
for e in x:
	mysplit = e.split()
	if pastid != int( mysplit[0] ) or e == lastline:  #if starting new poly
		polygons[pastid] = {}
		addedge = [templi[0], templi[-1]]
		if addedge[0][0] > addedge[1][0]:
			addedge.reverse()
		hashole = False
		for p in range(0, len(templi) - 1):
			if p > 0 and templi[p] in templi[0:p-1] and templi[p] != templi[-1]:
				hashole = True
			else:
				if templi[p][0] < templi[p + 1][0]:
					myedge = [templi[p], templi[p + 1]]
				else:
					myedge = [templi[p + 1], templi[p]]            
				polygons[pastid][str(myedge)] = myedge   
		if addedge not in templi and [addedge[1], addedge[0]] not in templi and addedge[0] != addedge[1] and hashole == False:
			polygons[pastid][str(addedge)] = addedge                   
		templi = []
        pastid = int( mysplit[0] )
	a = [ float( mysplit[1] ), float( mysplit[2] ) ]
	templi.append(a)


outfile = open("C:/rstjohn/SLU_Exp/parcel_verts_fixed4.txt", 'w')
count = 0
# polycode.plotpoly(parcels[487], 'r')
# plt.show()
# li = getpolygon(parcels[19])
# print "Done"

for p in polygons:
	count += 1
	if count <= 3007 or count >3501:
		continue
	print "on parcel #"+str(count) + " out of " + str(len(polygons))
	d = fixverts(p)
	print "writing to file."
	if d == polygons[p]:
		f = open(vertfile)
		gotpoly = False
		for line in f:
			strarr = line.split()
			if int(strarr[0]) == p:
				gotpoly = True
				outfile.write(line)
			elif int(strarr[0]) != p and gotpoly:
				break
		f.close()
	else:
		print "poly changed"
		vertli = getvertlist(d)
		for i in vertli:
			writeline =str(p) + "\t" + str(i[0]) + "\t" + str(i[1]) + "\n"
			outfile.write(writeline)
outfile.close()


	