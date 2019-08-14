"""**************************************************************************************************
FILE: ButtonControlGroupBox
Project: AcmeAutomator
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides startbutton functions.
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
class ButtonControlGroupBox:
    "Console Dut Tab Widget"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self, widget=None, gridLayout=None):
        self.buttonControlGroupBox = widget
        self.gridLayout = gridLayout
        self.font = QtGui.QFont()
        self.font.setFamily("Times New Roman")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setItalic(True)
        self.font.setWeight(75)
        self.buttonControlGroupBox.setFont(self.font)
        self.buttonControlGroupBox.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.buttonControlGroupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonControlGroupBox.setStyleSheet(StyleSheet(self.parent).get(stylesheet="ControlPanel.qss"))
        self.buttonControlGroupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonControlGroupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonControlGroupBox.setObjectName("buttonControlGroupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.buttonControlGroupBox)
        self.horizontalLayout_2.setContentsMargins(-1, 9, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.buttonControlGrouphorizontalLayout = QtWidgets.QHBoxLayout()
        self.buttonControlGrouphorizontalLayout.setObjectName("buttonControlGrouphorizontalLayout")
        self.horizontalLayout_2.addLayout(self.buttonControlGrouphorizontalLayout)
        self.gridLayout.addWidget(self.buttonControlGroupBox, 0, 0, 1, 1)
        return(self.buttonControlGroupBox, self.buttonControlGrouphorizontalLayout)
"""*********************************************************************************************
End of File
********************************************************************************************"""
