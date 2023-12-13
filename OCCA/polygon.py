class Polygon

#create dict of polygon
f = open(polyfile, 'r')
x = f.readlines()
lastline= x[-1]
polygons = {}  #dict of [polyid] of "edges", "num holes", "hole edges", "id"
holes = {}  #dict of ONLY edges in holes)
pastid = 0
templi = []
ptsgot = []
for e in x:
	mysplit = e.split()
	if pastid != int( mysplit[0] ) or e == lastline:  #if starting new poly
		polygons[pastid] = {}
		polygons[pastid]["num holes"] = 0
		polygons[pastid]["id"] = pastid
		polygons[pastid]["edges"] = {}
		addedge = [templi[0], templi[-1]]
		if addedge[0][0] > addedge[1][0]:
			addedge.reverse()
		inhole = False
		for p in range(0, len(templi) - 1):
			if p > 0 and templi[p] == templi[0]:
				inhole = True
				polygons[pastid]["num holes"] += 1
				holes[pastid] = {}
			else:
				if templi[p][0] < templi[p + 1][0]:
					myedge = [templi[p], templi[p + 1]]
				else:
					myedge = [templi[p + 1], templi[p]]            
				if inhole == True:
					holes[pastid][str(myedge)] = myedge 
				else:
					polygons[pastid]['edges'][str(myedge)] = myedge   
		if addedge not in templi and [addedge[1], addedge[0]] not in templi and addedge[0] != addedge[1] and polygons[pastid]["num holes"]==0:
			polygons[pastid]["edges"][str(addedge)] = addedge                   
		templi = []
		if polygons[pastid]['num holes'] > 0:
			polygons[pastid]["hole edges"] = holes[pastid]
		else:
			polygons[pastid]["hole edges"] = []
        pastid = int( mysplit[0] )
	a = [ float( mysplit[1] ), float( mysplit[2] ) ]
	templi.append(a)