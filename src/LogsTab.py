"""**************************************************************************************************
FILE: LogsTab
Project: AcmeAutomator
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides Logs tab functions.
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
CLASS: LogsTab
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class LogsTab:
    "Logs Tab"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self):
        self.logsTab = QtWidgets.QWidget()
        self.logsTab.setStyleSheet(StyleSheet(self.parent).get(stylesheet="LogsTab.qss"))
        self.logsTab.setObjectName("logsTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.logsTab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.logsVerticalLayout = QtWidgets.QVBoxLayout()
        self.logsVerticalLayout.setObjectName("logsVerticalLayout")
        self.logsListWidget = QtWidgets.QListWidget(self.logsTab)
        self.logsListWidget.setStyleSheet(StyleSheet(self.parent).get(stylesheet="LogsListWidget.qss"))
        self.logsListWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logsListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logsListWidget.setObjectName("logsListWidget")
        self.logsVerticalLayout.addWidget(self.logsListWidget)
        self.verticalLayout_6.addLayout(self.logsVerticalLayout)
        self.parent.consoleDutTabWidget.addTab(self.logsTab, "")
        self.parent.gridLayoutMain.addWidget(self.parent.consoleDutTabWidget, 1, 0, 1, 2)
        return(self.logsTab, self.logsListWidget)
"""*********************************************************************************************
End of File
********************************************************************************************"""
