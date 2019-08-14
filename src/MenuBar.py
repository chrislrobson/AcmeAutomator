"""**************************************************************************************************
FILE: MenuBar
Project: AcmeAutomator
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides menubar functions.
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
CLASS: MenuBar
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class MenuBar:
    "MenuBar"
    """"""
    def __init__( self, parent = None, gui_window = None ):
        self.name = self.__class__.__name__
        self.parent = parent
        self.gui_window = gui_window
    """"""
    def create(self):
        self.menubar = QtWidgets.QMenuBar(self.gui_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1295, 28))
        self.font = QtGui.QFont()
        self.font.setFamily("Times New Roman")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setItalic(False)
        self.font.setWeight(75)
        self.menubar.setFont(self.font)
        self.menubar.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.menubar.setStyleSheet(StyleSheet(self.parent).get(stylesheet="MenuBar.qss"))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setStyleSheet(StyleSheet(self.parent).get(stylesheet="MenuFile.qss"))
        self.menuFile.setObjectName("menuFile")
        self.menuConfiguration = QtWidgets.QMenu(self.menubar)
        self.menuConfiguration.setStyleSheet(StyleSheet(self.parent).get(stylesheet="MenuConfiguration.qss"))
        self.menuConfiguration.setObjectName("menuConfiguration")
        self.menuTest = QtWidgets.QMenu(self.menubar)
        self.menuTest.setStyleSheet(StyleSheet(self.parent).get(stylesheet="MenuTest.qss"))
        self.menuTest.setObjectName("menuTest")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setStyleSheet(StyleSheet(self.parent).get(stylesheet="MenuHelp.qss"))
        self.menuHelp.setObjectName("menuHelp")
        self.gui_window.setMenuBar(self.menubar)
        return()
    """"""
    def set_actions(self):
        self.actionReset = QtWidgets.QAction(self.gui_window)
        self.actionReset.setObjectName("actionReset")
        self.actionExit = QtWidgets.QAction(self.gui_window)
        self.actionExit.setObjectName("actionExit")
        self.actionChangeProfilesDirectory = QtWidgets.QAction(self.gui_window)
        self.actionChangeProfilesDirectory.setObjectName("actionProfileDirectory")
        self.actionSelectPlaybook = QtWidgets.QAction(self.gui_window)
        self.actionSelectPlaybook.setObjectName("actionSelectPlaybook")
        self.actionSelectDeviceUnderTest = QtWidgets.QAction(self.gui_window)
        self.actionSelectDeviceUnderTest.setObjectName("actionSelectDUT")
        self.actionClearDUTSelections = QtWidgets.QAction(self.gui_window)
        self.actionClearDUTSelections.setObjectName("actionCleatDUTSelections")
        self.actionExecuteTest = QtWidgets.QAction(self.gui_window)
        self.actionExecuteTest.setObjectName("actionExecute")
        self.actionManual = QtWidgets.QAction(self.gui_window)
        self.actionManual.setObjectName("actionManual")
        self.actionAbout = QtWidgets.QAction(self.gui_window)
        self.actionAbout.setObjectName("actionAbout")
        self.actionDocumentation = QtWidgets.QAction(self.gui_window)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuFile.addSeparator()
        self.menuConfiguration.addSeparator()
        self.menuConfiguration.addAction(self.actionChangeProfilesDirectory)
        self.menuConfiguration.addSeparator()
        self.menuTest.addSeparator()
        self.menuTest.addAction(self.actionSelectPlaybook)
        self.menuTest.addSeparator()
        self.menuTest.addAction(self.actionSelectDeviceUnderTest)
        self.menuTest.addSeparator()
        self.menuTest.addAction(self.actionExecuteTest)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionManual)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConfiguration.menuAction())
        self.menubar.addAction(self.menuTest.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("gui_window", "&File"))
        self.menuConfiguration.setTitle(_translate("gui_window", "&Configuration"))
        self.menuTest.setTitle(_translate("gui_window", "&Test"))
        self.menuHelp.setTitle(_translate("gui_window", "&Help"))
        self.actionReset.setText(_translate("gui_window", "&Reset"))
        self.actionExit.setText(_translate("gui_window", "&Exit"))
        self.actionChangeProfilesDirectory.setText(_translate("gui_window", "&Profile Directory"))
        self.actionSelectPlaybook.setText(_translate("gui_window", "&Select Playbook"))
        self.actionSelectDeviceUnderTest.setText(_translate("gui_window", "Select &DUT"))
        self.actionClearDUTSelections.setText(_translate("TestbedTesterMainWindow", "Clear DUT Selections"))
        self.actionExecuteTest.setText(_translate("gui_window", "&Execute"))
        self.actionDocumentation.setText(_translate("TestbedTesterMainWindow", "User Manual"))
        self.actionManual.setText(_translate("gui_window", "&Manual"))
        self.actionAbout.setText(_translate("gui_window", "&About"))
        return()
    """"""
    def get_actionExecute(self):
        return(self.actionExecuteTest)
"""*********************************************************************************************
End of File
********************************************************************************************"""
