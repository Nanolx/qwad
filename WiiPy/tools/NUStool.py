#----------------------------------------------------------------------
# NUS Tool - a simple command line tool for NUS downloading.
# (c) 2009 |Omega and #HACKERCHANNEL Productions.
#
# Wii.py (c) Xuzz, SquidMan, megazig, TheLemonMan, |Omega, and Matt_P.
#----------------------------------------------------------------------

import os, sys, Wii, shutil

if len(sys.argv) < 3:
	print "Usage: python %s -(d/p) titleid version [decrypt/fakesign](True/False) [download/pack](dirname/filename)" % sys.argv[0]
	sys.exit()
print sys.argv
titleid = int(sys.argv[2], 16)
print titleid
ver = int(sys.argv[3])
print type(ver)
print ver
if not (sys.argv[4]) and sys.argv[1] == "-d" :
	decrypt = False
else:
	decrypt = True

if len(sys.argv) < 6:
	tmp = "tmp"
else:
	tmp = sys.argv[5]

#downloading

print "Downloading..."
if(ver != 0):
	Wii.NUS(titleid, ver).download(tmp, decrypt = decrypt)
else:
	Wii.NUS(titleid).download(tmp, decrypt = decrypt)
print "Done downloading!"

#wadpacking

if sys.argv[1] == "-p":
	print "packing"
	if len(sys.argv[5]) != 0:
		wadfile = str(sys.argv[5]) + ".wad"
	else:
		wadfile = str(titleid) + "ver" + str(ver) + ".wad"
	Wii.WAD.loadDir(tmp).dumpFile(wadfile, fakesign = sys.argv[4])
	if(os.path.isdir(tmp)): #cleanup
		shutil.rmtree(tmp)
	print"Done packing the WAD!"
print "Everything is done!\nHave a nice day. :3"
sys.exit()
