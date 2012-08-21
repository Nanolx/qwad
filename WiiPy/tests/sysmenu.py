import os, Wii

print 'Enter the sysmenu version you want then just wait...'
version = int(input()) #97
#Wii.NUS(0x0000000100000002, version).download('0000000100000002ver' + str(version))
os.chdir('0000000100000002ver' + str(version))
print 'Tmd dump :\n'
print '%s' % Wii.TMD().loadFile('tmd')
print 'Now unpacking all the archives in there :3\n'

for root, dirs, files in os.walk(os.getcwd()):
	for name in files:
		print '%s' % name
		location = os.getcwd() + '/' + str(name)
		if name == '00000000.app':
			print 'IMET Title : %s' % Wii.IMET(name).getTitle()
		if open(location).read(4) == '\x55\xaa\x38\x2d':
			print 'Now unpacking the u8 archive %s' % location
			try:
				Wii.U8().loadFile(location)
			except: 
				print "fix the U8 code!"
		if open(location).read(4) == '\x43\x43\x46\x00':	
			print 'Now unpacking the CCF archive %s' % location
			Wii.CCF(location).decompress()

