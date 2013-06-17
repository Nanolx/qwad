# -*- coding: utf-8 -*-
"""
Module implementing Qwad's main window
"""
from PyQt4.QtGui import QMainWindow,QFileDialog,QMessageBox, QLabel
from PyQt4.QtCore import pyqtSignature,QString,QT_TR_NOOP,SIGNAL,QObject
from WiiPy.archive import WAD
from WiiPy.title import NUS, TMD
from Ui_VenPri import Ui_Qwad
from shutil import rmtree
from threading import Thread
import TitleIDs
import tempfile, os, time
import binascii

CWD = os.getcwd()

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

class MWQwad(QMainWindow, Ui_Qwad):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.defaultversion = self.trUtf8("""(Latest)""")
	self.availableVersions.setText("(---)")
        self.VersionlineEdit.setText(self.defaultversion)
        for key in TitleIDs.sorted_copy(TitleIDs.TitleDict):
            self.comboBox.addItem(key)
        for key in TitleIDs.SupportedRegions:
            self.ChooseRegion.addItem(key)
        self.getReady()
        self.default_region = ""

    def Status(self,status):
        print status
        self.setEnabled(False)
        self.statusBar.showMessage(status)

    def getReady(self):
        self.setEnabled(True)
        self.statusBar.showMessage(self.trUtf8("Ready"))
        os.chdir(CWD)
        print "Done."

    def ErrorDiag(self, error = QT_TR_NOOP("Unknown error")):
            print error
            QMessageBox.critical(None,
                self.trUtf8("Error"),
                self.trUtf8("""An error has ocurred:""") +" " + str(error),
                QMessageBox.StandardButtons(\
                QMessageBox.Ok),
                QMessageBox.Ok)

    def loadTMD(self,tmdpath):#TODO: TMD viewer
        """
        Displays _TMD information in the UI
        """
        tmd = TMD().loadFile(tmdpath)
        self.TitleID.setText("%016x" % tmd.tmd.titleid)
        tid = "%016x" % tmd.tmd.titleid
        tid = tid[8:]
        asc = ''.join([chr(int(''.join(c), 16)) for c in zip(tid[0::2],tid[1::2])])
        self.idASCII.setText("%s" % asc)
        self.IOSversion.setText(TitleIDs.TitleSwapDict["%s" % ("%016x" % tmd.tmd.iosversion)])
        self.TitleType.setText(str(tmd.tmd.title_type))
        self.GroupID.setText(str(tmd.tmd.group_id))
        self.Reserved.setText(str(tmd.tmd.reserved))
        self.AccessRights.setText(str(tmd.tmd.access_rights))
        self.Version.setText(str(tmd.tmd.title_version))
        self.Contents.setText(str(tmd.tmd.numcontents))
        self.BootIndex.setText(str(tmd.tmd.boot_index))

    @pyqtSignature("")
    def on_BotonRutaWad_clicked(self):
        """
        Get path to WAD file
        """
        WadPath = QFileDialog.getOpenFileName(\
            None,
            self.trUtf8("Select WAD file"),
            QString(),
            self.trUtf8("*.wad; *.WAD"),
            None)
        if WadPath != "" :
            self.MuestraRutaWad.setText(WadPath)

    @pyqtSignature("")
    def on_BotonRutaExtraer_clicked(self):
        """
        WAD contents output path
        """
        OutputDir = QFileDialog.getExistingDirectory(\
            None,
            self.trUtf8("Select where to store WAD contents"),
            QString(),
            QFileDialog.Options(QFileDialog.ShowDirsOnly))
        if OutputDir != "":
            self.MuestraRutaExtraer.setText(OutputDir)

    @pyqtSignature("")
    def on_Desempaqueta_clicked(self):
        """
        Unpack wad
        """
        try:
            self.unpack = Unpacking(str(self.MuestraRutaWad.text()), str(self.MuestraRutaExtraer.text()), self)
            self.unpack.start()
        except Exception, e:
            self.ErrorDiag(e)

    @pyqtSignature("")
    def on_BotonRutaEmpaquetado_clicked(self):
        """
        Select where to save the newly created WAD
        """
        NewWadPath = QFileDialog.getSaveFileName(\
            None,
            self.trUtf8("Select where to save the newly created WAD"),
            QString("output.wad"),
            self.trUtf8("*.wad; *.WAD"),
            None)
        if NewWadPath != "":
            self.MuestraRutaEmpaquetado.setText(NewWadPath)

    @pyqtSignature("")
    def on_BotonRutaDesempaquetado_clicked(self):
        """
        Get path off folder to pack.
        """
        Dir2Wad = QFileDialog.getExistingDirectory(\
            None,
            self.trUtf8("Select folder to pack into WAD"),
            QString(),
            QFileDialog.Options(QFileDialog.ShowDirsOnly))
        if Dir2Wad != "":
            self.MuestraRutaDesempaquetado.setText(Dir2Wad)

    @pyqtSignature("")
    def on_Empaqueta_clicked(self):
        """
        Create WAD
        """
        self.setEnabled(False)
        try:
            self.packing = Packing(str(self.MuestraRutaDesempaquetado.text()),str(self.MuestraRutaEmpaquetado.text()), self)
            self.packing.start()
        except Exception, e:
            self.ErrorDiag(e)
        self.setEnabled(True)

    @pyqtSignature("")
    def on_actionAcerca_de_Qwad_triggered(self):
        """
        About Qwad
        """
        from AboutQwad import AboutQwad
        Pop = AboutQwad()
        Pop.exec_()

    @pyqtSignature("")
    def on_actionAbout_Qt_triggered(self):
        """
        About Qt
        """
        QMessageBox.aboutQt(None,
            self.trUtf8("About Qt"))

    @pyqtSignature("")
    def on_Download_from_NUS_clicked(self):
        """
        Start doing the actual work... well, in fact, the actual work is done by Wii.py
        """
        try:
            version = self.VersionlineEdit.text()
            if  version == self.defaultversion:
                print "downloading latest version"
                version = None
            else:
                version = str(version)
                print "downloading version " + version
            outputdir = str(self.NusOutputPath.text())
            self.nusdow = nusDownloading(int(str(self.enteredTitleID.text()).lower(),16), version, outputdir,  self.decryptCheck.isChecked(), self)
            self.nusdow.start()
        except Exception, e:
            self.ErrorDiag(e)

    @pyqtSignature("")
    def on_NusOutputButton_clicked(self):
        """
        Selects the output path
        """
        if self.pack_in_WAD_checkbox.isChecked():
            outputdir = QFileDialog.getSaveFileName(\
                None,
                self.trUtf8("Select where to save the downloaded WAD"),
                QString(),
                self.trUtf8("*.wad; *.WAD"),
                None)
        else:
            outputdir = QFileDialog.getExistingDirectory(\
                None,
                self.trUtf8("Select the directory where store the downloaded files"),
                QString(),
                QFileDialog.Options(QFileDialog.ShowDirsOnly))
        if outputdir != "":
            self.NusOutputPath.setText(outputdir)

    @pyqtSignature("QString")
    def on_comboBox_currentIndexChanged(self, selection):
        """
        Show the title ID of the selected title
        """
        if self.comboBox.findText(selection) == 0:
            self.enteredTitleID.setText("")
            self.availableVersions.setText("")
        elif self.comboBox.findText(selection) > 0:
            self.enteredTitleID.enabled = False
            self.enteredTitleID.setText(TitleIDs.TitleDict[str(selection)])
            self.availableVersions.setText(TitleIDs.IOSdict[str(selection)])

    @pyqtSignature("QString")
    def on_comboBox2_currentIndexChanged(self, selection):
        """
        Show the title ID of the selected title
        """
        if self.comboBox2.findText(selection) == 0:
            self.enteredTitleID.setText("")
            self.availableVersions.setText("")
        elif self.comboBox2.findText(selection) > 0:
            self.enteredTitleID.enabled = False
            if self.default_region == "JAP":
                self.enteredTitleID.setText(TitleIDs.ChannelJAPDict[str(selection)])
                self.availableVersions.setText(TitleIDs.ChannelJAPVerDict[str(selection)])
            elif self.default_region == "PAL":
                self.enteredTitleID.setText(TitleIDs.ChannelPALDict[str(selection)])
                self.availableVersions.setText(TitleIDs.ChannelPALVerDict[str(selection)])
            elif self.default_region == "USA":
                self.enteredTitleID.setText(TitleIDs.ChannelUSADict[str(selection)])
                self.availableVersions.setText(TitleIDs.ChannelUSAVerDict[str(selection)])

    @pyqtSignature("QString")
    def on_ChooseRegion_currentIndexChanged(self, selection):
        self.default_region = "JAP"
        if self.default_region != "":
            count = self.comboBox2.count()
            while count > -1 :
                self.comboBox2.removeItem(count)
                count = count - 1
        if self.ChooseRegion.findText(selection) != 0:
            self.default_region = str(selection)
            self.comboBox2.addItem("Choose Channel")
            if self.default_region == "JAP":
                for key in TitleIDs.sorted_copy(TitleIDs.ChannelJAPDict):
                    self.comboBox2.addItem(key)
            elif self.default_region == "PAL":
                for key in TitleIDs.sorted_copy(TitleIDs.ChannelPALDict):
                    self.comboBox2.addItem(key)
            elif self.default_region == "USA":
                for key in TitleIDs.sorted_copy(TitleIDs.ChannelUSADict):
                    self.comboBox2.addItem(key)

    @pyqtSignature("")
    def on_enteredTitleID_returnPressed(self):
        """
        Place combobox un custom titleid
        """
        self.comboBox.setCurrentIndex(0)

    @pyqtSignature("int")
    def on_pack_in_WAD_checkbox_stateChanged(self, state):
        """
        Clear output path, because we change output type
        """
        self.NusOutputPath.clear()
        if state == 2:
            self.decryptCheck.setChecked(False)
            self.decryptCheck.setEnabled(False)
        elif state == 0:
            self.decryptCheck.setChecked(True)
            self.decryptCheck.setEnabled(True)
        elif state == 1:
            print "OMG, what are you doing?"
        else:
            print "This is the end of the world. For PyQt4, at least"

    @pyqtSignature("")
    def on_TMDfilepath_returnPressed(self):
        """
        Trigger loadTMD
        """
        self.loadTMD(str(self.TMDfilepath.text()))

    @pyqtSignature("")
    def on_TMDfilebutton_clicked(self):
        """
        Trigger loadTMD
        """
        tmdpath = QFileDialog.getOpenFileName(\
            None,
            self.trUtf8("Select a TMD file"),
            QString(),
            self.trUtf8("*.tmd; *.TMD"),
            None,
            QFileDialog.Options(QFileDialog.DontResolveSymlinks))
        if tmdpath != "":
            self.TMDfilepath.setText(tmdpath)
            self.loadTMD(str(tmdpath))

