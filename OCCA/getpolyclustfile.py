#Get poly clusts
print "Starting getpolyclustfile"
import polycode

polyclustfile = "C:/Users/rachel/Desktop/Work/WC_Stuff/El_Dorado_Exp/20ha_polyclust.txt"

ids = polycode.polygons.keys()
clusters = polycode.clusters

ids.sort()
f = open(polyclustfile, 'w')
for i in ids:
	if i > 1362:
		continue
	print i
	writeline = str(i)
	for c in clusters:
		if i in clusters[c]:
			writeline = writeline + "\t" + str(c)
	writeline = writeline + '\n'
	f.write(writeline)
f.close()


print "End of getpolyclustfile"