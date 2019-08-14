"""**************************************************************************************************
FILE: ConsoleDutTab
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
CLASS: ConsoleDutTab
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class ConsoleDutTab:
    "Console Dut Tab"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self):
        self.consoleDutTab = QtWidgets.QWidget()
        self.consoleDutTab.setStyleSheet(StyleSheet(self.parent).get(stylesheet="ConsoleDutTab.qss"))
        self.consoleDutTab.setObjectName("consoleDutTab")
        self.gridLayout = QtWidgets.QGridLayout(self.consoleDutTab)
        self.gridLayout.setObjectName("gridLayout")
        return(self.consoleDutTab, self.gridLayout)
"""*********************************************************************************************
End of File
********************************************************************************************"""
