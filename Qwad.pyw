#!/usr/bin/env python
#coding=utf-8
import sys, os
from optparse import OptionParser
from optparse import Option, OptionValueError
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QTranslator, QString, QLocale
from GUI.VenPri import MWQwad
from GUI.VenPri import nusDownloadingCLI
from TitleIDs import TitleDict

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

def main():
    description = """NUS-Downloader, WadManager and TMD-Viewer for Linux"""
    parser = OptionParser(option_class=MultipleOption,
                          usage='usage: qwad [OPTIONS] ARGUMENT',
                          description=description)
    parser.add_option('-d', '--downloads',
                      action="extend", type="string",
                      dest='download',
                      metavar='Arguments',
                      help='IOS <IOS> <Version> <Output> <DeCrypt> <Pack>')
    parser.add_option("-v", "--version", dest="version",
		      action="store_true", default=False, help="print version and exit")

    options, args = parser.parse_args()

    if options.version:
	    print "%s" % VERSION
	    sys.exit(0)

    if options.download:
	    if "IOS" in str(args[0]):
		xarg = TitleDict[str(args[0])]
		print "%s" % xarg
		print "%d" % int(str(xarg).lower(),16)
	   	nusdow = nusDownloadingCLI(int(str(xarg).lower(),16), args[1], args[2], args[3], args[4])
	    else:
		print "%s" % args[0]
		print "%d" % int(str(args[0]).lower(),16)
	        nusdow = nusDownloadingCLI(int(str(args[0]).lower(),16), args[1], args[2], args[3], args[4])
	    nusdow.start()
	    sys.exit(0)

    os.chdir(os.getenv("HOME"))
    translator = QTranslator()
    translator.load(QString("i18n/Qwad_%1").arg(QLocale.system().name()))
    qttranslator = QTranslator()
    qttranslator.load(QString("qt_%1").arg(QLocale.system().name()))
    Vapp = QApplication(sys.argv)
    Vapp.setOrganizationName("ssorgatem productions")
    Vapp.setApplicationName("Qwad")
    Vapp.installTranslator(translator)
    Vapp.installTranslator(qttranslator)
    VentanaP = MWQwad()
    VentanaP.show()
    sys.exit(Vapp.exec_())

if __name__ == "__main__":
    main()
