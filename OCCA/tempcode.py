myfile = "C:/rstjohn/SLU_Exp/Sim_11tps.txt"
newfile = "C:/rstjohn/SLU_Exp/Sim_11tps_new.txt"

ff = open(myfile)
fw = open(newfile, 'w')
rx = 0
myli = []
for line in ff:
	if "PERIOD" not in line:
		strarr = line.split(',')
		if int(strarr[3]) > rx:
			rx = int(strarr[3])
		if int(strarr[3]) < rx:
			myli.append(rx)
			rx = 0
ff.close()

x = 0.0
print myli
maxnum = 0
minnum = 100
for i in myli:
	x = x + i
	if i > maxnum:
		maxnum = i
	if i < minnum:
		minnum = i


	
print len(myli)
print maxnum
print minnum
print x/len(myli)
print "DONE"