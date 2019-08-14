"""**************************************************************************************************
FILE: DutListWidget
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
class DutListWidget:
    "Dut Label"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self, widget=None, layout=None):
        self.consoleDutTab = widget
        self.gridLayout = layout
        self.dutListWidget = QtWidgets.QListWidget(self.consoleDutTab)
        self.dutListWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dutListWidget.setStyleSheet(StyleSheet(self.parent).get(stylesheet="DutListWidget.qss"))
        self.dutListWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.dutListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.dutListWidget.setObjectName("dutListWidget")
        self.gridLayout.addWidget(self.dutListWidget, 1, 1, 1, 1)
        return(self.dutListWidget)
"""*********************************************************************************************
End of File
********************************************************************************************"""
