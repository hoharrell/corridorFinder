oldfile = "C:/rstjohn/maxnpv_fixed.cpx" 
newfile = "C:/rstjohn/6tps_maxnpv_full.cpx" 

fr = open(oldfile)
fw = open(newfile, 'w')

foundfixed = False
count = 0
for line in fr:
	if  "ixe" not in line:
		fw.write(line)
		# count = count + 1
	# if count == 20000:
		# break
fr.close()
fw.close()
		

