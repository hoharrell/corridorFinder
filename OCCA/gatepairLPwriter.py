
################################################################
##################### Gate Pair LP Writer ########################
################################################################




################################################################
#input: text files of polygon coordinates and triplets
#output: text files of triplet LPs

print "Starting program"

import foos
import time
import polycode
start_time = time.time()


simptime = 0
opttime = 0

polydict = polycode.polygons
ids = polydict.keys()

for i in ids:
	foos.LPWriter


i = range(100)

if __name__ == '__main__':
	pool = Pool(2)	
	pool.map(f, i) 
	
for t in range(0,  10):
	print "Starting on triplet "+str(t)+" of "+str(len(triplets)) + " , " + str(triplets[t])
	if fxns.ispolycontained(polygons[triplets[t][0]], polygons[triplets[t][1]], polygons[triplets[t][2]]):
		print str(triplets[t])+" has a contained poly."
	elif [x for x in triplets[t] if x in badpolys] == [] :
		r = fxns.LPwriter(polygons[triplets[t][0]], polygons[triplets[t][1]], polygons[triplets[t][2]])
		if r != 0:
			print "ERROR!!! At triplet "+str(triplets[t])
			break
	else:
		print "Triplet contained bad polygon.  Skipping."
	currtime = time.time() - start_time
	print "Current run time is %g seconds" % currtime

	
	
# print 'writing file'
# outfile = "C:/Users/rachel/Desktop/weirdtrips"+str(t[0])+"_"+str(t[1])+"_"+str(t[2])+".cpx"
# ff = open(outfile, 'w')
# ff.write("Disjoint:\n ")
# ff.write(disjointli)     
# ff.write("Holes\n ")
# ff.write(holeli)     
# ff.close()          
# print "file written.  check it out."
    
    # if ispolycontained(polygons[triplets[t][0]], polygons[triplets[t][1]], polygons[triplets[t][2]]):
        # print str(triplets[t])+" has a contained poly."
    # else:
        # r = LPwriter(triplets[t], polygons)
        # if r != 0:
            # print "ERROR!!!"
            # break
    # currtime = time.time() - start_time
    # print "Current run time is %g seconds" % currtime


#TROUBLESHOOTING   TTTTTT 
# t = triplets[31928]
# print t
# # print ispolycontained(polygons[t[0]], polygons[t[1]], polygons[t[2]])
# plotpoly(polygons[t[0]], 'g')
# plotpoly(polygons[t[1]], 'r')  
# plotpoly(polygons[t[2]], 'b')
# plt.show()  
# LPwriter(polygons[t[0]], polygons[t[1]], polygons[t[2]])
# a,b,c = preprocesstriplet(polygons[t[0]], polygons[t[1]], polygons[t[2]])
# tris = gettris(b)
# adjs = []
# for t1 in tris:
		# for t2 in tris:
			# for e1 in tris[t1]:
				# for e2 in tris[t2]:
					# if ifwithin(e1, e2) and t1 != t2:
						# # adjs.append([t1, t2])
# print adjs
# subtrips = getsubtrips(tris, a, c)  #subtrips
# print subtrips
# a, bn = simplifyedge(polygons[t[0]], polygons[t[1]])
# b, c = simplifyedge(bn, polygons[t[2]])
# print ispolydisjoint(b['edges'])
# a,b,c = newfixdisjoint(a, bn, polygons[t[2]])
# plotpoly(a, 'g')
# plotpoly(b, 'r')  
# plotpoly(c, 'b')
# print ispolydisjoint(b['edges'])
# plt.show()
# face = triangle.get_data('face')
# print face['holes']
# plot.plot(ax1, **face)
# print face
# tris = gettris(b)
# for i in tris:
	# currtri = tris[i]
	# for e in currtri:
		# x = [e[0][0], e[1][0]]
		# y = [e[0][1], e[1][1]]
		# plt.plot(x,y, 'k')
# plotpoly(a, 'r')  
# plotpoly(b, 'k')
# plotpoly(c, 'b')
# plt.show()

	
# a, bn = simplifyedge(polygons[t[0]], polygons[t[1]])
# b, c = simplifyedge(bn, polygons[t[2]])

# if ispolydisjoint(b['edges']):
   # print "disjoint.  fixing..."
   # a,b,c = fixdisjoint(a, b, c)
# for e in b['edges']:
	# if e in a['edges']:
		# print "shared edge with a"
	# if e in c['edges']:
		# print "shared edge with c"
# plotpoly(a, 'k')
# plotpoly(b, 'g')
# plotpoly(c, 'b')
# plt.show()
 

#subwidths = getsubwidths(tris, subtrips)
#sublengths = getsublengths(tris, subtrips)

#plt.axis([712620, 712650, 4296900, 4297280])
# plt.show()
end_time = time.time()
print("Elapsed time was %g seconds" % (end_time - start_time))

print "End of program"


