# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ssorgatem/Documents/python/Qwad/GUI/AboutQwad.ui'
#
# Created: Sat Jul 25 02:02:44 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(441, 496)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/wad.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.QwadIcon = QtGui.QLabel(Dialog)
        self.QwadIcon.setGeometry(QtCore.QRect(150, 0, 131, 131))
        self.QwadIcon.setPixmap(QtGui.QPixmap(":/icons/wad.png"))
        self.QwadIcon.setScaledContents(False)
        self.QwadIcon.setObjectName("QwadIcon")
        self.Qwad_name = QtGui.QLabel(Dialog)
        self.Qwad_name.setGeometry(QtCore.QRect(170, 110, 91, 51))
        self.Qwad_name.setObjectName("Qwad_name")
        self.Version = QtGui.QLabel(Dialog)
        self.Version.setGeometry(QtCore.QRect(180, 150, 51, 21))
        self.Version.setObjectName("Version")
        self.byAuthor = QtGui.QLabel(Dialog)
        self.byAuthor.setGeometry(QtCore.QRect(70, 170, 51, 20))
        self.byAuthor.setObjectName("byAuthor")
        self.versionNumber = QtGui.QLabel(Dialog)
        self.versionNumber.setGeometry(QtCore.QRect(230, 150, 131, 21))
        self.versionNumber.setObjectName("versionNumber")
        self.AuthorName = QtGui.QLabel(Dialog)
        self.AuthorName.setGeometry(QtCore.QRect(120, 170, 311, 20))
        self.AuthorName.setObjectName("AuthorName")
        self.abuttabs = QtGui.QTabWidget(Dialog)
        self.abuttabs.setGeometry(QtCore.QRect(10, 200, 421, 281))
        self.abuttabs.setObjectName("abuttabs")
        self.licensetab = QtGui.QWidget()
        self.licensetab.setObjectName("licensetab")
        self.textEdit = QtGui.QTextEdit(self.licensetab)
        self.textEdit.setGeometry(QtCore.QRect(0, 10, 411, 231))
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setObjectName("textEdit")
        self.abuttabs.addTab(self.licensetab, "")
        self.thankstab = QtGui.QWidget()
        self.thankstab.setObjectName("thankstab")
        self.label = QtGui.QLabel(self.thankstab)
        self.label.setGeometry(QtCore.QRect(10, 10, 391, 121))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.abuttabs.addTab(self.thankstab, "")

        self.retranslateUi(Dialog)
        self.abuttabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.Qwad_name.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:300; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt; font-weight:600;\">Qwad</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.Version.setText(QtGui.QApplication.translate("Dialog", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.byAuthor.setText(QtGui.QApplication.translate("Dialog", "Author: ", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setText(QtGui.QApplication.translate("Dialog", "GNU General Public License v3", None, QtGui.QApplication.UnicodeUTF8))
        self.abuttabs.setTabText(self.abuttabs.indexOf(self.licensetab), QtGui.QApplication.translate("Dialog", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Thanks to Wii.py team: Xuzz, SquidMan, megazig, TheLemonMan, |Omega, and Matt_P. Qwad is only a frontend for their unbelievably awesome framework.", None, QtGui.QApplication.UnicodeUTF8))
        self.abuttabs.setTabText(self.abuttabs.indexOf(self.thankstab), QtGui.QApplication.translate("Dialog", "Thanks", None, QtGui.QApplication.UnicodeUTF8))

import Qwad_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

