"""**************************************************************************************************
FILE: PauseButton
Project: AcmeAutomator
Author: Chripauseher Robson
Copyright by:  Chripauseher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides pausebutton functions.
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
CLASS: PauseButton
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class PauseButton:
    "Pause Button"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self, button=None):
        self.pauseButton = button
        self.font = QtGui.QFont()
        self.font.setFamily("Times New Roman")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setItalic(False)
        self.font.setWeight(75)
        self.pauseButton.setFont(self.font)
        self.pauseButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pauseButton.setStyleSheet(StyleSheet(self.parent).get(stylesheet="PauseButton.qss"))
        self.pauseButton.setObjectName("pauseButton")
        self.parent.buttonControlGrouphorizontalLayout.addWidget(self.pauseButton)
        return(self.pauseButton)
"""*********************************************************************************************
End of File
********************************************************************************************"""
