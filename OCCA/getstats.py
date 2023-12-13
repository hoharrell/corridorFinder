import statistics
import sys

datafile = "C:/rstjohn/Comp_Exps/CompExpResults.txt"
statfile = "C:/rstjohn/Comp_Exps/CompExpStats.txt"
dd = {}
kk = []
ff = open(datafile)
for line in ff:
	aa = line.split(",")
	if "ExpID"==aa[0]:
		for i in aa:
			kk.append(i)
		temp = kk[-1][:-1]
		kk[-1] = temp
	else:
		dd[aa[0]] = {}
		for x in range(1, len(kk)):
			dd[aa[0]][kk[x]] = float(aa[x])
# print dd
ff.close()

factors = ['clustlevel', 'numlevel', 'adjlevel', 'arealevel']
vars = [x for x in kk if x not in factors]
vars = vars[1:]

fw = open(statfile, 'w')
for f in factors:
	fw.write("," + f +",1,2,3\n")
	for v in vars:
		line1 =  v + ",mean"
		line2  = v + ",stdevs"
		line3 = v + ",CIlow"
		line4 = v + ",CIhigh"
		for i in [1.0,2.0,3.0]:
			tempdata = []
			for d in dd:
				if f not in dd[d]:
					print "Error for "+ d
					print dd[d]
				if dd[d][f] == i:
					tempdata.append(dd[d][v])
			m = statistics.mean(tempdata)
			line1 = line1 + "," + str(m)
			s = statistics.stdev(tempdata)
			line2 = line2 + "," + str(s)
			line3 = line3 + ',' + str(m-2*s)
			line4 = line4 + ',' + str(m+2*s)
			
		fw.write(line1 + '\n')
		fw.write(line2 + '\n')
		fw.write(line3 + '\n')
		fw.write(line4 + '\n\n')
	fw.write('\n\n')
fw.close()	
	
			
		
			
		
	
		
			