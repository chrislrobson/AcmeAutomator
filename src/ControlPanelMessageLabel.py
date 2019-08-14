"""**************************************************************************************************
FILE: ControlPanelMessageLabel
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
class ControlPanelMessageLabel:
    "Control Panel Message Label"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def create(self, widget=None, layout=None, gridLayout=None):
        self.controlPanelMessageWidget = widget
        self.controlPanelMessageLabel = QtWidgets.QLabel(self.controlPanelMessageWidget)
        self.horizontalLayout = layout
        self.gridLayoutMain = gridLayout
        self.font = QtGui.QFont()
        self.font.setFamily("sans-serif")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setItalic(False)
        self.font.setWeight(75)
        self.controlPanelMessageLabel.setFont(self.font)
        self.controlPanelMessageLabel.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.controlPanelMessageLabel.setStyleSheet(StyleSheet(self.parent).get(stylesheet="ControlPanelMessageLabel.qss"))
        self.controlPanelMessageLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controlPanelMessageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.controlPanelMessageLabel.setWordWrap(True)
        self.controlPanelMessageLabel.setObjectName("controlPanelMessageLabel")
        self.horizontalLayout.addWidget(self.controlPanelMessageLabel)
        self.gridLayoutMain.addWidget(self.controlPanelMessageWidget, 0, 1, 1, 1)
        return(self.controlPanelMessageLabel)
"""*********************************************************************************************
End of File
********************************************************************************************"""
