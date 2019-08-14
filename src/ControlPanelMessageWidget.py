"""**************************************************************************************************
FILE: ControlPanelMessageWidget
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
CLASS: ControlPanelMessageWidget
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class ControlPanelMessageWidget:
    "Dut Label"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self, widget=None):
        self.mainWindowWidget = widget
        self.controlPanelMessageWidget = QtWidgets.QWidget(self.mainWindowWidget)
        self.controlPanelMessageWidget.setStyleSheet(StyleSheet(self.parent).get(stylesheet="ControlPanelMessageWidget.qss"))
        self.controlPanelMessageWidget.setObjectName("controlPanelMessageWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.controlPanelMessageWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        return(self.controlPanelMessageWidget, self.horizontalLayout)
"""*********************************************************************************************
End of File
********************************************************************************************"""
