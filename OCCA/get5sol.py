solfile5 = "C:/rstjohn/6tps_maxnpv_full_sol2.cpx"
landfile5 = "C:/rstjohn/SLU_Exp/Sim_6tps.txt"
landfile = "C:/rstjohn/SLU_Exp/Sim_11tps.txt"



#get harvest data
harvdict5 = {}
f = open(landfile5)
for line in f:
	if "PERIOD" not in line:
		strarr = line.split(',')
		tp = int(strarr[0])
		u = int(strarr[1])
		rx = int(strarr[3])
		row = int(strarr[4])
		treatment = strarr[16]
		volharv = float(strarr[17])
		if u not in harvdict5:
			harvdict5[u] = {}
		if rx not in harvdict5[u]:
			harvdict5[u][rx] = {}
		if row == 0:
			harvdict5[u][rx][tp]= {}
			harvdict5[u][rx][tp]["treatment"] = []
			harvdict5[u][rx][tp]["vh"] = volharv
		if treatment != "None":
			harvdict5[u][rx][tp]["treatment"].append(treatment)	
		
		
mydict = {}
rxdict = {}
tps = range (0,6)
for i in harvdict5:
	mydict[i] = {}
	rxdict[i] = []
	for t in tps:
		mydict[i][t] = []
	
fa = open(solfile5)
for line in fa:
	if '<variable name="x'  in line and 'value="1"' in line:
		temparr = line.split('"')
		temparr2 = temparr[1].split("_")
		stand = int(temparr2[0][1:])
		rx = int(temparr2[1])
		for t in tps:
			mydict[stand][t] = {}
			mydict[stand][t]['treatment'] = harvdict5[stand][rx][t]['treatment']
			mydict[stand][t]['vh'] = harvdict5[stand][rx][t]['vh']
fa.close()

print "got 5tp sol."


#get harvest data
harvdict10 = {}
f = open(landfile)
for line in f:
	if "PERIOD" not in line:
		strarr = line.split(',')
		tp = int(strarr[0])
		u = int(strarr[1])
		rx = int(strarr[3])
		row = int(strarr[5])
		treatment = strarr[17]
		volharv = float(strarr[18])
		if u not in harvdict10:
			harvdict10[u] = {}
		if rx not in harvdict10[u]:
			harvdict10[u][rx] = {}
		if row == 0:
			harvdict10[u][rx][tp]= {}
			harvdict10[u][rx][tp]['treatment'] = []
			harvdict10[u][rx][tp]['vh'] = volharv
		if treatment != "None":
			harvdict10[u][rx][tp]['treatment'].append(treatment)	
f.close()		



badstands = []
tps = range(0,6)
for i in mydict:
	for rx10 in harvdict10[i]:
		isequal = True
		for t in tps:
			li1 = harvdict10[i][rx10][t]['treatment']
			li2 = mydict[i][t]['treatment']
			li1.sort()
			li2.sort()
			if li1 != li2:
				isequal = False
				break
			if harvdict10[i][rx10][t]['vh'] != mydict[i][t]['vh']:
				isequal = False
				break
		if isequal == True:
			rxdict[i].append(rx10)
	if rxdict[i] == []:
		badstands.append(i)


		
		
# print len(badstands)
# print len(rxdict)
# test = badstands[10]
# print "test stand is "+str(test)
# print mydict[test]


# print "10 rxs..."
# for rx10 in harvdict10[test]:
	# myli = {}
	# myvh = {}
	# for t in tps:
		# if 'Thinning' in harvdict10[test][rx10][1]['treatment']:
			# myli[t] = harvdict10[test][rx10][t]['treatment']
			# myvh[t] = harvdict10[test][rx10][t]['vh']
	# if myli != {}:
		# print myli
		# print myvh
	
print "End of get5sol.py"