#Here useful thread classes
class Unpacking(Thread):
    def __init__(self, wadpath, dirpath, QMW):
        Thread.__init__(self)
        self.wadpath = wadpath
        self.dirpath = dirpath
        self.QMW = QMW
        self.qobject = QObject()
        self.qobject.connect(self.qobject, SIGNAL("working"),self.QMW.Status)
        self.qobject.connect(self.qobject, SIGNAL("Exception"),self.QMW.ErrorDiag)
        self.qobject.connect(self.qobject, SIGNAL("Done"),self.QMW.getReady)
    def run(self):
        self.qobject.emit(SIGNAL("working"),UNPACKING)
        try:
            WAD.loadFile(self.wadpath).dumpDir(self.dirpath)
        except Exception, e:
            print e
            self.qobject.emit(SIGNAL("Exception"),e)
        self.qobject.emit(SIGNAL("Done"))

class UnpackingCLI(Thread):
    def __init__(self, wadpath, dirpath):
        Thread.__init__(self)
        self.wadpath = wadpath
        self.dirpath = dirpath
    def run(self):
        try:
            WAD.loadFile(self.wadpath).dumpDir(self.dirpath)
        except Exception, e:
            print e
        print "Done"

class Packing(Unpacking):
    def __init__(self, dirpath, wadpath, QMW, deletedir = False):
        Unpacking.__init__(self, wadpath, dirpath, QMW)
        self.deletedir = deletedir
    def run(self):
        self.qobject.emit(SIGNAL("working"),PACKING)
        try:
            print self.wadpath
	    print self.dirpath
	    WAD.loadDir(self.dirpath).dumpFile(self.wadpath)
            if self.deletedir:
                print "Cleaning temporary files"
                self.qobject.emit(SIGNAL("working"),CLEANING)
                rmtree(self.dirpath)
        except Exception, e:
            if self.deletedir:
                print "Cleaning temporary files"
                self.qobject.emit(SIGNAL("working"),CLEANING)
                rmtree(self.dirpath)
            print e
            self.qobject.emit(SIGNAL("Exception"),e)
        self.qobject.emit(SIGNAL("Done"))

