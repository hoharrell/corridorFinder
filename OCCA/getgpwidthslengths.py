print "Starting code"

import os.path
import polycode

#get gp widths, lengths
su = polycode.startunit
eu = polycode.endunit
triplets = polycode.triplets
myfile="C:/rstjohn/SLU_Exp/gp_width_length.txt"
fw = open(myfile,'w')
mypath = "C:/rstjohn/SLU_Exp/sols/"
count = 0
for t in triplets: 
	for i in range(0, 10):
		for j in range(0, 10):
			gpstr= str(t[0])+'_'+str(t[1])+'_'+str(t[2])+ "_" + str(i) + "_" + str(j)
			gpstr2 = str(t[2])+'_'+str(t[1])+'_'+str(t[0])+ "_" + str(j) + "_" + str(i)
			solfile = mypath + "gplpsol" + gpstr + ".cpx"
			if os.path.isfile(solfile):
				count = count + 1
				if count % 1000 == 0:
					print "On gp "+str(count)
				mywidth = ""
				mylen = ""
				ff=open(solfile)
				for line in ff:
					if 'objectiveValue' in line:
						temparr=line.split('"')
						mywidth=temparr[1]
					if '<variable name='  in line and 'L' in line:
						temparr=line.split('"')
						mylen = temparr[5]
					if mywidth != "" and mylen != "":
						writeline = gpstr + "   " + mywidth + "    " + mylen+"\n"
						fw.write(writeline)
						if t[0] != su and t[2] != eu:
							count = count + 1
							writeline = gpstr2 + "   " + mywidth + "    " + mylen+"\n"
							fw.write(writeline)
						break
				ff.close()
fw.close()

print("End of Code")
