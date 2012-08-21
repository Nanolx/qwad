#----------------------------------------------------------------------
# WADd - a simple command line tool for packing and unpacking wads.
# (c) 2009 |Omega and #HACKERCHANNEL Productions.
#
# Wii.py (c) Xuzz, SquidMan, megazig, TheLemonMan, |Omega, and Matt_P.
#----------------------------------------------------------------------
import Wii, sys, os

if(len(sys.argv) < 2):
	print "Usage: python wads.py <input> <output> ..."
	sys.exit(0)

for i in range(1, len(sys.argv), 2):
	if(os.isdir(sys.argv[i]):
		elem = sys.argv[i]
		elem2 = sys.argv[i + 1]
		Wii.WAD.loadDir(elem).dumpFile(elem2)
	else:
		elem = sys.argv[i]
		elem2 = sys.argv[i + 1]
		Wii.WAD.loadFile(elem).dumpDir(elem2)