class PackingCLI(UnpackingCLI):
    def __init__(self, dirpath, wadpath, deletedir = False):
        UnpackingCLI.__init__(self, wadpath, dirpath)
        self.deletedir = deletedir
    def run(self):
        try:
            print self.dirpath
            print self.wadpath
            WAD.loadDir(self.dirpath).dumpFile(self.wadpath)
            if self.deletedir:
                print "Cleaning temporary files"
                rmtree(self.dirpath)
        except Exception, e:
            if self.deletedir:
                print "Cleaning temporary files"
                rmtree(self.dirpath)
            print e
	print "Done"

class nusDownloading(Unpacking):
    def __init__(self, titleid, version, outputdir, decrypt, QMW):
        Unpacking.__init__(self, None, outputdir, QMW)
        if version != None:
            self.version = int(version)
        else:
            self.version = None
        self.decrypt = decrypt
        self.titleid = titleid
	print self.titleid
	print self.version
    def run(self):
        self.qobject.emit(SIGNAL("working"),DOWNLOADING)
        try:
            if self.QMW.pack_in_WAD_checkbox.isChecked():
                self.dirpath = tempfile.gettempdir() + "/NUS_"+ str(time.time()).replace(".","") # A safe place for temporary files
                NUS(self.titleid,self.version).download(self.dirpath, decrypt = self.decrypt)
                self.packing = Packing(self.dirpath, str(self.QMW.NusOutputPath.text()), self.QMW, True)
                self.packing.start()
            else:
                NUS(self.titleid,self.version).download(self.dirpath, decrypt = self.decrypt)
                self.qobject.emit(SIGNAL("Done"))
        except Exception, e:
            print e
            Errormsg = str(e) + ". " +  QT_TR_NOOP(QString("Title %1 version %2 maybe isn't available for download on NUS.").arg(str(self.titleid)).arg(str(self.version)))
            self.qobject.emit(SIGNAL("Exception"),Errormsg)
            self.qobject.emit(SIGNAL("Done"))

