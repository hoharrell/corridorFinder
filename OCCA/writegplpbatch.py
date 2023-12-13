# This code takes a csv file created by rlandscape dirsgs (12/15/15 version) 
#and creates a dictionary of polygons and edges

print "Starting code..."
# import csv
# import matplotlib.pyplot as plt
# from shapely.geometry import * 
# from polycode import *
# import gplp_foos
import os.path
import time
import sys
from compexpdata import *

batchfile = "C:/rstjohn/Comp_Exps/gplpbatch.txt"


fw = open(batchfile, 'w')

fw.write("set logfile C:/rstjohn/Comp_Exps/gplplog.log\n")
fw.write("set mip tolerances mipgap 0\n\n\n")

for hhh in dd['num_units']:
	for iii in dd['area_var']:
		for ggg in dd['deg_adj']:
			for jjj in ['1', '2', '3', '4', '5']: 
				mystr = "n"+hhh + "_deg" + ggg + "_area" + iii + "_" + jjj
				if mystr == "n600_deg55_area140_5":
					continue
				print mystr
				# fs = open('C:/rstjohn/Comp_Exps/gplpformsummary.txt')
				# isbad = False
				# for line in fs:
					# if mystr in line and "Bad" in line:
						# isbad = True
						# break
				# if isbad:
					# continue
				lpfile = "C:/rstjohn/Comp_Exps/Corr_LPs/" + mystr + "_corrlp.lp"
				solfile = "C:/rstjohn/Comp_Exps/Corr_LPs/" + mystr + "_corrsol.sol"
				# mypath = "C:/rstjohn/Comp_Exps/"+mystr+"/"
				# myfolder = "C:/rstjohn/Comp_Exps/" + mystr + "/gplps/"
				# edgefile = "C:/rstjohn/Comp_Exps/landscapes/" + 'land' + "_" + mystr + '_land.csv'
				# edgesdict, clusters, su, eu, triplets = getdata(edgefile)
				# print "got data"
				# for t in triplets:
					# if triplets.index(t) % 5000 == 0 and triplets.index(t) != 0:
						# print "On triplet "+str(t)+", which is number "+ str(triplets.index(t))	 + " out of " + str(len(triplets))	
					# for g1 in [0,1,2,3]:
						# for g2 in [0,1,2,3]:
							# mystr2 = str(t[0]) + "_" + str(t[1]) + "_" + str(t[2]) + "_" + str(g1) + "_" + str(g2)
							# lpfile = myfolder + 'gplp' + mystr2 + ".cpx"
							# solfile = myfolder + 'gplp' + mystr2 + "_sol.sol"
							# if os.path.exists(lpfile):
				writeline = "read "+ lpfile + " lp\n"
				fw.write(writeline)
				fw.write("Mipopt\n")
				writeline = "write "+ solfile + "\n\n\n"
				fw.write(writeline)
				# lpfile = "C:/rstjohn/Comp_Exps/Corr_LPs/" + hhh + "_" + iii + "_" + jjj + "_corrlp.lp"
				# solfile = "C:/rstjohn/Comp_Exps/Corr_LPs/" + hhh + "_" + iii + "_" + jjj + "_corrsol.sol"
							
		
fw.close()
sys.exit()
		

# batchfile = "C:/rstjohn/Comp_Exps/corrlpbatch.txt"
# fw = open(batchfile, 'w')
# fw.write("set logfile C:/rstjohn/Comp_Exps/corrlplog.log\n")
# fw.write("set mip tolerances mipgap 0\n\n\n")
logfile = "C:/rstjohn/Comp_Exps/corrlplog.log"
summaryfile = "C:/rstjohn/Comp_Exps/corrlpsolsummary.txt"
ff = open(logfile)
fw = open(summaryfile, 'w')
inone = False
expname = ""
objvalue = ""
soltime = ""	
for line in ff:
	if "Problem 'C:/rstjohn/Comp_Exps/Corr_LPs" in line:
		bb=line.split ("Corr_LPs/")
		cc = bb[1].split("_corrlp")
		expname = cc[0]
		inone = True
	if inone == True:
		if "MIP - Integer optimal solution:  Objective =" in line:
			bb= line. split("tive =")
			objvalue = bb[1]
		if "Solution time = " in line:
			bb=line.split("ime = ")
			aa= bb[1].split(".  Iterations")
			soltime = aa[0]
		if objvalue != "" and soltime != "":
			writeline = expname + ", " + objvalue[:-1] + ", " + soltime + "\n"
			fw.write(writeline)
			inone = False
			objvalue = ""
			soltime = ""
ff.close()		
fw.close()

print "End of Code"
