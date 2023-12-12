lpfile = "C:/rstjohn/11tps_throwawaycpx" 
print "writing lp file " + lpfile


from getCCdata import *

print len(polygons)
print len(gpdict)
print len(harvdict)
myf = 0.15
gmin = 100
tmin = 40
# rtot = 2100
# revmin = 0
solfile = "C:/rstjohn/11tps_maxg_fixedx_05corr_sol1.sol"


# totalforestarea = 14133.92
print "writing file"
tps = range(0,11)
############################ Write LP #############################

fw = open(lpfile, 'w')

fw.write("MAX \nOBJECTIVE: \n")
writeline = "xx"

for i in harvdict:
	for rx in harvdict[i]:
		if writeline =="xx" and harvdict[i][rx]['npv'] != 0:
			writeline = str(harvdict[i][rx]['npv']) + "x" + harvdict[i][rx]['label']
		elif harvdict[i][rx]['npv'] > 0:
			writeline = writeline + " + " + str(harvdict[i][rx]['npv']) + "x" + harvdict[i][rx]['label']
		elif harvdict[i][rx]['npv'] < 0:
			writeline = writeline + str(harvdict[i][rx]['npv']) + "x" + harvdict[i][rx]['label']
		if len(writeline) > 50:
			fw.write(writeline + '\n')
			writeline = ""
fw.write(writeline + '\n')

print "Objective Written"

fw.write("\nSubject to:\n")
# ########### Harvest constraints #############################

# fw.write("Kmax:    K<=150\n")
# writeline = "Rev_Constraint:  "
# for i in harvdict:
	# for rx in harvdict[i]:
		# if writeline =="Rev_Constraint:  " and harvdict[i][rx]['npv'] != 0:
			# writeline = str(harvdict[i][rx]['npv']) + "x" + harvdict[i][rx]['label']
		# elif harvdict[i][rx]['npv'] > 0:
			# writeline = writeline + " + " + str(harvdict[i][rx]['npv']) + "x" + harvdict[i][rx]['label']
		# elif harvdict[i][rx]['npv'] < 0:
			# writeline = writeline + str(harvdict[i][rx]['npv']) + "x" + harvdict[i][rx]['label']
		# if len(writeline) > 70:
			# fw.write(writeline + '\n')
			# writeline = ""
# writeline = writeline + ' >= 18000000\n'
# fw.write(writeline)


# one rx constraint:
for i in harvdict:
	writeline = "One_RX_"+ str(i) + ":    "
	for rx in harvdict[i]:
		if writeline == "One_RX_"+ str(i) + ":    ":
			writeline = writeline + "x" + harvdict[i][rx]['label']
		else:
			writeline = writeline + " + x" + harvdict[i][rx]['label']
		if len(writeline) > 70:
			fw.write(writeline + '\n')
			writeline = ""
	writeline = writeline + " = 1\n"
	fw.write(writeline)

# from get5sol import rxdict
		
# # 5tp rxs:
# for i in rxdict:
	# writeline = "fivetp_sol_rxs_" + str(i) + ":   "
	# for rx in rxdict[i]:
		# if writeline == "fivetp_sol_rxs_" + str(i) + ":   ":
			# writeline = writeline + "x" + str(i) + "_" + str(rx)
		# else: 
			# writeline = writeline + " + x" + str(i) + "_" + str(rx)
		# if len(writeline) > 70:
			# fw.write(writeline + '\n')
			# writeline = ""
	# if writeline != "fivetp_sol_rxs_" + str(i) + ":   ":
		# writeline = writeline + " = 1\n"
		# fw.write(writeline)

