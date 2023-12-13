print "starting CCLP writer"
import polycode


lpfile = "C:/rstjohn/SLU_Exp/LPs/maxtree_LP_lazy_nocluster.cpx" 

polyclustfile = "C:/rstjohn/SLU_Exp/polyclust.txt"
gpfile = "C:/rstjohn/SLU_Exp/gp_width_length.txt"
landfile = "C:/rstjohn/SLU_Exp/rx_data.txt"
clustconstfile = "C:/rstjohn/SLU_Exp/harvest_cluster_constraints.txt"
idkeyfile = "C:/rstjohn/SLU_Exp/parcel_data.txt"

print "Getting data"

polygons = polycode.polygons
clusters = polycode.clusters
su = polycode.startunit
eu = polycode.endunit
tps = range(0, 1) #1)
fmin = 0.15
fmax = 0.15
gmin = 100.0
tmin = 10.0
Rmax = 10000
rtot = 500.0
wmin = 0.0


myg = 0.0
myt = 0.0

#get harvest data
harvdict = {}
f = open(landfile)
for line in f:
	if "PERIOD" not in line:
		strarr = line.split('\t')
		if int(strarr[1]) not in harvdict:
			harvdict[int(strarr[1])] = {}
			myg = myg + float(strarr[14]) * float(strarr[12])
			myt = myt + float(strarr[15]) * float(strarr[12])
		label = strarr[1] + "_" + strarr[2]
		if int(strarr[2]) not in harvdict[int(strarr[1])]:
			label = strarr[1] + "_" + strarr[2]
			harvdict[int(strarr[1])][int(strarr[2])] = {'label':label,  'npv': float(strarr[9] ), 'treatment': strarr[10] , 'ha': float(strarr[12]) }
		harvdict[int(strarr[1])][int(strarr[2])][int(strarr[0])] = {'Basal Area': float(strarr[4]), 'Stems' : float(strarr[7]), 'Vol Harvested' : float(strarr[11]), 'r' : float(strarr[13]), 'g': float(strarr[14]), 't': float(strarr[15])}		
			
f.close()		



#get dicts of clusters poly is in	
polyinclust = {}	
# f = open(polyclustfile)
# for line in f:
	# strarr = line.split()
	# polyinclust[int(strarr[0])] = []
	# if len(strarr) > 1:
		# for i in strarr:
			# polyinclust[int(strarr[0])] .append(int(i))
# f.close()
		
		
# get gps, widths, lengths
count = 0
maxlen = 0.0
gpdict = {}
gpf=open(gpfile)
for line in gpf:
	count = count+1
	strarr = line.split()
	gpkey = strarr[0]
	temparr = gpkey.split("_")
	gparr = []
	clust = False
	for i in temparr:
		gparr.append(int(i))
		
	if float(strarr[1]) > wmin and gparr[0]<=eu and gparr[1]<=eu and gparr[2]<=eu:
		gpdict[gpkey]= {"gp": gparr, 'w': round(float(strarr[1]), 4), 'l': round(float(strarr[2]), 4)}	  #str(count)
		if float(strarr[2])> maxlen:
			maxlen = float(strarr[2])
gpf.close()
maxlen = maxlen+10



	

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
for i in polygons:
	polyarea[i] = 0.0
myidforunit = {}
f = open(idkeyfile)
for line in f:
	if 'ha' not in line:
		strarr = line.split('\t')
		origidforpoly[int(strarr[0])] = int(strarr[1])
		myidforunit[int(strarr[1])] = int(strarr[0])
		polyarea[int(strarr[0])] = float(strarr[2])
		if int(strarr[0]) in polyinclust:
			for a in polyinclust[int(strarr[0])]:
				polyarea[a] = polyarea[a] + float(strarr[2])
f.close()

maxarea = 0.0
for i in polyarea:
	if polyarea[i] > maxarea:
		maxarea = polyarea[i]
maxarea = maxarea+10

nolich = []
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
		nolich.append(p)
