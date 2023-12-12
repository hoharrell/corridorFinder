####Cluster Finding Program ####
#summary
#inputs:    csize, polygon ids, areas, and adjacencies .txt files
#outputs:   .txt file of all clusters less than csize

###################### functions ##########################

import polycode
import sys
from multiprocessing import Pool

areafile = "C:/rstjohn/SLU_Exp/parcel_areas.txt"
clfile = "C:/rstjohn/SLU_Exp/polygons_2ha.txt"
clvertfile = "C:/rstjohn/SLU_Exp/polygon_2ha_verts.txt"
clusteridseed = 10000
csize= 20000

def getareaclusters(p):
	#input: id
	#append new clusters to clusters
	global clusters
	if areas[p] < csize:
			newclusts = nextclusters([p])
			if newclusts != []:
				clusters = clusters + newclusts
				for i in newclusts:
					newc2 = nextclusters(i)
					if newc2 != []:
						clusters = clusters + newc2
						for j in newc2:
							newc3 = nextclusters(j)
							if newc3 != []:
								clusters = clusters + newc3
								for k in newc3:
									newc4 = nextclusters(k)
									if newc4 != []:
										clusters = clusters + newc4
										for l in newc4:
											newc5 = nextclusters(l)
											if newc5 != []:
												clusters = clusters + newc5
												for m in newc5:
													newc6 = nextclusters(m)
													if newc6 != []:
														clusters = clusters + newc6
														for n in newc6:
															newc7 = nextclusters(n)
															if newc7 != []:
																clusters = clusters + newc7
																print "Need new level!"	
	return 0
	
	
def getclustverts(clust):
	#input: cluster id
	#output: list of vertices
	d = {}
	for p in clust:
		d = polycode.mergepolys(d, parcels[p])
	myp = polycode.getpolygon(d)
	list1 = list(myp.exterior.coords)
	for i in myp.interiors:
		list1 += i.coords
	return list1
			
def getholeclusters(p):
	global clusters
	adjli = polycode.getadjs(p)
	holeli = [p]
	for h in adjli:
		inhole = True
		for e in parcels[h]:
			if e not in parcels[p]:
				inhole = False
				break
		if inhole:
			holeli.append(h)
	if holeli !=[]:
		clusters.append(holeli)
	return 0
	
def getnewadjs(tempcluster):
	#fxn that returns all units adjacent to cluster
	newadjs=[]
	for i in tempcluster:
		templi = polycode.getadjs(i)
		for j in templi:
			if j not in newadjs and j not in tempcluster:
				newadjs.append(j)
	return newadjs
    
def nextclusters(cluster):
	#input: cluster list
	#output lists of next level of cluster
	newclusts = []
	myadjs=getnewadjs(cluster)
	clarea = 0.0
	for c in cluster:
		clarea = clarea + areas[c]
	if myadjs != []:
		for k in myadjs:
			if clarea + areas[k] < csize:
				tempcluster = cluster + [k]
				newclusts.append(tempcluster)
	return newclusts

	
def foo1(p):
	print "getting clusters for parcel "+str(p) + " out of "+str(len(parcels))
	getareaclusters(p)
	if p in myli:
		getholeclusters(p)
	print len(clusters)
	return 0
###################### define and read in data ##########################


parcels = polycode.polygons
su = polycode.startunit
eu = polycode.endunit
del parcels[su]
del parcels[eu]


#get areas
file=open(areafile)
areas = {}
for line in file:
    strarr=line.split()
    temp=int(strarr[0])
    if temp in parcels:
        areas[temp] = float(strarr[1])
file.close()

#get clusters
clusters=[]
clustareas ={}
myli = polycode.hasholeli
count = 0
i = parcels.keys()
# if __name__ == "__main__":	
	# poo = Pool(7)
	# poo.map(foo1, i) 
for x in i:
	foo1(x)

#get rid of repeats
print("cleaning up clusters")
finalclusters=[]
tempclust=[]
for i in clusters:
	if len(i) < 2:
		continue
	i.sort()
	tempclust=[]
	for j in i:
		if j not in tempclust:
			tempclust.append(j)
	if tempclust not in finalclusters:
		finalclusters.append(tempclust)

print "There are " + str(len(finalclusters)) + " total clusters.  Writing file..."

#write cluster file
print "writing cluster files"

#write cluster and cluster verts files
fr=open(polycode.vertfile, 'r')
fw = open(clvertfile, 'w')
for line in fr:
	fw.write(line)
fr.close()

clusters = {}
ff = open(clfile, 'w')
for c in finalclusters:
	print finalclusters.index(c)
	print c
	id = finalclusters.index(c) + clusteridseed
	writeline=str(id)
	for p in c:
		writeline=writeline+"\t"+str(p)
	writeline=writeline+"\n"
	ff.write(writeline)
	myverts = getclustverts(c)
	for v in myverts:
		writeline = "\n" + str(id) + "\t" + str(v[0]) + "\t" + str(v[1])
		fw.write(writeline)
ff.close()
fw.close()
print "cluster files complete."


print "End of Code"