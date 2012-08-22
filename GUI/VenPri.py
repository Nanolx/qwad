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
        for key in TitleIDs.sorted_copy(TitleIDs.ChannelDict):
            self.comboBox2.addItem(key)
        self.getReady()

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
        self.idASCII.setText("%s" % binascii.unhexlify(str(tmd.tmd.titleid)[7:]))
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
        if self.comboBox.findText(selection) != 0:
            self.enteredTitleID.enabled = False
            self.enteredTitleID.setText(TitleIDs.TitleDict[str(selection)])
            self.availableVersions.setText(TitleIDs.IOSdict[str(selection)])

    @pyqtSignature("QString")
    def on_comboBox2_currentIndexChanged(self, selection):
        """
        Show the title ID of the selected title
        """
        if self.comboBox2.findText(selection) != 0:
            self.enteredTitleID.enabled = False
            self.enteredTitleID.setText(TitleIDs.ChannelDict[str(selection)])
            self.availableVersions.setText(TitleIDs.ChannelRegionDict[str(selection)])

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
            self.trUtf8("tmd; TMD"),
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

class Packing(Unpacking):
    def __init__(self, dirpath, wadpath, QMW, deletedir = False):
        Unpacking.__init__(self, wadpath, dirpath, QMW)
        self.deletedir = deletedir
    def run(self):
        self.qobject.emit(SIGNAL("working"),PACKING)
        try:
            print self.dirpath
            print self.wadpath
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

class nusDownloading(Unpacking):
    def __init__(self, titleid, version, outputdir, decrypt, QMW):
        Unpacking.__init__(self, None, outputdir, QMW)
        if version != None:
            self.version = int(version)
        else:
            self.version = None
        self.decrypt = decrypt
        self.titleid = titleid
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

#Statusbar messages
#FIXME: Why don't they get translated? It's frustrating
DOWNLOADING = QT_TR_NOOP("Downloading files from NUS... This may take a while, please, be patient.")
UNPACKING = QT_TR_NOOP("Unpacking WAD...")
PACKING = QT_TR_NOOP("Packing into WAD...")
CLEANING = QT_TR_NOOP("Cleaning temporary files...")