#Harvest accounting
for t in range(1, len(tps)):
	writeline = "Harvest_" + str(t) + ":   "
	for i in harvdict:
		for rx in harvdict[i]:
			if harvdict[i][rx][t]['vol harvested'] >0.01:
				if writeline == "Harvest_" + str(t) + ":   ":
					writeline = writeline + str(harvdict[i][rx][t]['vol harvested']) + "x" + harvdict[i][rx]['label']
				else: 
					writeline = writeline + "+" + str(harvdict[i][rx][t]['vol harvested']) + "x" + harvdict[i][rx]['label']
				if len(writeline) > 50:
					fw.write(writeline + '\n')
					writeline = ""
	writeline = writeline + "- H" + str(t) + " = 0\n"
	fw.write(writeline)
	
#Min flow
for t in range(1, len(tps)-1):
	writeline = "Min_Flow_" + str(t) + ":   "+ str(1-myf) + "H" + str(t) + " - H" + str(t+1) + " <= 0" 
	fw.write(writeline + '\n')

# Max flow
for t in range(1, len(tps)-1):
	writeline = "Max_Flow_" + str(t) + ":   "+ str(1+myf) + "H" + str(t) + " - H" + str(t+1) + " >= 0" 
	fw.write(writeline + '\n')

	
	
# # Not too thick
# badr = []	
# writeline = "Nottoothick:  "
# for i in harvdict:
	# badrxs = []
	# for rx in harvdict[i]:
		# rxok = True
		# for t in tps:
			# if harvdict[i][rx][t]['r'] == 1:
				# rxok = False
		# if not rxok:
			# badrxs.append(rx)
	# if len(badrxs) == len(harvdict[i]):
		# badr.append(i)
	# elif badrxs != 0:
		# for b in badrxs:
			# if writeline == "Nottoothick:  ":
				# writeline = writeline + "x" +  harvdict[i][b]['label']
			# else:
				# writeline = writeline + " + x" +  harvdict[i][b]['label']
			# if len(writeline) > 70:
				# fw.write(writeline + '\n')
				# writeline = ""
# writeline = writeline + " = 0\n"
# fw.write(writeline)
	
# # Fix sol  
# fa = open(solfile)
# for line in fa:
	# if '<variable name="x'  in line and 'value="1"' in line:
		# temparr = line.split('"')
		# writeline = "Fixed_" + temparr[1] + ":    " + temparr[1] + " = " +temparr[-2]+ "\n"
		# fw.write(writeline)
	# # if 'name="z' in line or 'name="y' in line: # and temparr[-2] not in ('0', '-0'):
		# # temparr = line.split('"')
		# # if temparr[-2] not in ("-0", "0"):
			# # writeline = "Fixed_" + temparr[1] + ":    " + temparr[1] + " = " +temparr[-2]+ "\n"
			# # fw.write(writeline)
		# # # # for t in tps:
			# # # # writeline = "Fixed_" + temparr[1] + str(t) + ":    " + temparr[1][:-1] + str(t) + " = " + temparr[7] + "\n"
			# # # # fw.write(writeline)			
# fa.close()

# fb = open("C:/rstjohn/feascorrs010.txt")
# for line in fb:
	# fw.write(line)
# fb.close()
	
	
# print "Harvest Constraints Written"




# # # # # # # # # ##################### Corridor connectivity constraints #############
# tps = range(0,11)
# # # #start flow
# for t in tps:
	# writeline = "Start_Flow_" + str(t) + ":  " 
	# for g in gpdict:
		# if gpdict[g]['gp'][0] == su:
			# if writeline ==  "Start_Flow_" + str(t) + ":  " :
				# writeline = writeline + "z" + g + "_" + str(t)
			# else:
				# writeline = writeline + " + z" + g + "_" + str(t)
			# if len(writeline) > 70:
				# fw.write(writeline + "\n")
				# writeline = ""
	# writeline = writeline + " = 1 \n"
	# fw.write(writeline)

# #end flow
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

