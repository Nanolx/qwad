# -*- coding: utf-8 -*-

"""
Module implementing AboutQwad.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from Ui_AboutQwad import Ui_Dialog

def Version():
    return "0.2+svn"
def Author():
    return "ssorgatem <ssorgatem@esdebian.org>"

class AboutQwad(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.versionNumber.setText(Version())
        self.AuthorName.setText(Author())
