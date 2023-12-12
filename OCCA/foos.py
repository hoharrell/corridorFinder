#### FUNCTIONS ###

import polycode
import copy

# import matplotlib.pyplot as plt
# from shapely.geometry import * 
# import numpy as np
import math as math
# import copy
# from scipy.spatial import Delaunay
# import triangle
# import triangle.plot as plot
# import polycode

########################### Functions #############################
def writeGPLPs(t, mypath):
	#input: triplet, file path
	#output: writes LP for each gate pair
	d = polycode.polygons
	d1 = copy.deepcopy(d[t[0]])
	d2 = copy.deepcopy(d[t[1]])
	d3 = copy.deepcopy(d[t[2]])
	if polycode.onecontained(d1, d2, d3):
		return 9
	g12 = polycode.findgates(d1, d2)
	g23= polycode.findgates(d2, d3)
	p = polycode.correspondingpoly(d1, d2, d3, g12, g23)
	if p =={}:
		return 9
	# tris = polycode.gettris(p)
	g12.sort()
	g23.sort()
	for i in range(0, len(g12)):
		if str(g12[i]) in p:
			for j in range(0, len(g23)):
				if str(g23[j]) in p:
					outfile = mypath + "blank" + str(t[0]) + "_" + str(t[1]) + "_" + str(t[2]) + "_" + str(i) + "_" + str(j) + ".cpx"
					return 0
					# subtrips = getsubtrips(tris, g12[i], g23[j])
					# subwidths = getsubwidths(tris, subtrips, g12[i], g23[j])
					# sublengths = getsublengths(tris, subtrips, g12[i], g23[j])
					# xx = writeLPfile(outfile, subtrips, subwidths, sublengths)
					# if xx == 9:
						# return 9
	



def altitude(e, p):
    #input: edge e, pt p
    #output: altitude of edge to point
    ##finds altitude of the point at e1 and e2 with base at e3
    pt1=e[0]
    pt2=e[1]
    mtop=pt2[1]-pt1[1]
    mbot=pt2[0]-pt1[0]
    if mbot!=0:
        m=mtop/mbot
    else:
        m=-100000000.0001
    b=pt1[1]-m*pt1[0]
    if m!=0:
        perpm=-(1/m)
    else:
        perpm=-100000000.0001
    perpb=p[1]-m*p[0]
    newx=(perpb-b)/(m-perpm)
    newy=m*newx+b
    newpt=[newx, newy]
    alt = distance(newpt, p)
    return(alt)

            
def distance(a, b):
    y = b[1]-a[1]
    x = b[0]-a[0]
    ans=y*y+x*x*1.0000
    return math.sqrt(ans)
        

def getsubtrips(tris, e1, e2):
    #input: dict of triangles, dicts of adj polys
    #output: list of subtriplets
	mysubs = []
	adjs = []  # get list of adj pairs
	for i in tris:  #get beginning and ending triangles
		if  e1 in tris[i] and ['s', i] not in adjs: 
			adjs.append(['s', i])
		if  e2 in tris[i] and [i, 'e'] not in adjs:
			adjs.append([i, 'e'])
	for t1 in tris:
		for t2 in tris:
			for e1 in tris[t1]:
				for e2 in tris[t2]:
					if ifwithin(e1, e2) and t1 != t2 and [t1, t2] not in adjs:
						adjs.append([t1, t2])
	for t in tris:
		tempadj = []
		for a in adjs:
			if t == a[0]:
				tempadj.append(a[1])
			elif t == a[1]:
				tempadj.append(a[0])
		for k1 in tempadj:
			for k2 in tempadj:
				if k1 != k2 and k2 !='s' and k1!='e' and [k1, t, k2] not in mysubs:
					mysubs.append([k1, t, k2])
	return mysubs

