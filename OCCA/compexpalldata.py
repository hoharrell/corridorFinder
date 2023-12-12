import os.path, time
import os
import sys
from compexpdata import * 
import datetime


def gettime(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

corrsolfile = "C:/rstjohn/Comp_Exps/corrlpsolsummary.txt"
corrformsummary = "C:/rstjohn/Comp_Exps/corrLPformulationsummary.txt"
gpsolvetimefile = "C:/rstjohn/Comp_Exps/gplpsolvetime.txt"
expdict = {}

# fz = open(gpsolvetimefile, 'w')

for hhh in dd['num_units']:
	for iii in dd['area_var']:
		for ggg in dd['deg_adj']:
			for jjj in ['1', '2', '3', '4', '5']: 
				expname = "n"+hhh + "_deg" + ggg + "_area" + iii + "_" + jjj
				if expname == "n600_deg55_area140_5" or expname =="n600_deg39_area98_5":
					continue
				expdict[expname] = {}
				expdict[expname]["num_units"] = hhh
				expdict[expname]["deg_adj"] = ggg
				expdict[expname]["area_var"] = iii
				# expdict[expname]['level'] = iii
				# gpfile = "C:/rstjohn/Comp_Exps/" + mystr + "/gpwidthlengths.txt"
				# myfolder = "C:/rstjohn/Comp_Exps/" + mystr + "/gplps/"
				# gpdict = getgpwidthlength(gpfile, 9000, 9000)
				# gps = gpdict.keys()
				# times = []
				# print mystr
				# for g in gps:
					# solfile = myfolder + 'gplp' + g + "_sol.sol"
					# if  os.path.exists(solfile):
						# (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(solfile)
						# tt = gettime(solfile)
						# times.append(tt)
				# times.sort()
				# soltime = times[-1] - times[0]
				# ww  = mystr + "," + str(soltime)+ "\n"
				# fz.write(ww)
			
						
# fz.close()
# # sys.exit()

# #corrsol summary
# print "getting corr sol summary!!!"
# corrlogfile = "C:/rstjohn/Comp_Exps/corrlplog.log"
# ff = open(corrlogfile)
# fw = open(corrsolfile, 'w')
# inone = False
# expname = ""
# objvalue = ""
# soltime = ""	
# for line in ff:
	# if "Problem 'C:/rstjohn/Comp_Exps/Corr_LPs" in line:
		# bb=line.split ("Corr_LPs/")
		# cc = bb[1].split("_corrlp")
		# expname = cc[0]
		# inone = True
	# if inone == True:
		# if "MIP - Integer optimal solution:  Objective =" in line:
			# bb= line. split("tive =")
			# objvalue = bb[1]
		# if "Solution time = " in line:
			# bb=line.split("ime = ")
			# aa= bb[1].split(".  Iterations")
			# soltime = aa[0]
		# if objvalue != "" and soltime != "":
			# writeline = expname + ", " + objvalue[:-1] + ", " + soltime + "\n"
			# fw.write(writeline)
			# inone = False
			# objvalue = ""
			# soltime = ""
# ff.close()		
# fw.close()
# sys.exit()


print "getting rest of data..."				
fa = open(corrsolfile)
for line in fa:
	aa = line.split(",")
	for i in aa:
		i.strip()
	# if aa[0] not in expdict:
		# print "Error with corrsolfile, exp "+aa[0]+" not in expdict"
		# sys.exit()
		# continue
	bb = aa[2].split(" s")
	if aa[0] in expdict:
		expdict[aa[0]]["CorrLPObjValue"] = float(aa[1])		
		expdict[aa[0]]["CorrLPSolveTime"] = float(bb[0])
	# print expdict[aa[0]]["CorrLPSolveTime"]
fa.close()

fb = open(corrformsummary)
for line in fb:
	aa = line.split(",")
	for i in aa:
		i.strip()
	if aa[0] in expdict:
		expdict[aa[0]]["CorrLPFormTime"] = float(aa[1]	)	
		expdict[aa[0]]["NumGPs"] = int(aa[2])
fb.close()



fz = open(gpsolvetimefile)
for line in fz:
	aa = line.split(",")
	for i in aa:
		i.strip()
	if aa[0] in expdict:
		# print aa[0]
		bb = aa[1].split(":")
		secs = int(bb[0])*60*60 + int(bb[1]) * 60 + float(bb[2])
		expdict[aa[0]]["GPLPSolveTime"] = secs
fz.close()

gplpformsummary = "C:/rstjohn/Comp_Exps/gplpformsummary.txt"
fc = open(gplpformsummary)
for line in fc:
	aa = line.split(",")
	for i in aa:
		i.strip()
	# yy = aa[0].split("and")
	# xx = "exp"+yy[1]
	if aa[0] in expdict:
			expdict[aa[0]]["NumClusters"] = int(aa[1])
			expdict[aa[0]]["GPLPFormTime"] = float(aa[3])
fc.close()

for e in expdict:
	# print e
	xx = expdict[e]["GPLPFormTime"] + expdict[e]["GPLPSolveTime"] 
	if "CorrLPFormTime" in expdict[e] and "CorrLPSolveTime" in expdict[e]:
		xx = xx +  expdict[e]["CorrLPFormTime"] + expdict[e]["CorrLPSolveTime"]
		expdict[e]["TotalTime"] = xx
	else: 
		expdict[e]["TotalTime"] = "xx"
print "Writing File"
# for hhh in dd:
	# print hhh
writefile = "C:/rstjohn/Comp_Exps/results.txt"
# fw = open(writefile, 'w')
exps = expdict.keys()
exps.sort()
print len(expdict)
kk = expdict[exps[0]].keys()
# zz = [x for x in dd if x != hhh]
# kk = [x for x in kk if x not in d]
kk.sort()
print kk

fw = open( "C:/rstjohn/Comp_Exps/avgs.txt", 'w')

writeline = "n, deg, area, GPs, Time\n"
fw.write(writeline)
for hhh in dd['num_units']:
	for iii in dd['area_var']:
		for ggg in dd['deg_adj']:
			gps = 0
			time = 0
			nn = 0
			for jjj in ['1', '2', '3', '4', '5']: 
				e = "n"+hhh + "_deg" + ggg + "_area" + iii + "_" + jjj
				if e in expdict:
					gps = gps + expdict[e]["NumGPs"]
					if expdict[e]["TotalTime"]!= 'xx':
						time = time + expdict[e]["TotalTime"]
						nn = nn+ 1
			avggps = gps/nn
			avgtime = time /nn
			writeline = hhh + "," + ggg +"," +iii+ "," + str(avggps) + "," + str(avgtime)+ '\n'
			fw.write(writeline)

fw.close()
sys.exit()
			
writeline = "ExpID"
for i in kk:
	writeline = writeline + "," + i
# print writeline
# sys.exit()
fw.write(writeline + "\n")
for e in exps:
	writeline = e
	# print expdict[e]
	for i in kk:
		if type(expdict[e][i]) == float:
			expdict[e][i]= round(expdict[e][i], 7)
		writeline = writeline + "," + str(expdict[e][i])
	if 'xx' not in writeline:
		fw.write(writeline + "\n")
	# sys.exit()
fw.close()
		


print "End of Code"
# print "created: %s" % time.ctime(os.path.getctime(file))
