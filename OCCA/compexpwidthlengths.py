# This code takes a csv file created by rlandscape dirsgs (12/15/15 version) 
#and creates a dictionary of polygons and edges

print "Starting code..."
# import csv
# import matplotlib.pyplot as plt
# from shapely.geometry import * 
# from polycode import *
# import gplp_foos
from compexpdata import *
import os.path
# import time
import sys

# batchfile = "C:/rstjohn/Comp_Exps/gplpbatch.txt"
# fw = open(batchfile)
# fw.write("set logfile C:/rstjohn/Comp_Exps/gplplog.log\n")
# fw.write("set mip tolerances mipgap 0\n\n\n")

print "in here"
for hhh in dd['num_units']:
	for iii in dd['area_var']:
		for ggg in dd['deg_adj']:
			for jjj in ['1', '2', '3', '4', '5']: 
				mystr = "n"+hhh + "_deg" + ggg + "_area" + iii + "_" + jjj
				if mystr == "n600_deg55_area140_5":
					continue
				print mystr
				# fb = open('C:/rstjohn/Comp_Exps/gplpformsummary.txt')
				# isbad = False
				# for line in fb:
					# if mystr in line and "Bad" in line:
						# isbad = True
						# break
				# if isbad:
					# continue
				# fb.close()
				myfolder = "C:/rstjohn/Comp_Exps/" + mystr + "/gplps/"
				edgefile = "C:/rstjohn/Comp_Exps/landscapes/" + 'land' + "_" + mystr + '_land.csv'
				edgesdict, clusters, su, eu, triplets = getdata(edgefile)
				wlfile = "C:/rstjohn/Comp_Exps/" + mystr + "/gpwidthlengths.txt"
				fw = open(wlfile, 'w')
				for t in triplets:
					if triplets.index(t) % 5000 == 0 and triplets.index(t) != 0:
						print "On triplet "+str(t)+", which is number "+ str(triplets.index(t))	 + " out of " + str(len(triplets))	
					for g1 in [0,1,2,3]:
						for g2 in [0,1,2,3]:
							mystr2 = str(t[0]) + "_" + str(t[1]) + "_" + str(t[2]) + "_" + str(g1) + "_" + str(g2)
							solfile = myfolder + 'gplp' + mystr2 + "_sol.sol"
							# print solfile
							if os.path.exists(solfile):
								# print "yup"
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
								writeline =  mystr2 + "," + myw + "," + myl +"\n"
								fw.write(writeline)
				
				fw.close()

print "End of Code"