noresist = []
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
		noresist.append(g)
		
		
		
		
print "writing file"
############################ Write LP #############################

fw = open(lpfile, 'w')

fw.write("MAX \nOBJECTIVE: \n")
writeline = "xx"
for t in tps:
	for p in polygons:
		if p not in nolich:
			if writeline =="xx":
				writeline ="t" + str(p) + "_" + str(t)
			else:
				writeline = writeline + " + t" + str(p) + "_" + str(t)
			if len(writeline) > 70:
				fw.write(writeline + '\n')
				writeline = ""
fw.write(writeline)
print "Objective Written"

fw.write("\nSubject to:\n")
# max tree
for t in tps:
	writeline = "Max_TreeLich_" + str(t) + ":  "
	for p in polygons:
		if p not in nolich:
			if writeline =="Max_TreeLich_" + str(t) + ":  ":
				writeline ="t" + str(p) + "_" + str(t)
			else:
				writeline = writeline + " + t" + str(p) + "_" + str(t)
			if len(writeline) > 70:
				fw.write(writeline + '\n')
				writeline = ""
	writeline =writeline + " <= 200 \n"
	fw.write(writeline)
	
# Fix harvest
fixedrxs={}
fa = open("C:/rstjohn/SLU_Exp/LPs/sol_harvest.cpx")
for line in fa:
	if '<variable name="x'  in line  and 'value="1"' in line:
		temparr = line.split('"')
		templi = temparr[1].split("_")
		templi[0] = templi[0].replace('x', '')
		# print templi
		fixedrxs[int(templi[0])] = int(templi[1])
		# temparr = line.split('"')
		# writeline = "Fixed_" + temparr[1] + ":    " + temparr[1] + "=1\n"
		# fw.write(writeline)
		# print writeline
fa.close()
	
	
print "Harvest Constraints Written"




# ##################### Corridor connectivity constraints #############
# #start flow
# for t in tps:
	# writeline = "Start_Flow_" + str(t) + ":  " 
	# for g in gpdict:
		# if gpdict[g]['gp'][0] == su:
			# if writeline ==  "Start_Flow_" + str(t) + ":  " :
				# writeline = writeline + "z" + g + "_" + str(t)
			# else:
				# writeline = writeline + " + z" + g + "_" + str(t)
			# if len(writeline) > 50:
				# fw.write(writeline + "\n")
				# writeline = ""
	# writeline = writeline + " = 1 \n"
	# fw.write(writeline)

writeline = "Start_Flow:  " 
for g in gpdict:
	if gpdict[g]['gp'][0] == su:
		if writeline ==  "Start_Flow:  " :
			writeline = writeline + "z" + g 
		else:
			writeline = writeline + " + z" + g 
		if len(writeline) > 70:
			fw.write(writeline + "\n")
			writeline = ""
writeline = writeline + " = 1 \n"
fw.write(writeline)
writeline = "End_Flow:  " 
for g in gpdict:
	if gpdict[g]['gp'][2] == eu:
		if writeline == "End_Flow:  " :
			writeline = writeline + "z" + g 
		else:
			writeline = writeline + " + z" + g 
		if len(writeline) > 70:
			fw.write(writeline + "\n")
			writeline = ""
writeline = writeline + " = 1 \n"
fw.write(writeline)
#end flow
# for t in tps:
	# writeline = "End_Flow_" + str(t) + ":  " 
	# for g in gpdict:
		# if gpdict[g]['gp'][2] == eu:
			# if writeline ==  "End_Flow_" + str(t) + ":  " :
				# writeline = writeline + "z" + g + "_" + str(t)
			# else:
				# writeline = writeline + " + z" + g + "_" + str(t)
			# if len(writeline) > 70:
				# fw.write(writeline + "\n")
				# writeline = ""
	# writeline = writeline + " = 1 \n"
	# fw.write(writeline)

