#!/usr/bin/env python
#coding=utf-8
import sys, os
from optparse import OptionParser
from optparse import Option, OptionValueError
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QTranslator, QString, QLocale
from GUI.VenPri import MWQwad, nusDownloadingCLI, PackingCLI, UnpackingCLI, ShowTMD
from TitleIDs import TitleDict, IOSdict, swap_dic

class MultipleOption(Option):
    ACTIONS = Option.ACTIONS + ("extend",)
    STORE_ACTIONS = Option.STORE_ACTIONS + ("extend",)
    TYPED_ACTIONS = Option.TYPED_ACTIONS + ("extend",)
    ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("extend",)

    def take_action(self, action, dest, opt, value, values, parser):
        if action == "extend":
            values.ensure_value(dest, []).append(value)
        else:
            Option.take_action(self, action, dest, opt, value, values, parser)

VERSION = '0.6'

def opts():
    os.chdir(sys.path[0])
    description = """NUS-Downloader, WadManager and TMD-Viewer for Linux"""
    parser = OptionParser(option_class=MultipleOption,
                          usage='usage: qwad [OPTIONS] ARGUMENT',
                          description=description)
    parser.add_option('-d', '--download',
                      action="extend", type="string",
                      dest='download',
                      metavar='Arguments',
                      help="IOS Version Output Decrypt Pack")
    parser.add_option('-u', "--unpack", dest="unpack", action="extend",
                      type="string", metavar='Arguments', help="unpack a WAD")
    parser.add_option('-p', "--pack", dest="pack", action="extend",
                      type="string", metavar='Arguments', help="pack folder as WAD")
    parser.add_option('-g', "--getversions", dest="getversions",
                      action="store_true", default=False, help="get available versions for IOS")
    parser.add_option('-c', "--convert", dest="convert",
		              action="store_true", default=False, help="convert between IOSxx and hex-value")
    parser.add_option('-t',  "--tmdinfo", default=False, dest="tmdinfo", action="store_true",
					  help="Show infos provided by TMD file")
    parser.add_option("-v", "--version", dest="version",
		      action="store_true", default=False, help="print version and exit")

    options, args = parser.parse_args()

    if options.version:
	    print "%s" % VERSION
	    sys.exit(0)

    if options.download:
	    if "IOS" in str(options.download[0]):
		xarg = TitleDict[str(options.download[0])]
	   	nusdow = nusDownloadingCLI(int(str(xarg).lower(),16), args[0], args[1], args[2], args[3])
	    else:

	        nusdow = nusDownloadingCLI(int(str(options.download[0]).lower(),16), args[0], args[1], args[2], args[3])
	    nusdow.start()
	    sys.exit(0)

    if options.getversions:
	    if "IOS" in str(args[0]):
		print "Available Versions for %s: %s" % (str(args[0]), IOSdict[str(args[0])])
	    else:
		NewDict = swap_dic(TitleDict)
		xarg = NewDict[str(args[0])]
	        print "Available Versions for %s: %s" % (str(args[0]), IOSdict[str(xarg)])
	    sys.exit(0)

    if options.convert:
	    if "IOS" in str(args[0]):
		print "%s == %s" % (str(args[0]), TitleDict[str(args[0])])
	    else:
		NewDict = swap_dic(TitleDict)
		xarg = NewDict[str(args[0])]
	        print "%s == %s" % (str(args[0]), xarg)
	    sys.exit(0)

    if options.unpack:
	    if os.access(str(options.unpack[0]), os.R_OK):
		wad = str(options.unpack[0])
	    else:
		print "WAD file %s does not exist." % str(options.unpack[0])
		sys.exit(1)
	    if os.access(str(args[0]), os.W_OK):
		folder = str(args[0])
	    else:
		os.mkdir(str(args[0]), 0755)
	    if os.access(str(args[0]), os.W_OK):
		UnpackingCLI(wad, str(args[0])).start()
	        sys.exit(0)
	    else:
		print "Output folder %s not writeable." % str(args[0])
  		sys.exit(1)

    if options.pack:
	    if os.access(str(options.pack[0]), os.R_OK):
		folder = str(options.pack[0])
	    else:
		print "Input folder %s not readable." % str(options.pack[0])
  		sys.exit(1)
	    if os.access(os.path.dirname(str(args[0])), os.W_OK):
	    	PackingCLI(folder, str(args[0])).start()
	        sys.exit(0)
	    else:
		print "Output file %s can't be created." % str(args[0])
		sys.exit(1)

    if options.tmdinfo:
        if os.access(str(args[0]), os.R_OK):
            ShowTMD(str(args[0]))
            sys.exit(0)
        else:
            print "Can't access %s." % str(args[0])
            sys.exit(1)

def main():
    # load our own translations
    translator = QTranslator()
    translator.load(QString("i18n/Qwad_%1").arg(QLocale.system().name()))
    # load Qt translations
    qttranslator = QTranslator()
    qttranslator.load(QString("qt_%1").arg(QLocale.system().name()))
    # change directory in $HOME, so that file-seletors don't start in Qwads source/data directory
    os.chdir(os.getenv("HOME"))
    # misc stuff
    Vapp = QApplication(sys.argv)
    Vapp.setOrganizationName("Nanolx")
    Vapp.setApplicationName("Qwad")
    Vapp.installTranslator(translator)
    Vapp.installTranslator(qttranslator)
    VentanaP = MWQwad()
    VentanaP.show()
    sys.exit(Vapp.exec_())

if __name__ == "__main__":
    opts()
    main()
