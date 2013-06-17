# -*- coding: utf-8 -*-

"""
Module implementing AboutQwad.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from Ui_AboutQwad import Ui_Dialog

def Version():
    return "0.8"
def Author():
    return "Christopher Roy Bratusek <nano@tuxfamily.org>"

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
