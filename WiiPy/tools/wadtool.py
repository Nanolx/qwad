#----------------------------------------------------------------------
# Copyright (C) 2009 zc00gii
#
# Wii.py (c) Xuzz, SquidMan, megazig, TheLemonMan, |Omega, and Matt_P.
#----------------------------------------------------------------------
import os, sys, Wii

def wadpack(waddir, wadfile):
	Wii.WAD.loadDir(waddir).dumpFile(wadfile)
	print "WAD packed successfully"

def wadunpack(wadfile,waddir):
	Wii.WAD.loadFile(wadfile).dumpDir(waddir)
	print "WAD unpacked successfully"

if(len(sys.argv) < 4):
        print "Usage: python wadtool.py [option] <input> <output>\nOptions:\n-u, --unpack     Unpack your desired WAD file\n-p, --pack       Pack your desired WAD file"
        sys.exit(0)

doPackOrUnpack = sys.argv[1]
inputWad = sys.argv[2]
outputWad = sys.argv[3]

if doPackOrUnpack in ('-u','--unpack'):
	wadunpack(inputWad, outputWad)
if doPackOrUnpack in ('-p','--pack'):
	wadpack(inputWad, outputWad)
