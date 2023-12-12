# This code takes a csv file created by rlandscape dirsgs (12/15/15 version) 
#and creates a dictionary of polygons and edges

print "Starting code..."
import csv
import matplotlib.pyplot as plt
from shapely.geometry import * 
from polycode import *
from compexpdata import *
import gplp_foos
import os.path
import time 
import sys
summaryfile = 'C:/rstjohn/Comp_Exps/gplpformsummary.txt'

for hhh in dd['num_units']:
	for iii in dd['area_var']:
		for ggg in dd['deg_adj']:
			for jjj in ['1', '2', '3', '4', '5']: 
				mystr = "n"+hhh + "_deg" + ggg + "_area" + iii + "_" + jjj
				gotit = False
				fs = open(summaryfile)
				for line in fs:
					if mystr in line and "Bad" in line:
						gotit = True
						break
				fs.close()
				if gotit == False:
					continue
				print mystr
				mypath = "C:/rstjohn/Comp_Exps/" + mystr + "/"
				if not os.path.exists(mypath):
					os.makedirs(mypath)
				myfolder = mypath + "gplps/"
				if not os.path.exists(myfolder):
					os.makedirs(myfolder)
				edgefile = "C:/rstjohn/Comp_Exps/landscapes/" + 'land' + "_" + mystr + '_land.csv'
				start_time = time.time()
				try:
					edgesdict, clusters, su, eu, triplets = getdata(edgefile)
					print "got data"
					if edgesdict == 5:
						fs = open(summaryfile, 'a')
						fs.write(mystr + ", Bad landscape\n")
						fs.close()
						continue
				except:
					fs = open(summaryfile, 'a')
					fs.write(mystr + ", Bad landscape\n")
					fs.close()
					continue
				print "writing GPLPS"
				numgps = 0
				isbad = False
				for t in triplets:
					if triplets.index(t) % 1000 == 0:
						print "On triplet "+str(t)+", which is number "+ str(triplets.index(t))	 + " out of " + str(len(triplets))
					kk = gplp_foos.writeGPLPs(t, myfolder, edgesdict)
					if kk == 999:
						print "ERROR triplet "+str(t)+", which is number "+ str(triplets.index(t)) + " out of " + str(len(triplets))
						fs = open(summaryfile, 'a')
						fs.write(mystr + ", Bad landscape\n")
						isbad = True
						fs.close()
						break
						# plotpoly(edgesdict[t[0]], 'r')
						# plotpoly(edgesdict[t[1]], 'g')
						# plotpoly(edgesdict[t[2]], 'b')
						# plt.axis([-0.1, 1.1, -0.1, 1.1])
						# plt.show()
						# sys.exit()
					elif kk < 100:
						numgps = numgps + kk
				end_time = time.time()
				print "Finished GPLPs."

				#write summary file
				if not isbad:
					f = open(summaryfile,"r")
					mylines = f.readlines()
					f.close()
					towrite = mystr + ", " + str(len(clusters)) + ', ' + str(numgps) + ', ' + str(end_time-start_time) + '\n'
					fs = open(summaryfile, 'w')
					for line in mylines:
						if mystr in line:
							fs.write(towrite)
						else:
							fs.write(line)
							
					fs.close()

print "End of Code"


			# tt = [5177, 5235, 5200]
			# # for p in tt:
				# # print "poly is "+str(p) + " and its adjs are "+str(adjdict[p])
			# # print tt
			# plotpoly(edgesdict[tt[0]], 'r')
			# plotpoly(edgesdict[tt[1]], 'g')
			# plotpoly(edgesdict[tt[2]], 'b')
			# plt.axis([-0.1, 1.1, -0.1, 1.1])
			# plt.show()
			# print gplp_foos.writeGPLPs(tt, mypath, edgesdict)
			# sys.exit()
			
