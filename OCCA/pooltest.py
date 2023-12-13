print "starting  code"

from multiprocessing import Pool
import gatecode
import polycode
import os.path


def foo1(x):
	errfile = "C:/Users/rachel/Desktop/error.txt"
	if os.path.isfile(errfile) :
		break
	out = gatecode.LPwriter(x)
	if out != 0:
		ff = open(errfile, 'w')
		ff.writeline(x)
		ff.close()
	return 0

t = polycode.triplets	

print "Starting parallel"

# if __name__ == "__main__":	
	# p = Pool(3)
	# p.map(foo2, i) 

plt.show()
	
print "ending code"