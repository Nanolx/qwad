#!/usr/bin/env python
#coding=utf-8
import sys
import optparse
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QTranslator, QString, QLocale
from GUI.VenPri import MWQwad

parser = optparse.OptionParser("qwad <option> [value]\
				\n\nQwad (c) 2012 Christopher Roy Bratusek\
				\nLicensed under the GNU GENERAL PUBLIC LICENSE v3")

parser.add_option("-v", "--version", dest="version",
                  action="store_true", default=False, help="print version and exit")

(options, args) = parser.parse_args()

if options.version:
		print "0.6"
		sys.exit(0)

if __name__ == "__main__":
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

