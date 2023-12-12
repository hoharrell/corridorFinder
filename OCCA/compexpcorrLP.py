####Wildlife Corridor LP Writer Program ####
#summary
#inputs:    polygon ids, ages, areas, triplet widths, 
#           and adjacencies .txt files
#outputs:   CPLEX LP for max min corridor width st:budget

###################### define and read in data ##########################
print "Starting CC LP Writer."
# import polycode
from compexpdata import *
import sys
import time
# import ast

###### Get poly ids, areas and clusters ###############

myM = 1.0   #arbitrary large number
myBudget = 0.25 
maxLength = 1.8
summaryfile = "C:/rstjohn/Comp_Exps/corrLPformulationsummary.txt"

print "writing corr LPs"
xx = 0
for hhh in dd['num_units']:
	for iii in dd['area_var']:
		for ggg in dd['deg_adj']:
			for jjj in ['1', '2', '3', '4', '5']: 
				mystr = "n"+hhh + "_deg" + ggg + "_area" + iii + "_" + jjj
				f = open(summaryfile)
				gotit = False
				for line in f:
					if mystr in line:
						gotit = True
						break
				f.close()
				if gotit:
					continue
				print mystr
				# fb = open('C:/rstjohn/Comp_Exps/gplpformsummary.txt')
				# isbad = False
				# for line in fb:
					# if mystr in line and "Bad" in line:
						# isbad = True
						# break
				# if isbad:
					# continue
				# fb.close()
				if mystr == "n600_deg55_area140_5":
					continue
				start_time = time.time()
				mypath = "C:/rstjohn/Comp_Exps/"+mystr+"/"
				myfolder = mypath  + "/gplps/"
				edgefile = "C:/rstjohn/Comp_Exps/landscapes/" + 'land' + "_" + mystr + '_land.csv'
				edgesdict, clusters, su, eu, triplets = getdata(edgefile)
				gpfile = "C:/rstjohn/Comp_Exps/" + mystr + "/gpwidthlengths.txt"
				lpfile = "C:/rstjohn/Comp_Exps/Corr_LPs/" + mystr + "_corrlp.lp"
				edgesdict, clusters, su, eu, triplets = getdata(edgefile)
				gpdict = getgpwidthlength(gpfile, su, eu)
				areadict = getareas(edgesdict)
				polyinclust = getpolyinclust(edgesdict, clusters)
				gates = getgates(gpdict)
				ff=open(lpfile, 'w')

				 # OBJECTIVE FUNCTION
				ff.write("MAX \nOBJECTIVE:\nv\n\nSubject to:\n")
				
				 # Budget constraint
				writeline="XX"
				cc=0
				currid=0
				currarea=0
				for g in gpdict:
					gparr = gpdict[g]["gp"]
					currid = gparr[1]
					currarea = areadict[currid]
					currstr = g
					if writeline=="XX":
						writeline="Budget_Const:   "+str(currarea)+"z"+g
					else:
						writeline=writeline+"+"+str(currarea)+"z"+g
					if len(writeline) > 60:
						ff.write(writeline+"\n")
						writeline=""
				writeline=writeline+"<="+str(myBudget)
				ff.write(writeline)
				# print "Budget constraint written"

				#Nonneg v Constraint
				ff.write("\nNonneg_v:     v>=0")

				#v def constraints
				for g in gpdict:
					mycoef = myM - float(gpdict[g]["w"])
					writeline = "\nv_def_" + g + ":   v + " + str(mycoef) + "z" + g + " <= " + str(myM)
					ff.write(writeline)
				# print "V def constraints written"
				# print su, eu
				# sys.exit()
				
				#BEGIN CORRIDOR
				writeline = "XX"
				for g in gpdict:
					gparr = gpdict[g]["gp"]
					if gparr[0] == su:
						if writeline == "XX":
							writeline = "\nBegin_Corridor_Const:    " + "z" + g
						else:
							writeline = writeline + " + z" + g
						if len(writeline) > 60:
							ff.write(writeline + "\n")
							writeline = ""
				if writeline == "XX":
					print "Error: no starting gates!"
				writeline = writeline + " = 1\n"
				ff.write(writeline)
				writeline = "XX"

				  
				#END CORRIDOR
				writeline = "XX"
				for g in gpdict:
					gparr = gpdict[g]["gp"]
					if gparr[2] == eu:
						if writeline == "XX":
							writeline = "End_Corridor_Const:    " + "z" + g
						else:
							writeline = writeline + " + z" + g
						if len(writeline) > 60:
							ff.write(writeline + "\n")
							writeline = ""
				if writeline == "XX":
					print "Error: no ending gates!"
				writeline = writeline + " = 1\n"
				ff.write(writeline)
				writeline = "XX"


				#NETWORK FLOW CONSTRAINTS
				writeline = "XX"
				kk = True
				for i in gates:
					if su != i[0] and eu != i[1]:
						gatestr = str(i[0]) + "_" + str(i[1]) + "_" + str(i[2])
						for x1 in gates[i]["in"]:
							if writeline == "XX": 
								writeline = "Flow_Const_" + gatestr + ":      z"+x1
							else:
								writeline = writeline + " + z" + x1
							if len(writeline) > 60:
								ff.write(writeline + "\n")
								writeline = ""
						for x2 in gates[i]["out"]:
							if writeline == "XX":
								writeline = "Flow_Const_" + gatestr + ":      z" + x2
							elif gates[i]["in"] == []:
								writeline = writeline + " + z" + x2
							else:
								writeline = writeline + " - z" + x2
							if len(writeline)> 60:
								ff.write(writeline + "\n")
								writeline = ""
						if writeline == "XX":
							print "ERROR IN NETFLOW!"
							break
						writeline = writeline + " = 0\n"
						ff.write(writeline)
						writeline = "XX"
				# print("WC constraints written")

				#CLUSTER CONSTRAINTS
				for p in polyinclust:
					for m in range(0, 3):
						templi=[]
						for g in gpdict:
							if gpdict[g]["gp"][m] in polyinclust[p] and gpdict[g]["gp"][m] not in templi:
								templi.append(g)
						writeline = "XX"
						for k in templi:
							if writeline == "XX":
								writeline = "Clust_Const_" + str(m) + "_" + str(p) + ":   z" + k
							else:
								writeline = writeline + " + z" + k
							if len(writeline) > 60:
								ff.write(writeline + "\n")
								writeline = ""
						if writeline != "XX":
							writeline = writeline + " <= 1\n"
							ff.write(writeline)
						
					
				#Length Constraint
				writeline = "Length_Constraint:    "
				for g in gpdict:
					if writeline ==  "Length_Constraint:    ":
						writeline = writeline + str(gpdict[g]['L']) + "z" + g
					else:
						writeline = writeline + "+" + str(gpdict[g]['L']) + "z" + g
					if len(writeline) > 60:
						writeline = writeline + "\n"
						ff.write(writeline)
						writeline = ""
				writeline = writeline + " <= " + str(maxLength) + "\n"
				ff.write(writeline)
				
				#BINARIES
				ff.write("\n\nBinary\n")
				writeline=""
				for g in gpdict:
					writeline = writeline + "     z" + g
					if len(writeline) > 60:
						ff.write(writeline + "\n")
						writeline = ""
				ff.write(writeline)

				ff.write("\nEnd")
				ff.close()
				end_time = time.time()
				
				#write summary file
				fw = open(summaryfile, 'a')
				line = mystr + ", "  + str(end_time-start_time) + ', ' + str(len(gpdict)) + '\n'
				fw.write(line)
				fw.close()

			