class nusDownloadingCLI(UnpackingCLI):
    def __init__(self, titleid, version, outputdir, decrypt, pack):
        UnpackingCLI.__init__(self, None, outputdir)
        if version != None:
            self.version = int(version)
        else:
            self.version = None
	self.decrypt = str2bool(decrypt)
	self.pack = str2bool(pack)
        self.titleid = titleid
	self.outputdir = outputdir
    def run(self):
        try:
            if self.pack:
                self.dirpath = tempfile.gettempdir() + "/NUS_"+ str(time.time()).replace(".","")
                NUS(self.titleid, self.version).download(self.dirpath, decrypt = self.decrypt)
                self.packing = PackingCLI(self.dirpath, str(self.outputdir), True)
                self.packing.start()
            else:
                NUS(self.titleid,self.version).download(self.outputdir, decrypt = self.decrypt)
        except Exception, e:
            print e

def ShowTMD(tmdpath):
	"""
	Displays _TMD information in the CLI
	"""
	tmd = TMD().loadFile(tmdpath)
	print "Title ID (HEX)     : %016x" % tmd.tmd.titleid
	tid = "%016x" % tmd.tmd.titleid
	tid = tid[8:]
	asc = ''.join([chr(int(''.join(c), 16)) for c in zip(tid[0::2],tid[1::2])])
	print "Title ID (ASCII)   : %s" % asc
	print "Title Version      : %s" % tmd.tmd.title_version
	print "Title Boot Index   : %s" % tmd.tmd.boot_index
	print "Title Contents     : %s" % tmd.tmd.numcontents
	if ("%016x" % tmd.tmd.iosversion) == "0000000000000000":
		print "Title IOS          : --"
	else:
		print "Title IOS          : %s" % TitleIDs.TitleSwapDict["%s" % ("%016x" % tmd.tmd.iosversion)]
	print "Title Access Rights: %s" % tmd.tmd.access_rights
	print "Title Type         : %s" % tmd.tmd.title_type
	print "Title Group ID     : %s" % tmd.tmd.group_id
	print "Title Reserved     : %s" % ''.join(str(tmd.tmd.reserved))

#Statusbar messages
#FIXME: Why don't they get translated? It's frustrating
DOWNLOADING = QT_TR_NOOP("Downloading files from NUS... This may take a while, please, be patient.")
UNPACKING = QT_TR_NOOP("Unpacking WAD...")
PACKING = QT_TR_NOOP("Packing into WAD...")
CLEANING = QT_TR_NOOP("Cleaning temporary files...")
