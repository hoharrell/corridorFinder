print "starting CC LP writer"
import polycode


gpfile = "C:/rstjohn/SLU_Exp/gp_width_length.txt"
landfile = "C:/rstjohn/SLU_Exp/landscape_data.txt"
lpfile = "C:/rstjohn/SLU_Exp/polyclust_constraints.txt" 

############## FUNCTIONS ######################

def getgates(gparr):
	#input: gate pair ints
	#output: adds to gates dict
	gate1 = (gparr[0], gparr[1], gparr[3])
	gate2 = (gparr[1], gparr[2], gparr[4])
	if gate1 not in gates.keys():
		gates[gate1] = {"in" : [], "out" : []}
	if gate2 not in gates.keys():
		gates[gate2] = {"in" : [], "out" : []}
	if gpkey not in gates[gate1]["in"]:
		gates[gate1]["in"].append(gpkey)
	if gpkey not in gates[gate2]["out"]:
		gates[gate2]["out"].append(gpkey)
		
#################################################
print "Getting data"

polygons = polycode.polygons
clusters = polycode.clusters
su = polycode.startunit
eu = polycode.endunit
minwidththreshold = 30.0
maxunitresistance = 30.0
avgresistancemax = 10.0

myflow = '20000'

#get poly lich, resist
polyinfo = {}
f = open(landfile)
for line in f:
	if "id" not in line:
		# print line
		strarr = line.split()
		pp = int(strarr[0])
		polyinfo[pp] = {}
		polyinfo[pp]['ha'] = round(float(strarr[1]), 4)
		polyinfo[pp]['g'] = round(float(strarr[2]), 4)
		polyinfo[pp]['t'] = round(float(strarr[3]), 4)
		polyinfo[pp]['r'] = round(float(strarr[4]), 4)
f.close()		

gtot= 0.0
ttot = 0.0
for i in polyinfo:
	gtot = gtot + polyinfo[i]['g']*polyinfo[i]['ha']
	ttot = ttot + polyinfo[i]['t']*polyinfo[i]['ha']


#get dicts of clusters poly is in	
polyinclust = {}	
f = open("C:/rstjohn/SLU_Exp/polyclust.txt")
for line in f:
	strarr = line.split()
	polyinclust[int(strarr[0])] = []
	if len(strarr) > 1:
		for i in strarr:
			polyinclust[int(strarr[0])] .append(int(i))
f.close()

		
		
# get gps, widths, lengths, gates #

count = 0
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
	gpdict[gpkey]= {"gp": gparr, 'w': round(float(strarr[1]), 4), 'l': round(float(strarr[2]), 4), 'varid' : str(count)}	
gpf.close()


	
fr = open("C:/rstjohn/SLU_Exp/varids.txt" , 'w')
for g in gpdict:
	writeline = g + "\t" + gpdict[g]['varid'] + '\n'
	fr.write(writeline)
fr.close()
	

#get gate info
f = open("C:/rstjohn/SLU_Exp/gp_in_out.txt")
gates = {}
for line in f:
	strarr = line.split()
	if strarr[1] not in gates.keys():
		gates[strarr[1]] = {}
	gates[strarr[1]][strarr[0]] = []
	for i in strarr[2:]:
		gates[strarr[1]][strarr[0]].append(i)
# for g in gates:
	# writeline = "in \t" + str(g)
	# for i in gates[g]['in']:
		# writeline = writeline + '\t' + str(i)
	# f.write(writeline + '\n')
	# writeline = "out \t" + str(g)
	# for j in gates[g]['out']:
		# writeline = writeline + '\t' + str(j)
	# f.write(writeline + '\n')
f.close()
		
print len(gpdict)


print "writing file"
# print "Got data.  Writing LP"
# ##### Write LP #########

fw = open(lpfile, 'w')

# fw.write("MAX \nOBJECTIVE: \n")
# writeline = "xx"
# count = 0
# for g in gpdict:
	# id = gpdict[g]['gp'][1]
	# if polyinfo[id]['g'] > 0:
		# if writeline == "xx":
			# writeline = str(polyinfo[id]['g']) + "z" + gpdict[g]['varid']  
		# else:
			# writeline = writeline + " + " + str(polyinfo[id]['g']) + "z" + gpdict[g]['varid'] 
		# count = count +1
		# if len(writeline) > 50:
			# # fw.write(writeline + "\n")
			# # writeline = ""
			
			
fw.write("MIN \nOBJECTIVE: \n")
writeline = "xx"
for g in gpdict:
	id = gpdict[g]['gp'][1]
	if polyinfo[id]['g'] > 0:
		if writeline == "xx":
			writeline = str(polyinfo[id]['r']*gpdict[g]['l'] ) + "z" + gpdict[g]['varid']  
		else:
			writeline = writeline + " + " + str(polyinfo[id]['r']*gpdict[g]['l']) + "z" + gpdict[g]['varid'] 
		count = count +1
		if len(writeline) > 50:
			fw.write(writeline + "\n")
			writeline = ""
