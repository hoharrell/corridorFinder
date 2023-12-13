### fxns that take a triplet an writes associated gate pair LPs**.

print "Starting gatefinder"


import polycode
import gplp_foos
import copy
import multiprocessing
import time
import os.path
import stopit
import matplotlib.pyplot as plt

@stopit.threading_timeoutable(default='not finished')
def foo1(x):
	t = triplets[x]
	# print t
	newf = "C:/rstjohn/SLU_Exp/running/"+str(t[0])+"_"+str(t[1])+"_"+str(t[2])+".txt"
	errf = "C:/rstjohn/SLU_Exp/errors/error_"+str(t[0])+"_"+str(t[1])+"_"+str(t[2])+".txt"
	contf = "C:/rstjohn/SLU_Exp/2ha_GPs_contained/contained_"+str(t[0])+"_"+str(t[1])+"_"+str(t[2])+".txt"
	gatef = "C:/rstjohn/SLU_Exp/2ha_GPs_nogate/nogate_"+str(t[0])+"_"+str(t[1])+"_"+str(t[2])+".txt"
	intf = "C:/rstjohn/SLU_Exp/gates_intersect/gatesint_"+str(t[0])+"_"+str(t[1])+"_"+str(t[2])+".txt"
	mypath = "C:/rstjohn/SLU_Exp/2ha_GP_LPs/"
	kk = 0
	if os.path.isfile(newf) or  os.path.isfile(errf) or  os.path.isfile(contf) or  os.path.isfile(gatef) : #or os.path.isfile(intf):
		return 0
	print "On triplet "+str(t)+", which is number "+ str(x)  + " out of "+str(len(triplets))+" triplets."
	try:
		kk = gplp_foos.writeGPLPs(t, mypath)
	except:
		print "Except ERROR triplet "+str(t)+", which is number "+ str(x) 
		ff = open(errf, 'w')
		ff.write(str(x)+'\n')
		ff.close()
		return 9
	if kk == 9:
		print "ERROR triplet "+str(t)+", which is number "+ str(x) 
		ff = open(errf, 'w')
		ff.write(str(x)+'\n')
		ff.close()
		return 9
	elif kk == 2:
		ff = open(contf, 'w')
		ff.write(str(x)+'\n')
		ff.close()
		return 2
	elif kk == 4:
		ff = open(intf, 'w')
		ff.write(str(x) + '\n')
		ff.close()
		return 4
	elif kk == 3:
		ff = open(gatef, 'w')
		ff.write(str(x)+'\n')
		ff.close()
		return 3
	else:
		ff = open(newf, 'w')
		ff.write(str(x)+'\n')
		ff.close()
		return 0

su = polycode.startunit
eu = polycode.endunit
triplets = polycode.triplets
i = range(0, len(triplets))	
d = polycode.polygons
print len(triplets)
print "Starting parallel"


# if __name__ == '__main__':
	# i=polycode.polygons.keys()
	# pool = Pool(7)	
	# writingLPs = pool.map(foo1, i) 
inds = range(0, len(triplets))
	
# # if __name__ == '__main__':
    # # Start bar as a process
	# for j in range(0, len(triplets)):
		# # print "j is "+str(j)
		# p = multiprocessing.Process(target = foo1, args = (j, ))
		# p.start()
		# # Wait for 20 seconds or until process finishes
		# p.join(20)
		# # If thread is still active
		# if p.is_alive():
			# print "running... let's kill it..."
			# # Terminate
			# p.terminate()
			# p.join()


		
		
for j in range(0, len(triplets)):
	# a = foo1(j)
	result = foo1(j, timeout=20)
	if result == 'not finished':
		t = triplets[j]
		errf = "C:/rstjohn/SLU_Exp/errors/error_"+str(t[0])+"_"+str(t[1])+"_"+str(t[2])+".txt"
		print "Timeout on triplet "+str(t)+", which is number "+ str(x) 
		ff = open(errf, 'w')
		ff.write(str(x)+'\n')
		ff.close()

# t = triplets[3477] 
# print t
# t = [ 357, 355, 3414]
# d1 = copy.deepcopy(d[t[0]])
# d2 = copy.deepcopy(d[t[1]])
# d3 = copy.deepcopy(d[t[2]])
# polycode.plotpoly(d1, 'r')
# polycode.plotpoly(d2, 'g')
# polycode.plotpoly(d3, 'b')
# g23= polycode.findgates(d2, d3)
# g12 = polycode.findgates(d1, d2)
# for i in g23+g12:
	# x = [i[0][0], i[1][0]]
	# y = [i[0][1], i[1][1]]
	# plt.plot(x, y, 'k')
# print g12
# print g23
# plt.show()
# newp = polycode.correspondingpoly(d1, d2, d3, g12, g23)
# print  gplp_foos.writeGPLPs(t, "C:/rstjohn/SLU_Exp/2ha_GP_LPs/")
# if newp != {}:
	# print "p not empty!"
	# polycode.plotpoly(newp, 'k')
	# plt.show()

print "End of gatefinder"