"""**************************************************************************************************
FILE: StatusBarMessages
Project: AcmeAutomator
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides statusbar functions.
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
CLASS: StatusBarMessages
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class StatusBarMessages:
    "StatusBar Messages"
    """"""
    def __init__( self, parent = None, gui_window = None ):
        self.name = self.__class__.__name__
        self.parent = parent
        self.gui_window = gui_window
    """"""
    def create(self):
        self.statusBarMessages = QtWidgets.QStatusBar(self.gui_window)
        self.statusBarMessages.setStyleSheet(StyleSheet(self.parent).get(stylesheet="StatusBarMessages.qss"))
        self.statusBarMessages.setObjectName("statusBarMessages")
        self.gui_window.setStatusBar(self.statusBarMessages)
        return(self.statusBarMessages)
"""*********************************************************************************************
End of File
********************************************************************************************"""
