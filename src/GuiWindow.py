"""**************************************************************************************************
FILE: GuiWindow
Project: AcmeAutomator
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module initializes Gui Window functions.
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
CLASS: GuiWindow
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class GuiWindow:
    "Gui Window"
    """"""
    def __init__(self, gui_window = None):
        self.name = self.__class__.__name__
        self.gui_window = gui_window
    """"""
    def create(self):
        self.gui_window.setObjectName("gui_window")
        self.gui_window.resize(1295, 711)
        self.font = QtGui.QFont()
        self.font.setFamily("DejaVu Sans Mono")
        self.font.setPointSize(12)
        self.gui_window.setFont(self.font)
        self.gui_window.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.gui_window.setStyleSheet(StyleSheet(self.gui_window).get(stylesheet="GuiWindow.qss"))
        self.mainWindowWidget = QtWidgets.QWidget(self.gui_window)
        self.mainWindowWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.mainWindowWidget.setStyleSheet(StyleSheet(self.gui_window).get(stylesheet="MainWindow.qss"))
        self.mainWindowWidget.setObjectName("mainWindowWidget")
        return(self.mainWindowWidget)
"""*********************************************************************************************
End of File
********************************************************************************************"""