fw.write(writeline + '\n')
print "Objective Written"

fw.write("\nSubject to:\n")


#start flow
writeline = "Start_Flow:\t"
for g in gpdict:
	if gpdict[g]['gp'][0] == su:
		if writeline ==  "Start_Flow:\t":
			writeline = writeline + "z" + gpdict[g]['varid'] 
		else:
			writeline = writeline + " + z" + gpdict[g]['varid'] 
		if len(writeline) > 50:
			fw.write(writeline + "\n")
			writeline = ""
writeline = writeline + " = 1 \n"
fw.write(writeline)
	

#end flow
writeline = "End_Flow:\t"
for g in gpdict:
	if gpdict[g]['gp'][2] == eu:
		if writeline ==  "End_Flow:\t":
			writeline = writeline + "z" + gpdict[g]['varid'] 
		else:
			writeline = writeline + " + z" + gpdict[g]['varid'] 
		if len(writeline) > 50:
			fw.write(writeline + "\n")
			writeline = ""
writeline = writeline + " = 1 \n"
fw.write(writeline)


# keep flow
writeline = "XX"
count = 0
cc = 0
kk = True
for i in gates:
	if su != i[0] and eu != i[1]:
		gatestr = str(i[0]) + "_" + str(i[1]) + "_" + str(i[2])
		for x1 in gates[i]["in"]:
			if writeline == "XX": 
				writeline = "Flow_Const_" + gatestr + ":      z"+gpdict[x1]['varid']
			else:
				writeline = writeline + " + z" + gpdict[x1]['varid']
			cc = cc + 1
			if cc > 6:
				fw.write(writeline + "\n")
				writeline = ""
				cc = 0
		for x2 in gates[i]["out"]:
			if writeline == "XX":
				writeline = "Flow_Const_" + gatestr + ":      z" + gpdict[x2]['varid']
			elif gates[i]["in"] == []:
				writeline = writeline + " + z" + gpdict[x2]['varid']
			else:
				writeline = writeline + " - z" + gpdict[x2]['varid']
			cc = cc + 1
			if cc > 6:
				fw.write(writeline + "\n")
				writeline = ""
				cc = 0  
		if writeline == "XX":
			print "ERROR IN NETFLOW!"
			break
		writeline = writeline + " = 0\n"
		fw.write(writeline)
		count = count+1
		writeline = "XX"
# #init flow
# writeline = "Init_Flow:  t0 "
# for g in gpdict:
	# if gpdict[g]['gp'][0] == su:
		# writeline = writeline + " + y" + gpdict[g]['varid'] 
		# if len(writeline) > 50:
			# fw.write(writeline + "\n")
			# writeline = ""
# writeline = writeline + " = " + myflow + " \n"
# fw.write(writeline)

# #enforce flow 1
# for g in gpdict:
	# writeline = "Flow1_" + gpdict[g]['varid']  +":   y" + gpdict[g]['varid']  + " - " + myflow + "z" + gpdict[g]['varid']  + "<=0"
	# fw.write(writeline + "\n")

# #enforce flow 2
# count = 0
# for g in gates:
	# count = count + 1
	# writeline = "Flow2_" + str(count) + ":   "
	# for i in gates[g]['out']:
		# if writeline == "Flow2_" + str(count) + ":   ":
			# writeline = writeline + "y" + gpdict[i]['varid'] 
		# else:
			# writeline = writeline + " + y" + gpdict[i]['varid'] 
		# if len(writeline) > 50:
			# fw.write(writeline + '\n')
			# writeline = ""
	# for j in gates[g]['in']:
		# if len(gates[g]['out']) > 0:
			# writeline = writeline + " - y" + gpdict[j]['varid']  + " - z" + gpdict[j]['varid'] 
		# else:
			# if writeline == "Flow2_" + str(count) + ":   ":
				# writeline = writeline + " y" + gpdict[j]['varid']  + " + z" + gpdict[j]['varid'] 
			# else:
				# writeline = writeline + " + y" + gpdict[j]['varid']  + " + z" + gpdict[j]['varid'] 
		# if len(writeline) > 50:
			# fw.write(writeline + '\n')
			# writeline = ""
	# writeline = " = 0 \n"
	# fw.write(writeline)


# # enforce flow 3
# writeline = "Flow3:   t0 "
# for g in gpdict:
	# writeline = writeline + " + z" + gpdict[g]['varid'] 
	# if len(writeline) >50:
		# fw.write(writeline + '\n')
		# writeline = ''
# writeline = writeline + " = " + myflow + "\n"
# fw.write(writeline)

# width restriction
writeline = "Width_Restriction:  "
for g in gpdict:
	if gpdict[g]['w'] < minwidththreshold:
		if writeline == "Width_Restriction:  ":
			writeline = writeline + "z" + gpdict[g]['varid'] 
		else:
			writeline = writeline + " + z" + gpdict[g]['varid'] 
		if len(writeline) >50:
			fw.write(writeline + '\n')
			writeline = ''