# #Start commod Flow
# for t in tps:
	# writeline = "Start_y_Flow_" + str(t) + ":   "
	# for g in gpdict:
		# if gpdict[g]['gp'][0] == su:
			# if writeline == "Start_X_Flow_" + str(t) + ":   ":
				# writeline = writeline + "y" + g + "_" + str(t)
			# else:
				# writeline = writeline + " + y" + g + "_" + str(t)
			# if len(writeline) > 70:
				# fw.write(writeline + "\n")
				# writeline = ""
	# writeline = writeline + " <= " + str(len(harvdict)) + "\n"
	# fw.write(writeline)

writeline = "Start_y_Flow:   "
for g in gpdict:
	if gpdict[g]['gp'][0] == su:
		if writeline == "Start_y_Flow:   ":
			writeline = writeline + "y" + g 
		else:
			writeline = writeline + " + y" + g 
		if len(writeline) > 70:
			fw.write(writeline + "\n")
			writeline = ""
writeline = writeline + " <= " + str(len(harvdict)) + "\n"
fw.write(writeline)

	
# # Flow Conservation
# for t in tps:
	# for g in gates:
		# if eu ==  gates[g]['arr'][1] or su == gates[g]['arr'][0]:
			# continue
		# writeline = "Flow_Conservation_" + g + "_" + str(t) + ":   "
		# if gates[g]['out'] != []:
			# for i in gates[g]['out']:
				# if writeline == "Flow_Conservation_" + g + "_" + str(t) + ":   ":
					# writeline = writeline + "y" + i + "_" + str(t) +  " - z" + i + "_" + str(t)
				# else:
					# writeline = writeline + " + y" + i + "_" + str(t) +  " - z" + i + "_" + str(t)
				# if len(writeline) > 70:
					# fw.write(writeline + "\n")
					# writeline = ""
			# if gates[g]['in'] ==[]:
				# writeline = writeline + " = 0 \n"
				# fw.write(writeline)
		# if gates[g]['in'] != []:
			# if gates[g]['out'] == []:
				# for i in gates[g]['in']:
					# if writeline == "Flow_Conservation_" + g + "_" + str(t) + ":   ":
						# writeline = writeline + "y" + i + "_" + str(t) 
					# else:
						# writeline = writeline + " + y" + i + "_" + str(t) 
					# if len(writeline) > 70:
						# fw.write(writeline + "\n")
						# writeline = ""
				# writeline = writeline + " = 0\n"
				# fw.write(writeline)
			# else:
				# for i in gates[g]['in']:
					# writeline = writeline + " - y" + i + "_" + str(t) 
					# if len(writeline) > 70:
						# fw.write(writeline + "\n")
						# writeline = ""
				# writeline = writeline + " = 0\n"
				# fw.write(writeline)

				#CAME FROM HERE!!!
				#y defs
# for t in tps:
	# for gp in gpdict:
		# writeline = "Y_Def1_ " + gp + "_" + str(t) + ":   z"+ gp + "_" + str(t) +" - y" + gp + "_" + str(t) + " <= 0\n" 
		# fw.write(writeline)
		# writeline = "Y_Def2_ " + gp + "_" + str(t) + ":   y"+ gp + "_" + str(t) +" - " + str(len(harvdict)) + "z" + gp + "_" + str(t) + " <= 0\n" 
		# fw.write(writeline)
		# writeline= "Y_nonneg_"+ gp + "_" + str(t) + ":   y"+ gp + "_" + str(t) + " >= 0\n"
		# fw.write(writeline)

for gp in gpdict:
	writeline = "Y_Def1_ " + gp + ":   z"+ gp +" - y" + gp + " <= 0\n" 
	fw.write(writeline)
	writeline = "Y_Def2_ " + gp +  ":   y"+ gp + " - " + str(len(harvdict)) + "z" + gp + " <= 0\n" 
	fw.write(writeline)
	writeline= "Y_nonneg_"+ gp + ":   y" + gp + " >= 0\n"
	fw.write(writeline)
		
