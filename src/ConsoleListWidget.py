"""**************************************************************************************************
FILE: ConsoleListWidget
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
CLASS: ConsoleListWidget
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class ConsoleListWidget:
    "Dut Label"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self, widget=None, layout=None, tabwidget=None):
        self.consoleDutTab = widget
        self.gridLayout = layout
        self.consoleDutTabWidget = tabwidget
        self.consoleListWidget = QtWidgets.QListWidget(self.consoleDutTab)
        self.consoleListWidget.setStyleSheet(StyleSheet(self.parent).get(stylesheet="ConsoleListWidget.qss"))
        self.consoleListWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.consoleListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.consoleListWidget.setObjectName("consoleListWidget")
        self.gridLayout.addWidget(self.consoleListWidget, 1, 0, 1, 1)
        self.consoleLabel = QtWidgets.QLabel(self.consoleDutTab)
        self.font = QtGui.QFont()
        self.font.setFamily("Times New Roman")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setItalic(False)
        self.font.setWeight(75)
        self.consoleLabel.setFont(self.font)
        self.consoleLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.consoleLabel.setStyleSheet(StyleSheet(self.parent).get(stylesheet="ConsoleLabel.qss"))
        self.consoleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.consoleLabel.setObjectName("ConsoleListWidget")
        self.gridLayout.addWidget(self.consoleLabel, 0, 0, 1, 1)
        self.consoleDutTabWidget.addTab(self.consoleDutTab, "")
        return(self.consoleListWidget, self.consoleLabel)
"""*********************************************************************************************
End of File
********************************************************************************************"""
