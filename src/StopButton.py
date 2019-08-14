"""**************************************************************************************************
FILE: StopButton
Project: AcmeAutomator
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides stopbutton functions.
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
CLASS: StopButton
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class StopButton:
    "Stop Button"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self, button=None):
        self.stopButton = button
        self.font = QtGui.QFont()
        self.font.setFamily("Times New Roman")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setItalic(False)
        self.font.setWeight(75)
        self.stopButton.setFont(self.font)
        self.stopButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stopButton.setStyleSheet(StyleSheet(self.parent).get(stylesheet="StopButton.qss"))
        self.stopButton.setObjectName("stopButton")
        self.parent.buttonControlGrouphorizontalLayout.addWidget(self.stopButton)
        return(self.stopButton)
"""*********************************************************************************************
End of File
********************************************************************************************"""