print "corridor connectivity constraints written"


	# for t in tps:
		# for m in range(0, 3):
			# if tempdict[p][m] == []:
				# continue
			# writeline = "Clust_Const_" + str(p) + "_" + str(t) + "_" + str(m) + ":   "
			# for a in tempdict[p][m]:
				# if writeline == "Clust_Const_" + str(p) + "_" + str(t) + "_" + str(m) + ":   ":
					# writeline = writeline + "z" + a + "_" + str(t)
				# else:
					# writeline = writeline + "+z" + a + "_" + str(t)
				# if len(writeline) > 70:
					# fw.write(writeline + '\n')
					# writeline = ""
			# writeline = writeline + " <= 1\n"
			# fw.write(writeline)

print "Cluster constraints written"			

# # # ############ Lichen constraints #############################

#g lich def consts
for p in polygons:
	if p not in nolich:
		if p not in clusters :
			unitli = [origidforpoly[p]]
		else:
			unitli = []
			for a in clusters[p]:
				if origidforpoly[a] in harvdict:
					unitli.append(origidforpoly[a])
		totarea = polyarea[p]
		for t in tps:
			writeline = "G_Lich_Def_1_" + str(p) + "_" + str(t) + ":    g" + str(p) + "_" + str(t)
			for u in unitli:
				rx = fixedrxs[u]
				# for rx in harvdict[u]:
				writeline = writeline + " - " +str(harvdict[u][rx]['ha'] * harvdict[u][rx][t]['g'] ) + "x" +  harvdict[u][rx]['label']
				if len(writeline) > 70:
					fw.write(writeline + '\n')
					writeline = ""
			writeline = writeline + "< = 0\n"
			fw.write(writeline)
			writeline = "G_Lich_Def_2_" + str(p) + "_" + str(t) + ":    g" + str(p) + "_" + str(t)
			for g in midpolgpdict[p]:
				writeline = writeline + " - " + str(maxarea) + "z" + g #+ "_" + str(t)
				if len(writeline) > 70:
					fw.write(writeline + '\n')
					writeline = ""
			writeline = writeline + " <= 0\n"
			fw.write(writeline)

			

#g accounting const	
for t in tps:
	writeline = "G_Lichen_Min"+ str(t) +":  "
	for p in polygons:
		if p not in nolich:
			if writeline == "G_Lichen_Min:  ":
				writeline = writeline + "g" + str(p) + "_" + str(t)
			else:
				writeline = writeline + " + g" + str(p) + "_" + str(t)
			if len(writeline) > 70:
				fw.write(writeline + '\n')
				writeline = ""
	writeline = writeline + " >= " + str(gmin) + "\n"
	fw.write(writeline)


#t lich def consts
for p in polygons:
	if p not in nolich:
		if p not in clusters :
			unitli = [origidforpoly[p]]
		else:
			unitli = []
			for a in clusters[p]:
				if origidforpoly[a] in harvdict:
					unitli.append(origidforpoly[a])
		totarea = polyarea[p]
		for t in tps:
			writeline = "T_Lich_Def_1_" + str(p) + "_" + str(t) + ":    t" + str(p) + "_" + str(t)
			for u in unitli:
				rx = fixedrxs[u]
				# for rx in harvdict[u]:
				writeline = writeline + " - " +str(harvdict[u][rx]['ha'] * harvdict[u][rx][t]['t'] ) + "x" +  harvdict[u][rx]['label']
				if len(writeline) > 70:
					fw.write(writeline + '\n')
					writeline = ""
			writeline = writeline + "< = 0\n"
			fw.write(writeline)
			writeline = "T_Lich_Def_2_" + str(p) + "_" + str(t) + ":    t" + str(p) + "_" + str(t)
			for g in midpolgpdict[p]:
				writeline = writeline + " - " + str(maxarea) + "z" + g #+ "_" + str(t)
				if len(writeline) > 70:
					fw.write(writeline + '\n')
					writeline = ""
			writeline = writeline + " <= 0\n"
			fw.write(writeline)