# # #Start commod Flow
# for t in tps:
	# writeline = "Start_y_Flow_" + str(t) + ":   "
	# for g in gpdict:
		# if gpdict[g]['gp'][0] == su:
			# if writeline == "Start_y_Flow_" + str(t) + ":   ":
				# writeline = writeline + "y" + g + "_" + str(t)
			# else:
				# writeline = writeline + " + y" + g + "_" + str(t)
			# if len(writeline) > 70:
				# fw.write(writeline + "\n")
				# writeline = ""
	# writeline = writeline + " <= " + str(len(harvdict)) + "\n"
	# fw.write(writeline)

		
# ## Flow Conservation
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
				
# # # static constraints
# # for t in tps:
	# # if t in (0, 60, 110, 16):
		# # continue
	# # for gp in gpdict:
		# # # writeline = "Static_z_"+ gp + "_" + str(t) + ":    z" + gp + "_" + str(t) + "-z" + gp + "_" + str(t-1) + " = 0\n"
		# # # fw.write(writeline)
		# # writeline = "Static_y_"+ gp + "_" + str(t) + ":    y" + gp + "_" + str(t) + "-y" + gp + "_" + str(t-1) + " = 0\n"
		# # fw.write(writeline)

			
# # writeline = "Bad_Rs_Const:   "
# # for g in gpdict:
	# # if g not in nfgp:
		# # midpol = gpdict[g]['gp'][1]
		# # if midpol not in clusters:
			# # unitli = [origidforpoly[midpol]]
		# # else:
			# # s = []
			# # unitli = []
			# # for a in clusters[midpol]:
				# # if origidforpoly[a] in harvdict:
					# # s.append(origidforpoly[a])
			# # for x in s:
				# # if x not in unitli:
					# # unitli.append(x)
		# # if [x for x in unitli if x in badr] != []:
			# # for t in tps:
				# # if writeline == "Bad_Rs_Const:   ":
					# # writeline = writeline + "z" + g+ "_" + str(t)
				# # else: 
					# # writeline = writeline + " + z" + g+ "_" + str(t)
				# # if len(writeline) > 70:
					# # fw.write(writeline + "\n")
					# # writeline = ""
# # writeline = writeline + " = 0\n"
# # fw.write(writeline)

# # # # # # # # ############ Lichen constraints #############################

# # # #g lich def consts
# pnog = []
# gpli = []
# for p in polygons:
	# if p not in nfu:
		# if p not in clusters :
			# unitli = [origidforpoly[p]]
		# else:
			# unitli = []
			# for a in clusters[p]:
				# if origidforpoly[a] in harvdict:
					# unitli.append(origidforpoly[a])
		# if [x for x in unitli if x in noglich] == unitli:
			# pnog.append(p)
			# continue
		# for t in tps:
			# writeline = "G_Lich_Def_1_" + str(p) + "_" + str(t) + ":    g" + str(p) + "_" + str(t)
			# for u in unitli:
				# for rx in harvdict[u]:
					# if  harvdict[u][rx][t]['g'] > 0:
						# writeline = writeline + " - " +str(areadict[u]  * harvdict[u][rx][t]['g'] ) + "x" +  harvdict[u][rx]['label']
					# if len(writeline) > 70:
						# fw.write(writeline + '\n')
						# # print writeline
						# writeline = ""
			# writeline = writeline + "< = 0\n"
			# # print writeline
			# fw.write(writeline)
			# writeline = "G_Lich_Def_2_" + str(p) + "_" + str(t) + ":    g" + str(p) + "_" + str(t)
			# for gp in midpolgpdict[p]:
				# if gpdict[gp]['gp'][1] == p:
					# writeline = writeline + " - " + str(polyarea[p]) + "z" + gp + "_" + str(t)
					# if len(writeline) > 70:
						# fw.write(writeline + '\n')
						# # print writeline
						# writeline = ""
			# writeline = writeline + " <= 0\n"
			# fw.write(writeline)
			# # print writeline
					

		

