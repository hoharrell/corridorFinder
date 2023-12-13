#read in parcel data, stand data
# import polycode
#new file: myid  origid   ha   amnt_g_lich    t_lich    resistance
# import polycode

# newf = "C:/rstjohn/SLU_Exp/trips_fixed.txt"
# # parcelf = "C:/rstjohn/SLU_Exp/parcel_data.txt"
# # standf = "C:/rstjohn/SLU_Exp/StandData.txt"
# # writef = "C:/rstjohn/SLU_Exp/landscape_data.txt"


# tripfile = "C:/rstjohn/SLU_Exp/SLU_2ha_trips.txt"

# su =3824
# eu = 3825
# #get triplets
# triplets = []
# ff=open(tripfile)
# fw = open(newf, 'w')
# count = 0
# last = 0
# for line in ff:
	# s = line.split()
	# temptrip = [int(s[0]), int(s[1]), int(s[2])] 
	# if temptrip[0] == eu or temptrip[1] == eu or temptrip[1] == su or temptrip[2] == su:
		# count = 0
	# else:
		# fw.write(line)
# ff.close() 
# fw.close


# pdict = {}
# f = open(parcelf)
# for line in f:
	# if "ha" in line:
		# continue
	# strli = line.split()
	# pdict[int(strli[0])] = {}
	# pdict[int(strli[0])]['orig_id'] = int(strli[1])
	# pdict[int(strli[0])]['ha'] = float(strli[2])
# f.close()

# sdict = {}
# f = open(standf)
# for line in f:
	# if "StandId" in line:
		# continue
	# strli = line.split(",")
	# sdict[int(strli[0])] = {}
	# if float(strli[10]) <0.5:
		# sdict[int(strli[0])]['g'] = float(strli[10])
	# else:
		# sdict[int(strli[0])]['g'] = 0.5
	# sdict[int(strli[0])]['t'] = float(strli[9])
	# sdict[int(strli[0])]['r'] = float(strli[11])
# f.close()

# ids = pdict.keys()
# ids.sort()

# f = open(writef, 'w')

# for i in ids:
	# origid = pdict[i]['orig_id']
	# if origid in sdict:
		# writeline = str(i) + "\t" + str(pdict[i]['ha']) + "\t" + str(sdict[origid]['g']*pdict[i]['ha'])+ "\t" + str(sdict[origid]['t']* pdict[i]['ha'])+ "\t" + str(sdict[origid]['r']) + "\n"
	# else:
		# writeline = str(i) + "\t" + str(pdict[i]['ha']) + "\t 0.00 \t 0 \t 0.00 \n" 
	
	# f.write(writeline)

# clusters = polycode.clusters
# for c in clusters:
	# area = 0.0
	# t = 0.0
	# g = 0.0
	# r = 0.0
	# for i in clusters[c]:
		# origid = pdict[i]['orig_id']
		# if origid in sdict:
			# area = area + pdict[i]['ha']
			# t = t + sdict[origid]['t']* pdict[i]['ha']
			# g = g +sdict[origid]['g']*pdict[i]['ha']
			# r = r + sdict[origid]['r']*pdict[i]['ha']
		# else:
			# area = area + pdict[i]['ha']
	# writeline = str(c) + '\t' + str(area) + "\t" + str(g) + '\t' + str(t)  + '\t' + str(r/area) + '\n'
	# f.write(writeline)
	
# f.close()