#t accounting const
# for t in tps:
	# writeline = "T_Lichen_Min"+ str(t) +":  "
	# for p in polygons:
		# if p not in nolich:
			# if writeline =="T_Lichen_Min"+ str(t) +":  ":
				# writeline = writeline + "t" + str(p) + "_" + str(t)
			# else:
				# writeline = writeline + " + t" + str(p) + "_" + str(t)
			# if len(writeline) > 50:
				# fw.write(writeline + '\n')
				# writeline = ""
	# writeline =writeline + " >= " + str(tmin) + "\n"
	# fw.write(writeline)

print "lichen constraints written"

############## Resistance Constraints ########

# # r def consts  FIX VARID
# count = 0
# for g in gpdict:
	# if g not in noresist:
		# midpol = gpdict[g]['gp'][1]
		# if midpol not in clusters:
			# unitli = [origidforpoly[midpol]]
		# else:
			# unitli = []
			# for a in clusters[midpol]:
				# if origidforpoly[a] in harvdict:
					# unitli.append(origidforpoly[a])
		# totarea = polyarea[midpol]
		# for t in tps:
			# writeline = "R_Def_1_" +  gpdict[g]['varid'] +"_" + str(t) + ":   r"+gpdict[g]['varid'] +"_" + str(t) + " - " + str(maxlen) + "z" + gpdict[g]['varid'] +"_" + str(t) + " <= 0\n"
			# fw.write(writeline)	
			# writeline = "R_def_2_" + gpdict[g]['varid'] +"_" + str(t) + ":   "+ str(totarea) + "z" + gpdict[g]['varid'] +"_" + str(t)+ " - " + "r" + gpdict[g]['varid'] +"_" + str(t)
			# for u in unitli:
				# for rx in harvdict[u]:
					# writeline = writeline + " + " +str( harvdict[u][rx]['ha'] * harvdict[u][rx][t]['r'] * gpdict[g]['l'] / totarea) +  "x" +  harvdict[u][rx]['label']
					# if len(writeline) > 70:
						# fw.write(writeline + '\n')
						# writeline = ""
			# writeline = writeline + " <= " + str(maxlen) + '\n'
			# fw.write(writeline)
					
# # r tot constraint
# for t in tps:
	# print t
	# writeline = "Resist_Total_" + str(t) + ":   "
	# for g in gpdict:
		# if g not in noresist:
			# if writeline == "Resist_Total_" + str(t) + ":   ":
				# writeline = writeline + "r"  + gpdict[g]['varid'] +"_" + str(t)
			# else:
				# writeline = writeline + " + r"  + gpdict[g]['varid'] +"_" + str(t)
			# if len(writeline) > 70:
				# fw.write(writeline + '\n')
				# writeline = ""
	# writeline = writeline + " <= " + str(rtot) + "\n"
	# fw.write(writeline)
	
# print "Resistance constraints written"

#LAZY
fw.write("\nLazy Constraints\n")
for g in gates:
	if eu ==  gates[g]['arr'][1] or su == gates[g]['arr'][0]:
		continue
	writeline = "Flow_Conservation_" + g + ":   "
	if gates[g]['out'] != []:
		for i in gates[g]['out']:
			if writeline == "Flow_Conservation_" + g + ":   ":
				writeline = writeline + "y" + i +  " - z" + i 
			else:
				writeline = writeline + " + y" + i +  " - z" + i 
			if len(writeline) > 70:
				fw.write(writeline + "\n")
				writeline = ""
		if gates[g]['in'] ==[]:
			writeline = writeline + " = 0 \n"
			fw.write(writeline)
	if gates[g]['in'] != []:
		if gates[g]['out'] == []:
			for i in gates[g]['in']:
				if writeline == "Flow_Conservation_" + g + ":   ":
					writeline = writeline + "y" + i 
				else:
					writeline = writeline + " + y" + i 
				if len(writeline) > 70:
					fw.write(writeline + "\n")
					writeline = ""
			writeline = writeline + " = 0\n"
			fw.write(writeline)
		else:
			for i in gates[g]['in']:
				writeline = writeline + " - y" + i 
				if len(writeline) > 70:
					fw.write(writeline + "\n")
					writeline = ""
			writeline = writeline + " = 0\n"
			fw.write(writeline)

				
