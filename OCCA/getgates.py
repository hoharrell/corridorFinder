gatefile = "C:/Users/rachel/Desktop/Work/WC_Stuff/El_Dorado_Exp/20ha_gates.txt"
gpfile = "C:/Users/rachel/Desktop/Work/WC_Stuff/El_Dorado_Exp/20ha_gp_width_length.txt"

gpdict = {}
gates = {}
count = 0
file=open(gpfile)
startunit=1363   #unit that can start the corridor
endunit=1364    #unit that can end the corridor

for line in file:
	count = count + 1
	print count    #89167
	strarr = line.split()
	gpkey = strarr[0]
	temparr = gpkey.split("_")
	gparr = []
	for i in temparr:
		gparr.append(int(i))
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
file.close()
fw=open(gatefile, 'w')
for g in gates:
	writeline = str(g) + ";" + str(gates[g]['in']) + ";" + str(gates[g]['out']) +"\n"
	fw.write(writeline)
fw.close()


# file=open("C:/Users/rachel/Desktop/gp_width_length.txt")
# for line in file:
	# strarr = line.split()
	# gpkey = strarr[0]
	# gpw = float(strarr[1])
	# gpl = float(strarr[2])
	# temparr = gpkey.split("_")
	# gparr = []
	# for i in temparr:
		# gparr.append(int(i))
	# if gparr[1] not in [startunit, endunit]:
		# if gparr[0] != endunit  and gparr[2] != startunit:
			# gpdict[gpkey]= {"gp":gparr, "w": gpw, "l": gpl}
		# if gparr[0]!= startunit and gparr[2] != endunit:
			# gparr2 = [gparr[2], gparr[1], gparr[0], gparr[4], gparr[3]]
			# gpkey2 = ""
			# for i in gparr2:
				# if gpkey2 == "":
					# gpkey2 = str(i)
				# else:
					# gpkey2 = gpkey2 + "_" +str(i)
			# gpdict[gpkey2]= {"gp":gparr2, "w": gpw, "l": gpl}
# file.close()

# print "writing file..."

# newf = open("C:/Users/rachel/Desktop/gps.txt", 'w')
# for g in gpdict:
	# writeline = g + ";" + str(gpdict[g]["gp"]) + ";" + str(gpdict[g]["w"]) + ";" + str(gpdict[g]["l"]) + '\n'
	# newf.write(writeline)
# newf.close
# import polycode
# triplets = polycode.triplets
# clusters = polycode.clusters
# polyids = []
# for t in triplets:
	# for i in t:
		# if i not in polyids:
			# polyids.append(i)
# polyids.sort()
# count = 0
# newf = open("C:/Users/rachel/Desktop/polyclust.txt", 'w')
# for p in polyids:
	# count = count + 1
	# print count
	# if p not in clusters.keys():
		# clustlist=[]
		# for c in clusters:
			# if p in clusters[c]:
				# clustlist.append(c)
		# writeline = str(p)
		# for i in clustlist:
			# writeline = writeline + "    " + str(i)
		# writeline = writeline + "\n"
		# newf.write(writeline)
# newf.close()

print "END"