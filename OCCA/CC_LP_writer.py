####Wildlife Corridor LP Writer Program ####
#summary
#inputs:    polygon ids, ages, areas, triplet widths, 
#           and adjacencies .txt files
#outputs:   CPLEX LP for max min corridor width st:budget

###################### define and read in data ##########################
print "Starting CC LP Writer."
import polycode
# import ast

###### Get poly ids, areas and clusters ###############
gpfile = "C:/Users/rachel/Desktop/Work/WC_Stuff/El_Dorado_Exp/20ha_gp_width_length.txt"
areafile = "C:/Users/rachel/Desktop/Work/WC_Stuff/El_Dorado_Exp/El_Dorado_acres.txt"
lpfile = "C:/Users/rachel/Desktop/Work/WC_Stuff/El_Dorado_Exp/20ha_CC_LP.cpx"

su = polycode.startunit  #unit that can start the corridor
eu = polycode.endunit  #unit that can end the corridor
myM = 10000   #arbitrary large number
myBudget = 7380 #roughly 15% of 49195.18 acres of total area
polygons = polycode.polygons
clusters = polycode.clusters
polyids = polygons.keys()
polyids.sort()

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


print "Getting data..." 

#get areas
polyareas={}       #dict of poly ids and areas
file=open(areafile)
for line in file:
    strarr=line.split()
    temp=int(strarr[0])
    temparea=float(strarr[1])
    if temp in polygons:
		polyareas[temp] = temparea
file.close()
for i in clusters:
    temparea = 0
    for j in clusters[i]:
        temparea = temparea+polyareas[j]
	polyareas[i] = temparea

#get dicts of clusters poly is in	
polyinclust = {}	
for p in polygons:
	if p in clusters:
		continue
	templi = [p]
	for c in clusters:
		if p in clusters[c]:
			templi.append(c)
	if len(templi) > 1:
		polyinclust[p] = templi

# get gps, widths, lengths, gates #
gpdict = {}
gates = {}
gpf=open(gpfile)
for line in gpf:
	strarr = line.split()
	gpkey = strarr[0]
	temparr = gpkey.split("_")
	gparr = []
	clust = False
	for i in temparr:
		gparr.append(int(i))
	getgates(gparr)
	gpdict[gpkey]= {"gp": gparr, 'w': float(strarr[1]), 'l': float(strarr[2])}

	
		
	
gpf.close()

# print gates



print "Got data.  Writing program."
print len(gates)
print len(gpdict)
print len(polyareas)
print len(polygons)


# ############################ write LP ##############################
print "Writing LP"
ff=open(lpfile, 'w')


 # OBJECTIVE FUNCTION
ff.write("MAX \nOBJECTIVE:\nv\n\nSubject to:\n")
print("Objective written")

 # Budget constraint
writeline="XX"
cc=0
currid=0
currarea=0
for g in gpdict:
	gparr = gpdict[g]["gp"]
	currid = gparr[1]
	currarea = polyareas[currid]
	currstr = g
	if writeline=="XX":
		writeline="Budget_Const:   "+str(currarea)+"z"+g
	else:
		writeline=writeline+"+"+str(currarea)+"z"+g
	cc=cc+1
	if cc>4:
		ff.write(writeline+"\n")
		writeline=""
		cc=0
writeline=writeline+"<="+str(myBudget)
ff.write(writeline)
print "Budget constraint written"


#Nonneg v Constraint
ff.write("\nNonneg_v:     v>=0")

#v def constraints
for g in gpdict:
	mycoef = myM - gpdict[g]["w"]
	writeline = "\nv_def_" + g + ":   v + " + str(mycoef) + "z" + g + " <= " + str(myM)
	ff.write(writeline)
print "V def constraints written"

#BEGIN CORRIDOR
writeline = "XX"
cc = 0
for g in gpdict:
	gparr = gpdict[g]["gp"]
	if gparr[0] == su:
		if writeline == "XX":
			writeline = "\nBegin_Corridor_Const:    " + "z" + g
			cc = cc + 1
		else:
			writeline = writeline + " + z" + g
			cc = cc + 1
		if cc > 5:
			ff.write(writeline + "\n")
			writeline = ""
			cc = 0
if writeline == "XX":
	print "Error: no starting gates!"
writeline = writeline + " = 1\n"
ff.write(writeline)
writeline = "XX"

  
  
#END CORRIDOR
writeline = "XX"
cc = 0
for g in gpdict:
	gparr = gpdict[g]["gp"]
	if gparr[2] == eu:
		if writeline == "XX":
			writeline = "End_Corridor_Const:    " + "z" + g
			cc = cc + 1
		else:
			writeline = writeline + " + z" + g
			cc = cc + 1
		if cc > 5:
			ff.write(writeline + "\n")
			writeline = ""
			cc = 0
if writeline == "XX":
	print "Error: no ending gates!"
writeline = writeline + " = 1\n"
ff.write(writeline)
writeline = "XX"


#NETWORK FLOW CONSTRAINTS
writeline = "XX"
count = 0
cc = 0
kk = True
for i in gates:
	if su != i[0] and eu != i[1]:
		gatestr = str(i[0]) + "_" + str(i[1]) + "_" + str(i[2])
		for x1 in gates[i]["in"]:
			if writeline == "XX": 
				writeline = "Flow_Const_" + gatestr + ":      z"+x1
			else:
				writeline = writeline + " + z" + x1
			cc = cc + 1
			if cc > 6:
				ff.write(writeline + "\n")
				writeline = ""
				cc = 0
		for x2 in gates[i]["out"]:
			if writeline == "XX":
				writeline = "Flow_Const_" + gatestr + ":      z" + x2
			elif gates[i]["in"] == []:
				writeline = writeline + " + z" + x2
			else:
				writeline = writeline + " - z" + x2
			cc = cc + 1
			if cc > 6:
				ff.write(writeline + "\n")
				writeline = ""
				cc = 0  
		if writeline == "XX":
			print "ERROR IN NETFLOW!"
			break
		writeline = writeline + " = 0\n"
		ff.write(writeline)
		count = count+1
		writeline = "XX"
print("WC constraints written")

#CLUSTER CONSTRAINTS
count = 0
for p in polyinclust:
	count = count + 1
	if count == 50:
		count = 0
		print "On cluster constraint  for poly " + str(p)
	for m in range(0, 3):
		templi=[]
		for g in gpdict:
			if gpdict[g]["gp"][m] in polyinclust[p] and gpdict[g]["gp"][m] not in templi:
				templi.append(g)
		writeline = "XX"
		cc = 0
		for k in templi:
			if writeline == "XX":
				writeline = "Clust_Const_" + str(m) + "_" + str(p) + ":   z" + k
			else:
				writeline = writeline + " + z" + k
			cc = cc + 1
			if cc > 6:
				ff.write(writeline + "\n")
				writeline = ""
				cc = 0
		if writeline != "XX":
			writeline = writeline + " <= 1\n"
			ff.write(writeline)
        
print("cluster constraints written")
        

#BINARIES
ff.write("\n\nBinary\n")
writeline=""
for g in gpdict:
	writeline = writeline + "     z" + g
	cc = cc + 1
	if cc > 4:
		ff.write(writeline + "\n")
		writeline = ""
		cc = 0
ff.write(writeline)

ff.write("\nEnd")
print("LP successfully written. Yay!")
ff.close()