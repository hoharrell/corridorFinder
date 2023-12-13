###### Triplet Finder ######

print "Starting triplet finder" 

import polycode
from multiprocessing import Pool


su = polycode.startunit
eu = polycode.endunit
polydict = polycode.polygons
	

# i = range(len(ids))
# trips = []


#find trips
# ff = open(myfile,'w')
# count = 0
# numtrips = 0
# for i in polydict:
	# count = count+1
	# print "on poly #" + str(count) + " out of " + str(len(polydict)) + " polys"
	# tempadjs = polycode.getadjs(i)
	# print numtrips
	# for a in tempadjs:
		# for b in tempadjs:
			# if polycode.overlaps(a,b) == False:
				# if a == su or b == eu or a < b:
					# numtrips = numtrips +1
					# writeline = str(a) + "\t" + str(i) + "\t" + str(b) + "\n"
					# ff.write(writeline)
				
# ff.close()    


def myfoo(x):
	trips = []
	print "On polygon "+str(x)
	# print len(trips)
	adjs = polycode.getadjs(x)
	for a in adjs:
		for b in adjs:
			if a == su or b == eu or a < b:
				if polycode.overlaps(a,b) == False:
					trips.append([a,x,b])
	return trips
	

		# myfoo(x)

		
if __name__ == '__main__':
	myfile="C:/rstjohn/El_Dorado_Exp/ElD_30ha_trips.txt"
	i=polydict.keys()
	# for x in range(0, 100):
		# if x in polydict:
			# i.append(x)
	pool = Pool(7)	
	alltrips = pool.map(myfoo, i) 
	alltrips = [ent for sublist in alltrips for ent in sublist]
	print len(alltrips)
	ff = open(myfile,'w')
	for t in alltrips:
		writeline=str(t[0])+"\t"+str(t[1])+"\t"+str(t[2])+"\n"
		ff.write(writeline)
	ff.close()
	
# def func(inputs):
    # successes = []

    # for input in inputs:
        # result = #something with return code
        # if result == 0:
            # successes.append(input)
    # return successes

# def main():     
    # pool = mp.Pool()
    # total_successes = pool.map(func, myInputs) # Returns a list of lists
    # # Flatten the list of lists
    # total_successes = [ent for sublist in total_successes for ent in sublist]
		
# myfile="C:/Users/rachel/Desktop/clustertripsnew2.txt"
# ff = open(myfile,'w')
# for i in range(0,len(trips)):
    # writeline=str(trips[i][0])+"\t"+str(trips[i][1])+"\t"+str(trips[i][2])+"\n"
    # ff.write(writeline)
# ff.close()

print "End of triplet finder"



