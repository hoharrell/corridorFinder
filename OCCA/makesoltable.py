# #make GIS table
solfile = "C:/rstjohn/SLU_Exp_Results/11tps_maxnpv_nocorr_sol.sol"
tablefile = "C:/rstjohn/SLU_Exp_Results/11tps_maxnpv_nocorr_sol_table.txt"

from getCCdata import *

tps = range(0, 11)

print "getting sol"
solrxs = {}
corridors = {}
for t in tps:
	corridors[t] = []
solf = open(solfile)
for line in solf:
	if 'variable name="'  in line: 
		temparr = line.split('"')
		# print temparr
		tempval = float(temparr[-2])
		myi = temparr[1]
		if 'z' in temparr[1] and tempval > 0.1:
			myi = temparr[1]
			myi = myi.replace('z', '')
			myi2 = myi.split('_')
			gp = myi2[0] +"_" + myi2[1]+"_" + myi2[2]+"_" + myi2[3]+"_" + myi2[4]
			myt = int(myi2[5])
			myunit = int(myi2[1])
			if myunit > eu:
				for c in clusters[myunit]:
					corridors[myt].append(c)
			else:
				corridors[myt].append(myunit)
		if 'x' in temparr[1] and tempval > 0.1:
			myi = temparr[1]
			myi = myi.replace('x', '')
			myi2 = myi.split("_")
			solrxs[int(myi2[0])] = int(myi2[1])
		
solf.close()


print "writing table"

ff = open(tablefile, 'w')
ff.write("MyID\tTIME\tRESISTANCE\tG_LICH\tT_Lich\tCORR\n")

for p in polygons:
	if p not in clusters:
		for tp in tps: 
			if origidforpoly[p] in harvdict:
				unit = origidforpoly[p]
				rx = solrxs[unit]
				myr = harvdict[unit][rx][tp]['r']
				myg = harvdict[unit][rx][tp]['g']
				myt = harvdict[unit][rx][tp]['t']
				# if myg != 0:
					# print "got one"
			else:
				myr = 0
				myg = 0
				myt = 0
			if p in corridors[tp]:
				incorr = 1
			else:
				incorr = 0
			writeline = str(p) + "\t" + str(tp) +"\t" + str(myr) + "\t" + str(myg) +"\t" + str(myt) +"\t" + str(incorr) +"\n"		
			ff.write(writeline)

ff.close()

# solfile = "C:/rstjohn/SLU_Exp/LPs/corr_sol_0_to_2.cpx"
# writefile = "C:/rstjohn/SLU_Exp/LPs/fixed_corr.txt"
# # Fix sol  
# fa = open(solfile)
# fw = open(writefile, 'w')
# for line in fa:
	# if '<variable name="x'  in line and 'value="1"' in line:
		# temparr = line.split('"')
		# writeline = "Fixed_" + temparr[1] + ":    " + temparr[1] + " = 1\n"
		# fw.write(writeline)
	# if ('name="z' in line or 'name="y' in line) and 'value="0"' not in line:
		# temparr = line.split('"')
		# temparr2 = temparr[1].split('_')
		# if int(temparr2[-1]) < 3 and temparr[7] != '0':
			# writeline = "Fixed_" + temparr[1] + ":    " + temparr[1] + " = " + temparr[7] + "\n"
			# # print writeline
			# fw.write(writeline)
		# # for t in tps:
			# # writeline = "Fixed_" + temparr[1] + str(t) + ":    " + temparr[1][:-1] + str(t) + " = " + temparr[7] + "\n"
			# # fw.write(writeline)			
# fa.close()
# fw.close()