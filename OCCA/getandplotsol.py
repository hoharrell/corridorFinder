#get and plot solution
from polycode import *
from compexpdata import *
import matplotlib.pyplot as plt

hhh = 'area_var'
iii = '58'
jjj = '2'

mypath = "C:/rstjohn/Comp_Exps/"+hhh+"/"
print hhh, iii, jjj

if hhh == 'clust_size':
	edgefile = mypath + "landscapes/land_" + jjj + '_land.csv'
else:
	edgefile = mypath + "landscapes/land_" + iii + "_" + jjj + '_land.csv'
edgesdict, clusters, su, eu, triplets = getdata(edgefile, hhh, float(iii))
solfile = "C:/rstjohn/Comp_Exps/Corr_LPs/"+hhh +"_" + iii + "_" + jjj + "_corrsol.sol"
fs = open(solfile)
solpolys = []
for line in fs:
	if 'variable name="z' in line and 'value="1"' in line:
		# print line
		aa=line.split('z')
		bb = aa[1].split('"')
		cc = bb[0].split("_")
		polys = cc[0:2]
		for x in polys:
			p = int(x)
			plotpoly(edgesdict[p], 'k')
			if p not in solpolys:
				solpolys.append(p)
fs.close()
solpolys.sort()
print solpolys
plt.show()
		
		