def getsubwidths(tris, subtrips, e1, e2):
    #input: dict of tris, list of subtrips, dicts of adj polys
    #output: list of widths
	widths = []
	for s in subtrips:
		s1 = tris[s[1]]
		mya = []
		myb = []
		myc = []
		if s[0] == 's' and e1 in s1: 
			mya = e1
		else:
			for e in s1:
				if e in tris[s[0]]:
					mya = e        
		if s[2] == 'e' and e2 in s1:
			myb = e2
		else:
			for e in s1:
				if e in tris[s[2]]:
					myb = e
		for e in s1:
			if e != mya and e != myb:
				myc = e
				break
		if mya[0] in myb:
			ptC = mya[0]
			ptB = mya[1]
		else:
			ptC = mya[1]
			ptB = mya[0]
		if myb[0] not in mya:
			ptA = myb[0]
		else:
			ptA = myb[1]
		len_a=distance(mya[0], mya[1])
		len_b=distance(myb[0], myb[1])
		len_c=distance(myc[0], myc[1])
		d = min(len_a, len_b)
		if mya == myb:
			widths.append(d)
		elif max(len_a, len_b, len_c) > len_c:
			widths.append(d)
		elif isConstrained(myc, tris):
			mydist = altitude(myc, ptC)
			widths.append(mydist)
		else:
			myw = SearchWidth(ptC, s1, myc, d, tris)
			widths.append(myw)
	return widths

def getsublengths(tris, subtrips, e1, e2):
    #input: dict of tris, list of subtrips
    #output: list of lengths
    lengths= []
    for s in subtrips:
        #print s
        s0 = []
        s2 = []
        if s[0] == 's':
            s0.append(e1)
        else:
            s0 = tris[s[0]]
        s1 = tris[s[1]]
        if s[2] == 'e':
            s2.append(e2)
        else:
            s2 = tris[s[2]]
        for e in s1:
            if e in s0:
                x = (e[0][0] + e[1][0]) / 2
                y = (e[0][0] + e[1][0]) / 2
                mid1 = [x,y]
            if e in s2:
                x = (e[0][0] + e[1][0]) / 2
                y = (e[0][0] + e[1][0]) / 2
                mid2 = [x,y]
        temp = distance(mid1, mid2)
        lengths.append (temp )
    return lengths



def ifwithin( e1, e2):
    #input: two edges
    #output: True if they are within epsilon, false ow
    if abs(e1[0][0] - e2[0][0])+abs(e1[1][0] - e2[1][0]) + abs(e1[0][1] - e2[0][1]) + abs(e1[1][1] - e2[1][1]) < 0.0001:
        return True
    return False
    
def isConstrained(e, tris):
    #input: edge, dict of tris
    #output: True if edge boundary, false otherwise
    for t in tris:
        if e in tris[t]:
            return False
    return True


def isObtuse(p1, p2, p3):
    #input: 3 vertices
    #output: True if angle obtuse, False otherwise
    A = distance(p1, p2)
    B = distance(p2, p3)
    C = distance(p1, p3)
    d = (A * A + B * B - C * C)/(2.0 * B * C)
    if d >0:
        return False
    return True
	
def SearchWidth(C, T, e, d, tris):
    #input: a la Demyen
    #output: width
    U = e[0]
    V = e[1]
    if C == U:
        print "C ==U !"
    if U == V:
        print "U == V!"
    if C == V:
        print "C == V!"
        
    if isObtuse(C, U, V) or isObtuse(C, V, U):
        return d
    dd= altitude(e, C)
    if dd > d:
        return d
    elif isConstrained(e, tris):
        return dd
    else:
        for t in tris:
            if e in tris[t]:
                TT = tris[t]
        ee = [x for x in TT not in T]
        newd = SearchWidth(C, TT, ee[0], d)
    return SearchWidth(C, TT, ee[1], newd)

def shareapoint(e1, e2):
	#input: two edges
	#output: true if true
	if e1[0]  in e2 or e1[1] in e2:
		return True
	return False

