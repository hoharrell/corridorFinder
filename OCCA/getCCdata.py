
print "Getting Data"

import polycode


polyclustfile = "C:/rstjohn/SLU_Exp/polyclust.txt"
gpfile = "C:/rstjohn/SLU_Exp/gp_width_length.txt"
landfile = "C:/rstjohn/SLU_Exp/Sim_11tps.txt"
idkeyfile = "C:/rstjohn/SLU_Exp/parcel_data.txt"


polygons = polycode.polygons
clusters = polycode.clusters
su = polycode.startunit
eu = polycode.endunit
tps = range(0,  11)
wmin = 50.0
myg = 0.0
myt = 0.0



#get harvest data
harvdict = {}
f = open(landfile)
areadict = {}
for line in f:
	if "PERIOD" not in line:
		strarr = line.split(',')
		tp = int(strarr[0])
		u = int(strarr[1])
		ha = float(strarr[2])
		rx = int(strarr[3])
		row = int(strarr[5])
		basalarea = float(strarr[6])
		species = strarr[7]
		height = float(strarr[8])
		age = float(strarr[9])
		stems = float(strarr[10])
		volume = float(strarr[11])
		if strarr[12] != '':
			npv = float(strarr[12])
		rxname = strarr[13]
		veg = strarr[14]
		regensp = strarr[16]
		treatment = strarr[17]
		volharvested = float(strarr[18])
		if u not in areadict:
			areadict[u] = ha
		label = str(u) + "_" +str(rx)
		if u not in harvdict:
			harvdict[u] = {}
		if rx not in harvdict[u]:
			harvdict[u][rx] = {'label':label,  'npv': npv, 'rx name': rxname, 'ha': ha}
		if row == 0:
			harvdict[u][rx][tp]= {'ss' : False, "fert" : False, 'basal area': basalarea, 'species': species, 'height': height, 'age': age, 'stems' : stems, 'vol harvested' : volharvested, 'veg': veg}		
		if treatment == "SoilPreparation" or (tp > 0 and harvdict[u][rx][tp - 1]['ss'] and age < 50):
			harvdict[u][rx][tp]['ss'] = True
		if treatment == "Fertilization" or (tp > 0 and harvdict[u][rx][tp - 1]['fert']):
			harvdict[u][rx][tp]['fert'] = True
		if  species =='Contorta' or stems >= 2000:
			myr = 1
		elif stems > 1600 and height > 3.0:
			myr = 1
		else:
			myr = stems /  2000.0 
			if myr >= 1:
				print "Myr is too big! " +str(myr) + "   " + str(stems)
		if age > 120:
			myt = 1
		else:
			myt = 0
		if tp == 0  and "Lichen" in veg:
			myg = 1.0
		elif tp > 0 and species =='Pine' and age >= 10 and  harvdict[u][rx][tp]['ss'] == False and  basalarea < 20 and harvdict[u][rx][tp]['fert'] == False:
			myg = 1.0
		else:
			myg = 0.0
			# if (tp > 0 and harvdict[u][rx][tp-1]['ss']) or age < 15:
			# if  or age >=50:
			# elif tp > 0 or age >=50:
				# myg = 1 #harvdict[u][rx][tp-1]['g'] + 0.01
			# elif age >= 60:
				# myg = 0.25 + 0.002 * (age - 50) 
		# else:
			# myg = 0.0
			# if myg > 0.5:
				# myg = 0.5
			
		harvdict[u][rx][tp]['t'] = myt
		harvdict[u][rx][tp]['g'] = myg
		harvdict[u][rx][tp]['r'] = myr
f.close()		

	
#get dicts of clusters poly is in	
polyinclust = {}	
f = open(polyclustfile)
for line in f:
	strarr = line.split()
	polyinclust[int(strarr[0])] = []
	if len(strarr) > 1:
		for i in strarr:
			polyinclust[int(strarr[0])] .append(int(i))
f.close()
			
