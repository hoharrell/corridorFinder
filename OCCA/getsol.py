

solfile = "C:/rstjohn/11tps_maxnpv_full_sol.sol"
writef = "C:/rstjohn/11tps_maxnpv_full_sol_summary.txt"

from getCCdata import *

tps = range(0, 11)
######################## FUNCTIONS ####################################

def groundlich(gp, t):
	midpol = gpdict[gp]['gp'][1]
	if midpol < eu:
		x = origidforpoly[midpol]
		if x in solrxs:
			rx = solrxs[x]
			return areadict[x] * harvdict[x][rx][t]['g'] 
			# print "x is single unit " + 
			# print "area is " + str(areadict[x]) + " and g lich is "+str(harvdict[x][rx][t]['g'])
			# return  harvdict[x][rx][t]['g'] *  areadict[x]
		else: 
			# print x
			# print "x not in solrxs"
			return 0	
	else:  #str(areadict[u]  * harvdict[u][rx][t]['g'] )
		ans = 0.0
		for u in clusters[midpol]:
			x = origidforpoly[u]
			if x in solrxs:
				rx = solrxs[x]
				ans = ans + areadict[x] * harvdict[x][rx][t]['g'] 
			# else:
				# print x
		# print "x is cluster"
		return ans 

def treelich(gp, t):
	midpol = gpdict[gp]['gp'][1]
	if midpol < eu:
		x = origidforpoly[midpol]
		if x in solrxs:
			rx = solrxs[x]
			return harvdict[x][rx][t]['t'] * areadict[x]
		else: 
			return 0
	else:
		ans = 0.0
		for u in clusters[midpol]:
			x = origidforpoly[u]
			if x in solrxs:
				rx = solrxs[x]
				ans = ans +  harvdict[x][rx][t]['t'] *  areadict[x]
		return ans 
	
def resistance(gp, t):
	midpol = gpdict[gp]['gp'][1]
	if midpol < eu:
		x = origidforpoly[midpol]
		if x in solrxs:
			rx = solrxs[x]
			if harvdict[x][rx][t]['r'] == 1:
				print "ERROR: resistance coeff 1!"
				print gp, t
				print "Stand ID: " + str(x) + ";  rx: " + str(rx) + ";   t: " + str(t)
			return harvdict[x][rx][t]['r']  * gpdict[gp]['l']
		else: 
			return 0
	else:
		rcoef = 0.0
		for u in clusters[midpol]:
			x = origidforpoly[u]
			if x in solrxs:
				rx = solrxs[x]
				if harvdict[x][rx][t]['r'] == 1:
					print "ERROR: resistance coeff 1!"
					print gp, t
					print "Stand ID: "+str(x)+";  rx: "+str(rx) + ";   t: "+str(t)
				rcoef = rcoef + harvdict[x][rx][t]['r'] * areadict[x] / polyarea[midpol] 
		return rcoef * gpdict[gp]['l']
	
############################ BODY OF CODE #################################

print "getting sol"
solrxs = {}
corridors = {}
polycorrli = {}
mygs = {}
mygunits = {}
for t in tps:
	corridors[t] = []
	polycorrli[t] = []
	mygs[t] = 0.0
	mygunits[t] =[]