# # g accounting const	
# for t in tps:
	# writeline = "G_Lichen_Min_"+ str(t) +":  "
	# for p in polygons:
		# if p not in nfu and p not in pnog:
			# if writeline == "G_Lichen_Min_"+ str(t) +":  ":
				# writeline = writeline + "g" + str(p) + "_" + str(t)
			# else:
				# writeline = writeline + " + g" + str(p) + "_" + str(t)
			# if len(writeline) > 70:
				# fw.write(writeline + '\n')
				# # print writeline
				# writeline = ""
	# writeline = writeline + " >= " + str(gmin) + "\n"
	# # print writeline
	# fw.write(writeline)


# # #t lich def consts
# pnot=[]
# for p in polygons:
	# if p not in nfu:
		# if p not in clusters :
			# unitli = [origidforpoly[p]]
		# else:
			# unitli = []
			# for a in clusters[p]:
				# if origidforpoly[a] in harvdict:
					# unitli.append(origidforpoly[a])
		# totarea = polyarea[p]
		# if [x for x in unitli if x in notlich] == unitli:
			# pnot.append(p)
			# continue	
		# for t in tps:
			# writeline = "T_Lich_Def_1_" + str(p) + "_" + str(t) + ":    t" + str(p) + "_" + str(t)
			# for u in unitli:
				# for rx in harvdict[u]:
					# if  harvdict[u][rx][t]['t']  > 0:
						# writeline = writeline + " - " +str(areadict[u]  * harvdict[u][rx][t]['t'] ) + "x" +  harvdict[u][rx]['label']
					# if len(writeline) > 70:
						# fw.write(writeline + '\n')
						# writeline = ""
			# writeline = writeline + "< = 0\n"
			# fw.write(writeline)
			# writeline = "T_Lich_Def_2_" + str(p) + "_" + str(t) + ":    t" + str(p) + "_" + str(t)
			# for gp in midpolgpdict[p]:
				# if gpdict[gp]['gp'][1] == p:
					# writeline = writeline + " - " + str(polyarea[p]) + "z" + gp + "_" + str(t)
					# if len(writeline) > 70:
						# fw.write(writeline + '\n')
						# # print writeline
						# writeline = ""
			# writeline = writeline + " <= 0\n"
			# fw.write(writeline)



# # t accounting const	
# for t in tps:
	# writeline = "T_Lichen_Min_"+ str(t) +":  "
	# for p in polygons:
		# if p not in nfu and p not in pnot:
			# if writeline == "T_Lichen_Min_"+ str(t) +":  ":
				# writeline = writeline + "t" + str(p) + "_" + str(t)
			# else:
				# writeline = writeline + " + t" + str(p) + "_" + str(t)
			# if len(writeline) > 70:
				# fw.write(writeline + '\n')
				# # print writeline
				# writeline = ""
	# writeline = writeline + " >=  " + str(tmin) + "\n"
	# # print writeline
	# fw.write(writeline)

	
# print "lichen constraints written"

				
# #max gate flow
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

# # y defs
# for t in tps:
	# for gp in gpdict:
		# writeline = "Y_Def1_ " + gp + "_" + str(t) + ":   z"+ gp + "_" + str(t) +" - y" + gp + "_" + str(t) + " <= 0\n" 
		# fw.write(writeline)
		# writeline = "Y_Def2_ " + gp + "_" + str(t) + ":   y"+ gp + "_" + str(t) +" - " + str(len(harvdict)) + "z" + gp + "_" + str(t) + " <= 0\n" 
		# fw.write(writeline)
		# writeline= "Y_nonneg_"+ gp + "_" + str(t) + ":   y"+ gp + "_" + str(t) + " >= 0\n"
		# fw.write(writeline)		
# print "corridor connectivity constraints written"

# # clust consts
# tempdict = {}
# for g in gpdict:
	# if gpdict[g]['gp'][1] in clusters:
		# for a in clusters[gpdict[g]['gp'][1]]:
			# if a not in tempdict:
				# tempdict[a] = []
			# tempdict[a].append(g)
	# else:
		# if gpdict[g]['gp'][1] not in tempdict:
			# tempdict[gpdict[g]['gp'][1]] = []
		# tempdict[gpdict[g]['gp'][1]].append(g)