writeline = writeline + " = 0\n"
fw.write(writeline)

# #resist for unit < #
writeline = "Unit_Resistance:  "
for g in gpdict:
	midunit = gpdict[g]['gp'][1]
	if polyinfo[midunit]['r'] > maxunitresistance:
		if  writeline == "Unit_Resistance:  ":
			writeline = writeline + "z" + gpdict[g]['varid'] 
		else: 
			writeline = writeline + " + z" + gpdict[g]['varid'] 
		if len(writeline) >50:
			fw.write(writeline + '\n')
			writeline = ''
if writeline != "Unit_Resistance:  ":
	writeline = writeline + " = 0 \n"
	fw.write(writeline)

# # avg resist for land < #
# writeline = "Total_avg_Resistance:  "
# for g in gpdict:
	# midunit = gpdict[g]['gp'][1]
	# kk = gpdict[g]['l'] * (polyinfo[midunit]['r'] - avgresistancemax)
	# if  writeline == "Total_avg_Resistance:  ":
			# writeline = writeline + str(kk) + "z"  + gpdict[g]['varid'] 
	# elif kk >0: 
		# writeline = writeline + " + " + str(kk) + "z" + gpdict[g]['varid'] 
	# elif kk < 0:
		# writeline = writeline  + str(kk) + "z" + gpdict[g]['varid'] 
	# if len(writeline) >50:
		# fw.write(writeline + '\n')
		# writeline = ''
# writeline = writeline + " <= 0\n"
# fw.write(writeline)

#total ground lichen
writeline = "G_Lichen_Const:  "
for g in gpdict:
	id = gpdict[g]['gp'][1]
	if polyinfo[id]['g'] > 0:
		if writeline == "G_Lichen_Const:  ":
			writeline = str(polyinfo[id]['g']*polyinfo[id]['ha']) + "z" + gpdict[g]['varid']  
		else:
			writeline = writeline + " + " + str(polyinfo[id]['g']*polyinfo[id]['ha']) + "z" + gpdict[g]['varid'] 
		count = count +1
		if len(writeline) > 50:
			fw.write(writeline + "\n")
			writeline = ""
writeline = writeline + " >= " + str(gtot*0.20)	
fw.write(writeline + '\n')
print "G Lich must be at least "  + str(gtot*0.20)


#total tree lichen
writeline = "T_Lichen_Const:  "
for g in gpdict:
	id = gpdict[g]['gp'][1]
	if polyinfo[id]['t'] > 0:
		if writeline == "G_Lichen_Const:  ":
			writeline = str(polyinfo[id]['t']*polyinfo[id]['ha']) + "z" + gpdict[g]['varid']  
		else:
			writeline = writeline + " + " + str(polyinfo[id]['t']*polyinfo[id]['ha']) + "z" + gpdict[g]['varid'] 
		count = count +1
		if len(writeline) > 50:
			fw.write(writeline + "\n")
			writeline = ""
writeline = writeline + " >= " + str(ttot*0.20)	
fw.write(writeline + '\n')
print "T Lich must be at least "  + str(ttot*0.20)


# #poly clust consts
f = open("C:/rstjohn/SLU_Exp/cluster_constraints.txt")
for line in f:
	fw.write(line)
f.close()


# for p in polyinclust:
	# if p % 500 == 0:
		# print "On cluster constraint  for poly " + str(p)
	# temparr=[[],[],[]]
	# for g in gpdict:
		# for m in range(0, 3):
			# if gpdict[g]["gp"][m] in polyinclust[p] and gpdict[g]["gp"][m] not in temparr[m]:
				# temparr[m].append(gpdict[g]['varid'] )
	# for m in range(0, 3):
		# writeline = "XX"
		# for k in temparr[m]:
			# if writeline == "XX":
				# writeline = "Clust_Const_" + str(m) + "_" + str(p) + ":   z" + k
			# else:
				# writeline = writeline + " + z" + k
			# if len(writeline) > 50:
				# fw.write(writeline + "\n")
				# writeline = ""
		# if writeline != "XX":
			# writeline = writeline + " <= 1\n"
			# fw.write(writeline)
        
# print("cluster constraints written")



#nonneg y
for g in gpdict:
	writeline = "Nonneg_y_" + gpdict[g]['varid']  +":   y" + gpdict[g]['varid']  + ">=0"
	fw.write(writeline + "\n")
fw.write("Nonneg_t0:  t0>=0 \n")


# #binary
fw.write('\nBinary\n')
writeline = ""
for g in gpdict:
	writeline = writeline + '\t' + "z" + gpdict[g]['varid'] 
	if len(writeline) > 50:
		fw.write(writeline + '\n')
		writeline = ""
		
fw.write('\n\nEnd')

fw.close()
print "End of SLU CC LP writer"