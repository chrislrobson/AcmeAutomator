"""**************************************************************************************************
FILE: DutLabel
Project: AcmeAutomator
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides DUT label functions.
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
CLASS: StartButton
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class DutLabel:
    "Dut Label"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self, widget=None, layout=None):
        self.consoleDutTab = widget
        self.gridLayout = layout
        self.dutLabel = QtWidgets.QLabel(self.consoleDutTab)
        self.font = QtGui.QFont()
        self.font.setFamily("Times New Roman")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setItalic(False)
        self.font.setWeight(75)
        self.dutLabel.setFont(self.font)
        self.dutLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.dutLabel.setStyleSheet(StyleSheet(self.parent).get(stylesheet="DutLabel.qss"))
        self.dutLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dutLabel.setObjectName("DutLabel")
        self.gridLayout.addWidget(self.dutLabel, 0, 1, 1, 1)
        return(self.dutLabel)
"""*********************************************************************************************
End of File
********************************************************************************************"""