# for p in polygons:
	# if p not in tempdict:
		# continue
	# for t in tps:
		# writeline = "Clust_Combo_Const_" + str(p) + "_" + str(t)  + ":   "
		# for a in tempdict[p]:
			# if writeline == "Clust_Combo_Const_" + str(p) + "_" + str(t)  + ":   ":
				# writeline = writeline + "z" + a + "_" + str(t)
			# else:
				# writeline = writeline + " + z" + a + "_" + str(t)
			# if len(writeline) > 70:
				# fw.write(writeline + '\n')
				# writeline = ""
		# if p not in nfu:
			# if p not in clusters:
				# unitli = [origidforpoly[p]]
			# else:
				# unitli = []
				# for a in clusters[p]:
					# if origidforpoly[a] in harvdict and origidforpoly[a] not in unitli:
						# unitli.append(origidforpoly[a])
			# for u in unitli:
				# for rx in harvdict[u]:
					# if harvdict[u][rx][t]['r'] == 1:
						# writeline = writeline + " + x"+  harvdict[u][rx]['label']
						# if len(writeline) > 70:
							# fw.write(writeline + '\n')
							# writeline = ""
		# if writeline != "Clust_Combo_Const_" + str(p) + "_" + str(t)  + ":   ":
			# writeline = writeline + " <= 1\n"
			# fw.write(writeline)

# print "Cluster constraints written"			

# # ##No Impenetrable Units
# # for t in tps:
	# # for p in polygons:
		# # if p not in nfu:
			# # writeline = "NotImpenetrable_"+str(p)+"_"+str(t) +":    "
			# # for gp in midpolgpdict[p]:
				# # if gpdict[gp]['gp'][1] == p:
					# # if writeline == "NotImpenetrable_"+str(p)+"_"+str(t) +":    ":
						# # writeline = writeline +  "z" + gp + "_" + str(t)
					# # else:
						# # writeline = writeline +  " + z" + gp + "_" + str(t)
					# # if len(writeline) > 70:
						# # fw.write(writeline + '\n')
					# # writeline = ""
			# # if p not in clusters:
				# # unitli = [origidforpoly[p]]
			# # else:
				# # unitli = []
				# # for a in clusters[p]:
					# # if origidforpoly[a] in harvdict and origidforpoly[a] not in unitli:
						# # unitli.append(origidforpoly[a])
			# # for u in unitli:
				# # for rx in harvdict[u]:
					# # if harvdict[u][rx][t]['r'] == 1:
						# # writeline = writeline + " + x"+  harvdict[u][rx]['label']
						# # if len(writeline) > 70:
							# # fw.write(writeline + '\n')
						# # writeline = ""
			# # if writeline != "NotImpenetrable_"+str(p)+"_"+str(t) +":    ":
				# # writeline = writeline + " <= 1\n"
				# # fw.write(writeline)


# # ############## Resistance Constraints ########

