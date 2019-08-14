"""**************************************************************************************************
FILE: ConsoleDutTabWidget
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
class ConsoleDutTabWidget:
    "Console Dut Tab Widget"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self, widget=None, layout=None):
        self.consoleDutTabWidget = widget
        self.horizontalLayout = layout
        self.font = QtGui.QFont()
        self.font.setFamily("DejaVu Sans")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.consoleDutTabWidget.setFont(self.font)
        self.consoleDutTabWidget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.consoleDutTabWidget.setStyleSheet(StyleSheet(self.parent).get(stylesheet="ConsoleDutTabWidget.qss"))
        self.consoleDutTabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.consoleDutTabWidget.setObjectName("consoleDutTabWidget")
        return(self.consoleDutTabWidget)
"""*********************************************************************************************
End of File
********************************************************************************************"""
