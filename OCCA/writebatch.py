################################################################
##################### Triplet LP Batchfile Writer ########################
################################################################

import polycode
import os.path

#input: text files of polygon coordinates and triplets
#output: text files of gate pair LPs

triplets = polycode.triplets
print "Starting program"


count = 0
myfile="C:/rstjohn/SLU_Exp/SLU_gp_batch.txt"
ff = open(myfile,'w')
mypath = "C:/rstjohn/SLU_Exp/"
for t in triplets: 
	# print triplets.index(t)
	for i in range(0, 10):
		for j in range(0, 10):
			tripstr= str(t[0])+'_'+str(t[1])+'_'+str(t[2])+ "_" + str(i) + "_" + str(j)
			oldname =mypath +"2ha_GP_LPs/gplp"+ str(t[0]) + "_" + str(t[1]) + "_" + str(t[2]) + "_" + str(i) + "_" + str(j) + ".cpx"
			if os.path.isfile(oldname):
				count = count +1
				if count % 1000 == 0:
					print count
				writeline='set logfile ' + mypath + 'logs/gplp'+tripstr+'.log\n'
				ff.write(writeline)
				writeline = 'read ' + oldname + ' lp\n'
				ff.write(writeline)
				ff.write('Mipopt\n')
				writeline = 'write ' + mypath + '/sols/gplpsol'+tripstr+'.cpx sol\n\n'
				ff.write(writeline)
ff.close()    
print "there are "+ str(count) + ' gate pairs total'
print "End of program"