# get gps, widths, lengths
gpdict = {}
gpf=open(gpfile)
for line in gpf:
	strarr = line.split()
	gpkey = strarr[0]
	temparr = gpkey.split("_")
	gparr = []
	for i in temparr:
		gparr.append(int(i))
	if float(strarr[1]) > wmin:
		gpdict[gpkey]= {"gp": gparr, 'w': round(float(strarr[1]), 4), 'l': round(float(strarr[2]), 4)}	 
gpf.close()

#get gates
gates = {}
for g in gpdict:
	if su != gpdict[g]['gp'][1] and eu not in gpdict[g]['gp'][0:1]:
		gate1 = str(gpdict[g]['gp'][0]) + '_' + str(gpdict[g]['gp'][1]) + '_'+ str(gpdict[g]['gp'][3])
		if gate1 not in gates:
			gates[gate1] = {'arr': [gpdict[g]['gp'][0], gpdict[g]['gp'][1], gpdict[g]['gp'][3]], 'in':[], 'out': []}
		gates[gate1]['in'].append(g)
	if su not in gpdict[g]['gp'][1:2] and eu != gpdict[g]['gp'][1]:
		gate2 = str(gpdict[g]['gp'][1]) + '_' + str(gpdict[g]['gp'][2]) + '_'+ str(gpdict[g]['gp'][4])
		if gate2 not in gates:
			gates[gate2] = {'arr': [gpdict[g]['gp'][1], gpdict[g]['gp'][2], gpdict[g]['gp'][4]], 'in':[], 'out': []}
		gates[gate2]['out'].append(g)

#get dict of gps where [id] is middle polygon
midpolgpdict = {}
for i in polygons:
	midpolgpdict[i] =[]
for g in gpdict:
	midpol = gpdict[g]['gp'][1]
	midpolgpdict[midpol].append(g )
	if midpol in clusters:
		for j in clusters[midpol]:
			midpolgpdict[j].append(g )

			
#get id key, polyareas
origidforpoly = {}
polyarea = {}
myidforunit = {}
f = open(idkeyfile)
for line in f:
	if 'ha' not in line:
		strarr = line.split('\t')
		origidforpoly[int(strarr[0])] = int(strarr[1])
		myidforunit[int(strarr[1])] = int(strarr[0])
		polyarea[int(strarr[0])] = float(strarr[2])
for c in clusters:
	polyarea[c] = 0.0
	for u in clusters[c]:
		if origidforpoly[u] != 0:
			polyarea[c] = areadict[origidforpoly[u]] + polyarea[c]
		else:
			polyarea[c] = polyarea[u] + polyarea[c]
	# print c, clusters[c], polyarea[c]
				
f.close()

maxpolyarea = 0.0
for p in polyarea:
	if polyarea[p] > maxpolyarea:
		maxpolyarea = polyarea[p]

nfu = []
for p in polygons:
	if p not in clusters :
		if origidforpoly[p] in harvdict:
			unitli = [origidforpoly[p]]
		else:
			unitli = []
	else:
		unitli = []
		for a in clusters[p]:
			if origidforpoly[a] in harvdict:
				unitli.append(origidforpoly[a])
	if unitli == []:
		nfu.append(p)
nfgp = []
for g in gpdict:
	midpol = gpdict[g]['gp'][1]
	if midpol not in clusters:
		if origidforpoly[midpol] in harvdict:
			unitli = [origidforpoly[midpol]]
		else:
			unitli = []
	else:
		unitli = []
		for a in clusters[midpol]:
			if origidforpoly[a] in harvdict:
				unitli.append(origidforpoly[a])
	if unitli ==[]:
		nfgp.append(g)

noglich = []
notlich = []
for u in harvdict:
	isglich = False
	istlich = False
	for rx in harvdict[u]:
		for tp in tps:
			if harvdict[u][rx][tp]['g'] > 0:  
				isglich = True
				# print "got ground lichen!"
			if harvdict[u][rx][tp]['t'] > 0:
				istlich = True
				# print "got tree lichen!"
	if  isglich == False :
		noglich.append(u)
	if istlich == False:
		notlich.append(u)
		
		
print "got data"