solf = open(solfile)
for line in solf:
	# if "objectiveValue=" in line:
		# print line
		# break   
	# if "ixed" in line:
		# print "YUP FIXED"
	# if "tatic" in line:
		# print "YUP STATIC"
	if 'variable name="'  in line: # or 'name="y' in line:
		temparr = line.split('"')
		tempval = float(temparr[-2])
		myi = temparr[1]
		# if 'H'  in temparr[1]:
			# print temparr[1], tempval
		if 'z' in temparr[1] and tempval > 0.1:
			myi = temparr[1]
			myi = myi.replace('z', '')
			myi2 = myi.split('_')
			gp = myi2[0] +"_" + myi2[1]+"_" + myi2[2]+"_" + myi2[3]+"_" + myi2[4]
			myt = int(myi2[5])
			# for t in tps:
			corridors[myt].append(gp)
		if 'x' in temparr[1] and tempval > 0.1:
			myi = temparr[1]
			myi = myi.replace('x', '')
			myi2 = myi.split("_")
			solrxs[int(myi2[0])] = int(myi2[1])
		# if 'g' in temparr[1] and tempval > 0:
			# myi = temparr[1]
			# myi = myi.replace('g', '')
			# myi2 = myi.split('_')
			# myt = int(myi2[1])"
			# mygs[myt] = mygs[myt] + tempval
			# mygunits[myt].append(int(myi2[0]))
	
solf.close()
# print len(solrxs)
# print len(harvdict)
# print mygs

print "got sol"

for t in tps:
	tempd = {}
	templi = []
	# print t
	for i in corridors[t]:
		tempd[gpdict[i]['gp'][1]] = i
		if groundlich(i, t) > 0:
			templi.append(gpdict[i]['gp'][1])
	# for x in  mygunits[t]:
		# if x not in tempd:
			# print x
			# print tempd
			# print groundlich(tempd[x], t)
	
		

mynpv = 0.0
for x in solrxs:
	mynpv = mynpv + harvdict[x][solrxs[x]]['npv']
print mynpv
fw1 = open(writef, 'w')
writeline = 'TP, length, avg_resist, g_lich, t_lich, width\n'
fw1.write(writeline)
print writeline
li = []
for t in tps:
	li = []
	rmax = 0.0
	ltot = 0.0
	glich = 0.0
	tlich = 0.0
	rtot = 0.0
	rmax = 0.0
	width = 999999999.99
	for i in corridors[t]:
		# print i
		myr = resistance(i, t)
		rtot = rtot + myr
		if myr > rmax:
			rmax = myr
		ltot = ltot + gpdict[i]['l']
		glich = glich + groundlich(i, t)
		tlich = tlich + treelich(i, t)
		# if treelich(i, t)>0:
			# print i, t
		if gpdict[i]['w'] < width:
			width = gpdict[i]['w']
		if gpdict[i]['gp'][1] > eu:
			midpol = gpdict[i]['gp'][1]
			for c in clusters[midpol]:
				li.append(c)
		else:
			li.append(gpdict[i]['gp'][1])	
	li.sort()
	polycorrli[t] = li
	writeline = str(t) + ','+str(ltot) + ', ' + str(rtot/ltot*2000) + ', ' + str(glich)+ ',' + str(tlich)+ ',' + str(width) 
	print writeline
	fw1.write(writeline+ "\n")
	# fw1.write(str(li) + '\n\n\n')
	# break
fw1.close()


# # # Fix sol  
# fa = open("C:/rstjohn/SLU_Exp/LPs/21tps_maxt_5corr_sol.cpx" )
# fw = open("C:/rstjohn/SLU_Exp/LPs/21tps_fixed_0_5corr.cpx" , 'w')
# for line in fa:
	# # if '<variable name="x'  in line :# and 'value="1"' in line:
		# # temparr = line.split('"')
		# # writeline = "Fixed_" + temparr[1] + ":    " + temparr[1] + " = " +temparr[7]+ "\n"
		# # fw.write(writeline)
	# if ('name="z' in line or 'name="y' in line) and 'value="0"' not in line:
		# temparr = line.split('"')
		# writeline = "Fixed_" + temparr[1] + ":    " + temparr[1] + " = " +temparr[7]+ "\n"
		# # print writeline
		# fw.write(writeline)
		# # for t in tps:
			# # writeline = "Fixed_" + temparr[1] + str(t) + ":    " + temparr[1][:-1] + str(t) + " = " + temparr[7] + "\n"
			# # fw.write(writeline)			
# fa.close()
# fw.close()


print "End of Code"