# # for g in gpdict:
	# # if g not in nfgp:# and g not in badgp:
		# # midpol = gpdict[g]['gp'][1]
		# # if midpol not in clusters:
			# # unitli = [origidforpoly[midpol]]
		# # else:
			# # s = []
			# # unitli = []
			# # for a in clusters[midpol]:
				# # if origidforpoly[a] in harvdict:
					# # s.append(origidforpoly[a])
			# # for x in s:
				# # if x not in unitli:
					# # unitli.append(x)
		# # for t in tps:
			# # writeline = "R_Def_1_" +  g+"_" + str(t) + ":   r" + g +"_" + str(t) + " - 0.999999z" + g +"_" + str(t) + " <= 0\n"
			# # fw.write(writeline)	
			# # writeline = "R_def_2_" + g +"_" + str(t) + ":   z" + g +"_" + str(t)+ " - " + "r" + g +"_" + str(t)
			# # totxcoef = 0.0
			# # for u in unitli:
				# # if len(unitli) == 1:
					# # xcoef = 1
				# # else:
					# # xcoef =  areadict[u]  / polyarea[midpol]
					# # # print areadict[u]
					# # totxcoef = totxcoef + xcoef
				# # for rx in harvdict[u]:
					# # if harvdict[u][rx][t]['r'] > 1 or totxcoef > 1.1:
						# # print "My totcoef is too big!  totcoef: "+str(totxcoef) + "  ha: " + str(areadict[u] )+  "  totha: " + str(polyarea[midpol] )+"  resistance: " + str(harvdict[u][rx][t]['r'] )+ "  totarea: " + str(totarea )
						# # print unitli, midpol, g, t
						# # break
					# # writeline = writeline + " + " + str( harvdict[u][rx][t]['r'] * xcoef ) +  "x" +  harvdict[u][rx]['label']   #harvdict[u][rx][t]['r'] * gpdict[g]['l']
					# # #writeline = writeline + " + " + str( harvdict[u][rx][t]['r'] ) +  "x" +  harvdict[u][rx]['label']   #harvdict[u][rx][t]['r'] * gpdict[g]['l']
					# # if len(writeline) > 70:
						# # fw.write(writeline + '\n')
						# # writeline = ""
			# # writeline = writeline + " <= 1\n"
			# # fw.write(writeline)
					
# # # r tot constraint
# # for t in tps:
	# # print t
	# # writeline = "Resist_Total_" + str(t) + ":   "
	# # for g in gpdict:
		# # if g not in nfgp: # and g not in badgp:
			# # if writeline == "Resist_Total_" + str(t) + ":   ":
				# # writeline = writeline + str(gpdict[g]['l']) + "r"  + g +"_" + str(t)
			# # else:
				# # writeline = writeline + " + " + str(gpdict[g]['l']) + "r"  + g +"_" + str(t)
			# # if len(writeline) > 70:
				# # fw.write(writeline + '\n')
				# # writeline = ""
	# # writeline = writeline + "  - Rmax <= 0\n " # + str(rtot) + "\n"
	# # fw.write(writeline)
	
# # print "Resistance constraints written"

# ################ Variable Ranges ######################

# # # bounds
# fw.write("\nbounds\n")
# for p in polygons:
	# for t in tps:
		# if p not in nfu and p not in pnog:
			# writeline =  "0 <= g" + str(p) + "_" + str(t) + " <= " + str(polyarea[p]) + "\n"
			# fw.write(writeline)
		# if p not in nfu and p not in pnot:
			# writeline =  "0 <= t" + str(p) + "_" + str(t) + " <= " + str(polyarea[p]) + "\n"
			# fw.write(writeline)
			
			
# # # for g in gpdict:
	# # if g not in nfgp: # and g not in badgp:
		# # writeline = ""
		# # for t in tps:
			# # writeline = writeline + "0 <= r" +  g +"_" + str(t) +"< 1 \n"
		# # fw.write(writeline)
	
#binary x
fw.write('\nBinary\n')
writeline = ""
for i in harvdict:
	for rx in harvdict[i]:
		writeline = writeline + '\tx' + harvdict[i][rx]['label']
		if len(writeline) > 70:
			fw.write(writeline + '\n')
			writeline = ""
fw.write(writeline)
			
# for gp in gpdict:
	# for t in tps:
		# writeline = writeline + '\tz' + gp + "_" + str(t)
		# if len(writeline) > 70:
			# fw.write(writeline + '\n')
			# writeline = ""
# fw.write(writeline + '\n')
			

fw.write('\n\nEnd')

fw.close()
# fa = open(lpfile)
# for line in fa:
	# if "v" in line and "vation" not in line:
		# print line
# fa.close()
print "End of SLU Harvest LP writer"