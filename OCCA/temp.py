# This code takes a csv file created by rlandscape dirsgs (12/15/15 version) 
#and creates a dictionary of polygons and edges

print "Starting code..."
import csv
import matplotlib.pyplot as plt
from shapely.geometry import * 
from polycode import *
import gplp_foos
import os.path
import time
import sys

batchfile = "C:/rstjohn/Comp_Exps/gplpbatch.txt"
fw = open(batchfile, 'w')
fw.write("set logfile C:/rstjohn/Comp_Exps/gplplog.log\n")
fw.write("set mip tolerances mipgap 0\n\n\n")
xx = 0
for clustlevel in [1,2,3]:
	for numlevel in [1,2,3]:
		for arealevel in [1,2,3]:
			for adjlevel in [1,2,3]:
				if arealevel == 1 and adjlevel == 3:
					continue
				landname = 'num' + str(numlevel) + 'area' + str(arealevel) + 'adj' + str(adjlevel)
				expname = landname + 'clust' + str(clustlevel)
				print expname
				mypath = "C:/rstjohn/Comp_Exps/rland_landscapes/" + expname + "_gplps/"
				edgefile = 'C:/rstjohn/Comp_Exps/rland_landscapes/' + landname + '_land.csv'
				
				mytable = []
				f = open(edgefile, 'rb')
				landscape = csv.reader(f)
				for row in landscape:
					if 'y1' not in row:
						mytable.append(row)
				f.close()	
					
				#get polyids:
				mypolys = []
				for row in mytable:
					p1 = int(row[5])
					p2 = int(row[6])
					if p1 not in mypolys:
						mypolys.append(p1)
					if p2 not in mypolys:
						mypolys.append(p2)
				# print mypolys
					
				#get hole polys	
				holepolys = []
				for p in mypolys:
					ishole  = True
					for row in mytable:
						if p in (int(row[5]), int(row[6])) and row[10] == '0':
							ishole = False
							break
					if ishole == True:
						holepolys.append(p)
				# print holepolys

				#get merged polys
				merged = {}  # key is orig poly, entry is new poly id
				templi = []
				for p in mypolys:
					if p not in holepolys:
						for row in mytable:
							if p in (int(row[5]), int(row[6])) and row[9] == '1':
								li = [int(row[5]), int(row[6])]
								newmerge = True
								for i in templi:
									if li[0] in i or li[1] in i:
										newmerge = False
										if li[0] not in i:
											i.append(li[0])
										if li[1] not in i:
											i.append(li[1])
										i.sort()
								if newmerge == True:
									li.sort()
									templi.append(li)
				fixedyet = False
				while not fixedyet:
					fixedyet = True
					for i in templi:
						newli = i
						for j in templi:
							if i != j and [x for x in i if x in j] != []:
								for p in j:
									if p not in i:
										newli.append(p)
										newli.sort()
								templi.remove(j)
								break
						if newli != i:
							fixedyet = False
							i = newli
							break
				for i in templi:
					for j in i:
						if j != i[0]:
							merged[j] = i[0]
							
				#get adjs
				adjdict = {}
				for row in mytable:
					if row[9] == '0' and row[10] == '0' and row[11] == '0':
						p1 = int(row[5])
						p2 = int(row[6])
						if p1 in merged:
							p1 = merged[p1]
						if p2 in merged:
							p2 = merged[p2]
						if p1 not in adjdict:
							adjdict[p1] = []
						if p2 not in adjdict:
							adjdict[p2] = []
						if p2 not in adjdict[p1]:
							adjdict[p1].append(p2)
						if p1 not in adjdict[p2]:
							adjdict[p2].append(p1)
				for p in adjdict:
					if p in adjdict[p]:
						adjdict[p].remove(p)
						# print "removed one"
							
				#get edges
				edgesdict = {}
				for row in mytable:
					if row[9] == '0' and row[11] == '0':
						edge= [[float(row[1]), float(row[2])],[float(row[3]), float(row[4])]]
						edge.sort()
						for z in [5,6]:
							p1 = int(row[z])
							if p1 not in holepolys:
								if p1 not in merged:
									if p1 not in edgesdict:
										edgesdict[p1] = {}
									edgesdict[p1][str(edge)]= edge
								if p1 in merged:
									temppoly = merged[p1]
									if temppoly not in edgesdict:
										edgesdict[temppoly] = {}
									edgesdict[temppoly][str(edge)]= edge


									
				#fix border edges
				for p in edgesdict:
					b = []
					for i in edgesdict[p]:
						e = edgesdict[p][i]
						if 0 in e[0] or 0 in e[1] or 1 in e[0] or 1 in e[1]:
							b.append(e)
					if len(b) == 1 and len(edgesdict[p]) == 1:
						ee = b[0]
						if ee[0][0] ==  0 or ee[1][0] == 0:
							newx = 0
						else:
							newx = 1.0
						if ee[0][1] ==  0 or ee[1][1] == 0:
							newy = 0
						else:
							newy = 1.0
						newpt = [newx, newy]
						newedge1 = [ee[0], newpt]
						newedge2 = [ee[1], newpt]
						newedge1.sort()
						newedge2.sort()
						edgesdict[p][str(newedge1)] = newedge1
						edgesdict[p][str(newedge2)] = newedge2
					elif len(b) == 2:
						if 0 in b[0][0] or 1 in b[0][0]:
							bp1 = b[0][0]
						else:
							bp1 = b[0][1]
						if 0 in b[1][0] or 1 in b[1][0]:
							bp2 = b[1][0]
						else:
							bp2 = b[1][1]	
						if bp1[0] == bp2[0] or bp1[1] == bp2[1]: #no corner
							newedge = [bp1, bp2]
							newedge.sort()
							edgesdict[p][str(newedge)] = newedge
						else:
							if bp1[0] ==  0 or bp2[0] == 0:
								newx = 0
							else:
								newx = 1.0
							if bp1[1] ==  0 or bp2[1] == 0:
								newy = 0
							else:
								newy = 1.0
							newpt = [newx, newy]
							newedge1 = [bp1, newpt]
							newedge2 = [bp2, newpt]
							newedge1.sort()
							newedge2.sort()
							edgesdict[p][str(newedge1)] = newedge1
							edgesdict[p][str(newedge2)] = newedge2
					elif len(b) in [3,4]:
						# print p
						xborder = []
						yborder = []
						for ee in b:
							if ee[0][0] in [0,1]:
								xborder.append(ee[0])
							if ee[1][0] in [0,1]:
								xborder.append(ee[1])
							if ee[0][1] in [0,1]:
								yborder.append(ee[0])
							if ee[1][1] in [0,1]:
								yborder.append(ee[1])
						xborder.sort()
						yborder.sort()
						# print xborder
						# print yborder
						if len(xborder) not in [0,2,4] and len(yborder) not in [0,2,4]:
							print "ERROR.  Found "+str(len(b))+ " edges adjacent to border in poly "+str(p)
							plotpoly(edgesdict[p], 'k')
							plt.show()
						elif len(xborder) == 4:
							newedge1 = [xborder[0], xborder[1]]
							newedge2 = [xborder[2], xborder[3]]
						elif len(yborder) == 4:
							newedge1 = [yborder[0], yborder[1]]
							newedge2 = [yborder[2], yborder[3]]
						else:
							newedge1 = [xborder[0], xborder[1]]
							newedge2 = [yborder[0], yborder[1]]
						edgesdict[p][str(newedge1)] = newedge1
						edgesdict[p][str(newedge2)] = newedge2
					elif len(b) != 0:
						print "ERROR.  Found "+str(len(b))+ " edges adjacent to border in poly "+str(p)
						print edgesdict[p]
						plotpoly(edgesdict[p], 'k')
						plt.show()

						
				#fix dangles
				for p in edgesdict:
					finished = False
					while not finished:
						finished = True
						for e in edgesdict[p]:
							checkpt1 = False
							checkpt2 = False
							for ee in edgesdict[p]:
								if ee != e and edgesdict[p][e][0] in  edgesdict[p][ee]:
									checkpt1 = True
								if ee != e and edgesdict[p][e][1] in  edgesdict[p][ee]:
									checkpt2 = True
							if not checkpt1 or not checkpt2:
								del edgesdict[p][e]
								finished = False
								break


				#get su and eu
				su = 99999
				eu = 99999
				sudist = 5
				eudist = 5
				for p in edgesdict: 
					mypoly = getpolygon(edgesdict[p])
					if Point(0,0).distance(mypoly) < sudist and p < 5000:
						su = p
						sudist = Point(0,0).distance(mypoly) 
					if Point(1,1).distance(mypoly) < eudist and p < 5000:
						eu = p
						eudist = Point(1,1).distance(mypoly)
								
				areasum = 0.0
				for p in edgesdict:
					mypoly = getpolygon(edgesdict[p])
					areasum = areasum + mypoly.area	
				avgarea = areasum / len(edgesdict)


				def clustcheck(curr, clusters):
					for c in clusters:
						if clusters[c] == curr:
							return True
					return False

				#get clusters
				clusters = {}
				clustind = 5000
				if clustlevel == 1:
					numclusters = 0
				elif clustlevel == 2:
					maxclustsize = 1 * avgarea
				elif clustlevel == 3:
					maxclustsize = 1.5 * avgarea
				if clustlevel > 1:
					for p in edgesdict:
						parea = getpolygon(edgesdict[p]).area
						if parea < maxclustsize and p in adjdict and p not in [su, eu]:
							for a1 in adjdict[p]:
								a1area = getpolygon(edgesdict[a1]).area
								if a1area + parea < maxclustsize and a1 not in [su, eu]:
									currcluster = [p, a1]
									currcluster.sort()
									if not clustcheck(currcluster, clusters):
										clusters[clustind]=currcluster
										clustind = clustind +1
									for a2 in adjdict[a1]:
										a2area = getpolygon(edgesdict[a2]).area
										if a2 not in currcluster and parea + a1area + a2area < maxclustsize and a2 not in [su, eu]:
											currcluster = [p, a1, a2]
											currcluster.sort()
											if clustcheck(currcluster, clusters):
												clusters[clustind]=currcluster
												clustind = clustind +1
											for a3 in adjdict[a2]:
												a3area = getpolygon(edgesdict[a3]).area
												if a3 not in currcluster and parea + a1area + a2area +a3area < maxclustsize and a3 not in [su, eu]:
													currcluster = [p, a1, a2, a3]
													currcluster.sort()
													if clustcheck(currcluster, clusters):
														clusters[clustind]=currcluster
														clustind = clustind + 1
													for a4 in adjdict[a3]:
														a4area = getpolygon(edgesdict[a4]).area
														if a4 not in currcluster and parea + a1area + a2area +a3area + a4area < maxclustsize and a3 not in [su, eu]:
															currcluster = [p, a1, a2, a3, a4]
															currcluster.sort()
															if clustcheck(currcluster, clusters):
																clusters[clustind]=currcluster
																clustind = clustind + 1
															for a5 in adjdict[a4]:
																a5area = getpolygon(edgesdict[a5]).area
																if a5 not in currcluster and parea + a1area + a2area +a3area + a4area + a5area < maxclustsize and a3 not in [su, eu]:
																	currcluster = [p, a1, a2, a3, a4, a5]
																	currcluster.sort()
																	if clustcheck(currcluster, clusters):
																		clusters[clustind]=currcluster
																		clustind = clustind + 1
																	for a6 in adjdict[a5]:
																		a6area = getpolygon(edgesdict[a6]).area
																		if a6 not in currcluster and parea + a1area + a2area +a3area + a4area + a5area + a6area < maxclustsize and a3 not in [su, eu]:
																			currcluster = [p, a1, a2, a3, a4, a5, a6]
																			currcluster.sort()
																			if clustcheck(currcluster, clusters):
																				clusters[clustind]=currcluster
																				clustind = clustind + 1
																				print "need another cluster level!!!"
																				print len(clusters)
																				sys.exit()
					numclusters = len(clusters)
					for c in clusters:    #edges
						edgesdict[c] = {}
						for p in clusters[c]:
							for ee in edgesdict[p]:
								goodedge = True
								for p2 in clusters[c]:	
									if p != p2 and ee in edgesdict[p2]:
										goodedge = False
										break
								if goodedge:
									edgesdict[c][ee] = edgesdict[p][ee]
					for p in edgesdict:  	#update adjs
						for p2 in edgesdict:
							if p < p2 and p in clusters or p2 in clusters:
								if [x for x in edgesdict[p] if x in edgesdict[p2]] !=[]:
									if p in clusters:
										li1 = clusters[p]
									else:
										li1 = [p]
									if p2 in clusters:
										li2 = clusters[p2]
									else:
										li2 = [p2]
									if [x for x in li1 if x in li2] == []:
										if p not in adjdict:
											adjdict[p] =[]
										if p2 not in adjdict:
											adjdict[p2] =[]
										if p2 not in adjdict[p]:
											adjdict[p].append(p2)
										if p not in adjdict[p2]:
											adjdict[p2].append(p)
			
				#create triplets
				triplets = []
				for p in adjdict:
					for a in adjdict[p]:
						for b in adjdict[p]:
							if a !=b and (a == su or b == eu or a < b):
								if clustlevel == 1 or (a not in clusters and b not in clusters):
									triplets.append([a,p,b])
								else:
									if a in clusters:
										apolys = clusters[a] 
									else:
										apolys = [a]
									if b in clusters:
										bpolys = clusters[b]
									else:
										bpolys = [b]
									if [x for x in apolys if x in bpolys] == []:
										triplets.append([a,p,b])

								
				print "writing file"
				# xx = 0
				wlfile = mypath + expname + "gpwidthlengths.txt"
				fw = open(wlfile, 'w')
				for t in triplets:
					tstr = str(t[0]) + "_" + str(t[1]) + "_" + str(t[2])
					for g1 in range(0, 4):
						for g2 in range(0, 4):
							solfile = mypath + "gplp" + tstr + "_" + str(g1) + "_" +str(g2) + "_sol1.sol"
							if os.path.exists(solfile):
								fs = open(solfile)
								myw = 0
								myl = 0
								for line in fs:
									if 'variable name="v" ' in line:
										temparr = line.split('"')
										myw = temparr[5]
									if 'variable name="L" ' in line:
										temparr = line.split('"')
										myl = temparr[5]
								fs.close()
								writeline = tstr + "," + myw + "," + myl
								fw.write(writeline)
								xx = xx + 1
								writeline = "read "+ lpfile + " lp\n"
								fw.write(writeline)
								fw.write("Mipopt\n")
								solfile = mypath + "gplp" + tstr + "_" + str(g1) + "_" +str(g2) + "_sol.sol"
								writeline = "write "+ solfile + "\n\n\n"
								fw.write(writeline)
								if xx % 1000 == 0:
									print str(xx) + "gp lps for exp " + expname + " batched thus far."

				fw.close()

print "End of Code"