def  writeLPfile(outfile, subtrips, subwidths, sublengths):  
	#input: triplet, poly dict
    #output:  LP text file
	ff = open(outfile, 'w')
	ff.write('MAX \nOBJECTIVE:\nv\n\nSubject to:\n')   
	for j in range(0, len(subtrips)):
		if subwidths[j] != 0:
			writeline = 'VConst_' + str(j) + ':   v + ' + str(500000 - subwidths[j]) + 'x' + str(subtrips[j][0]) + '_' + str(subtrips[j][1]) + '_' + str(subtrips[j][2]) + ' <= 500000\n'
			ff.write(writeline)
	writeline = 'XX'         
	for e in  subtrips:
		if writeline == 'XX' and e[0] == 's':
			writeline = "Start_flow:   x" + str(e[0]) + '_'+str(e[1]) + '_' + str(e[2])
		elif e[0] == 's':
			writeline = writeline + " + x" + str(e[0]) + '_' + str(e[1]) + '_' + str(e[2])
	writeline = writeline + " = 1\n"
	if 'XX' not in writeline:
		ff.write(writeline)
	else:
		return "ERROR: NO START FLOW"      
	writeline = 'XX'    
	for e in subtrips:                
		if writeline == 'XX' and e[2] == 'e':
			writeline = "End_flow:   x" + str(e[0]) + '_ '+ str(e[1]) + '_' + str(e[2])
		elif e[2] == 'e':
			writeline = writeline + " + x" + str(e[0]) + '_' + str(e[1]) + '_' + str(e[2])
	writeline = writeline + " = 1 \n"
	if 'XX' not in writeline:
		ff.write(writeline)
	else:
		print("end tris are", endtris)
		return "ERROR: NO ENDFLOW"
	adjli = []  # get list of adj pairs
	for s in subtrips:
		if [s[0], s[1]] not in adjli:
			adjli.append([s[0], s[1]])
		if [s[1], s[2]] not in adjli:
			adjli.append([s[1], s[2]])
	for a in adjli:  #flow constraint
		writeline = 'XX'
		isitneg = False
		for k in subtrips:
			if a[0] == k[0] and a[1] == k[1] and a[0] != 's' and a[1] != 'e':
				if writeline == 'XX':
					writeline = 'Flow_Const_' + str(a[0]) + "_" + str(a[1]) + ':     x' + str(k[0]) + '_' + str(k[1]) + '_' + str(k[2])
				else:
					writeline = writeline + ' + x' + str(k[0]) + '_' + str(k[1]) + '_' + str(k[2])
		for k in subtrips:
			if a[0] == k[1] and a[1] == k[2] and a[0] != 's' and a[1] != 'e':
				if writeline == 'XX':
					writeline = 'Flow_Const_' + str(a[0]) + "_" + str(a[1]) + ':     x' + str(k[0]) + '_' + str(k[1]) + '_' + str(k[2])
					isitneg = True
				elif isitneg:
					writeline = writeline + ' + x' + str(k[0]) + '_' + str(k[1]) + '_' + str(k[2])
				elif not isitneg: 
					writeline = writeline + ' - x' + str(k[0]) + '_' + str(k[1]) + '_' + str(k[2])
		if writeline != 'XX':
			writeline = writeline + ' = 0\n'
			ff.write(writeline)
    
	writeline = "Length_Account:   L"   #length accounting constraint
	mycount = 0   #got to here
	for j in range(0, len(subtrips)):
		if subtrips[j][0] != subtrips[j][2]:
			mycount = mycount+1
			writeline = writeline+"-"+str(sublengths[j])+"x"+str(subtrips[j][0])+'_'+str(subtrips[j][1])+'_'+str(subtrips[j][2])
			if mycount >= 5:
				writeline = writeline+"\n"
				ff.write(writeline)
				writeline=""
				mycount=0
	writeline=writeline+"=0\n"
	ff.write(writeline)
    
	ff.write('Vnonneg:   v>=0\n\nBinary\n')         #z>=0
	writeline=''
	tempind=0
	for j in range(0, len(subtrips)):                     #binary x's
		writeline=writeline+"   x"+str(subtrips[j][0])+'_'+str(subtrips[j][1])+"_"+str(subtrips[j][2])
		tempind=tempind+1
		if tempind>6:
			ff.write(writeline)
			writeline='\n'    
			tempind=0         
	ff.write(writeline)
	writeline=''                                   
	ff.write('\nEnd') 
	ff.close()
	return 0
	