#max gate flow
# for t in tps:
	# for g in gates:
		# if gates[g]['out'] != []:
			# writeline = "MaxNumFlows_" + g + "_" + str(t) + ":   "
			# for i in gates[g]['out']:
				# if writeline == "MaxNumFlows_" + g + "_" + str(t) + ":   ":
					# writeline = writeline + "z" + i + "_" + str(t) 
				# else:
					# writeline = writeline + " + z" + i + "_" + str(t) 
				# if len(writeline) > 70:
					# fw.write(writeline + "\n")
					# writeline = ""
			# writeline = writeline + " <= 1\n"
			# fw.write(writeline)
for g in gates:
	if gates[g]['out'] != []:
		writeline = "MaxNumFlows_" + g + ":   "
		for i in gates[g]['out']:
			if writeline == "MaxNumFlows_" + g + ":   ":
				writeline = writeline + "z" + i 
			else:
				writeline = writeline + " + z" + i 
			if len(writeline) > 70:
				fw.write(writeline + "\n")
				writeline = ""
		writeline = writeline + " <= 1\n"
		fw.write(writeline)


# # clust consts
# tempdict = {}
# for g in gpdict:
	# for p in gpdict[g]['gp'][0:2]:
		# myind =  gpdict[g]['gp'][0:2].index(p)
		# if p in clusters:
			# for a in clusters[p]:
				# if a not in tempdict:
					# tempdict[a] = [[],[],[]]
				# tempdict[a][myind].append(g)
		# else:
			# if p not in tempdict:
				# tempdict[p] = [[],[],[]]
			# tempdict[p][myind].append(g)
# for p in tempdict:
	# for m in range(0, 3):
		# if tempdict[p][m] == []:
			# continue
		# writeline = "Clust_Const_" + str(p) + "_" + str(m) + ":   "
		# for a in tempdict[p][m]:
			# if writeline == "Clust_Const_" + str(p) + "_" + str(m) + ":   ":
				# writeline = writeline + "z" + a 
			# else:
				# writeline = writeline + " + z" + a 
			# if len(writeline) > 70:
				# fw.write(writeline + '\n')
				# writeline = ""
		# writeline = writeline + " <= 1\n"
		# fw.write(writeline)

################ Variable Ranges ######################

#bounds
fw.write("\nbounds\n")
for i in polygons:
	if i not in nolich:
		writeline = ""
		for t in tps:
			writeline = writeline + "0 <= g" + str(i) + "_" + str(t) + " <= " + str(maxarea) + "\n"
			writeline =  writeline + "0 <= t" + str(i) + "_" + str(t) + " <= " + str(maxarea) + "\n"
		fw.write(writeline)
# for g in gpdict:
	# if g not in noresist:
		# writeline = ""
		# for t in tps:
			# writeline = writeline + "0 <= r" +  gpdict[g]['varid'] +"_" + str(t) +"<=" + str(maxlen)+ "\n"
		# fw.write(writeline)
	
#binary x
fw.write('\nBinary\n')
writeline = ""
# for i in harvdict:
	# for rx in harvdict[i]:
		# writeline = writeline + '\tx' + harvdict[i][rx]['label']
		# if len(writeline) > 70:
			# fw.write(writeline + '\n')
			# writeline = ""
# fw.write(writeline)
			
for g in gpdict:
	writeline = writeline + '\tz' + g 
	if len(writeline) > 70:
		fw.write(writeline + '\n')
		writeline = ""
	# for t in tps:
		# writeline = writeline + '\tz' + g + "_" + str(t)
		# if len(writeline) > 70:
			# fw.write(writeline + '\n')
			# writeline = ""
fw.write(writeline + '\n')
			

fw.write('\n\nEnd')

fw.close()
print "End of SLU Harvest LP writer"