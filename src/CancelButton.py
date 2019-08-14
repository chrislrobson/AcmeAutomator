"""**************************************************************************************************
FILE: CancelButton
Project: AcmeAutomator
Author: Chricancelher Robson
Copyright by:  Chricancelher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides cancelbutton functions.
**************************************************************************************************"""
"""
Python Libraries
"""
from PyQt5 import QtCore, QtGui, QtWidgets
"""
Homegrown Libraries
"""
from StyleSheets import StyleSheet
"""
CLASS: CancelButton
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class CancelButton:
    "Cancel Button"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self, button=None):
        self.cancelButton = button
        self.font = QtGui.QFont()
        self.font.setFamily("Times New Roman")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setItalic(False)
        self.font.setWeight(75)
        self.cancelButton.setFont(self.font)
        self.cancelButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelButton.setStyleSheet(StyleSheet(self.parent).get(stylesheet="CancelButton.qss"))
        self.cancelButton.setObjectName("cancelButton")
        self.parent.buttonControlGrouphorizontalLayout.addWidget(self.cancelButton)
        return(self.cancelButton)
"""*********************************************************************************************
End of File
********************************************************************************************"""
