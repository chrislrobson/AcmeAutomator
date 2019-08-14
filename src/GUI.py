"""**********************************************************************************************
* FILE: GUI
* PROJECT: AcmeAutomator
* CLASS(s): GUI
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID):
* DATE: 9/17/18 TIME: 09:25:00
* COPYRIGHT (c): 9/17/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION:  Main Gui logic built by QtDesigner and translated by "pyuic5"
*               Then greatly modified by the author to reduce the code per local class
**********************************************************************************************"""
from PyQt5 import QtCore, QtGui, QtWidgets
import os
"""
Home grown libraries
"""
from EnableDisableButtons import EnableDisableButtons
from StyleSheets import StyleSheet
from StartButton import StartButton
from StopButton import StopButton
from CancelButton import CancelButton
from PauseButton import PauseButton
from ControlPanelMessageLabel import ControlPanelMessageLabel
from ConsoleDutTabWidget import ConsoleDutTabWidget
from ButtonControlGroupBox import ButtonControlGroupBox
from DutLabel import DutLabel
from DutListWidget import DutListWidget
from ConsoleListWidget import ConsoleListWidget
from GuiWindow import GuiWindow
from ControlPanelMessageWidget import ControlPanelMessageWidget
from ConsoleDutTab import ConsoleDutTab
from LogsTab import LogsTab
from MenuBar import MenuBar
from StatusBarMessages import StatusBarMessages
"""
CLASS: GuiMainWindow
METHOD: gui_main_window
DESCRIPTION: Main GUI window setup and startup
INPUT: Qt5 QApplication processor window called from the startup Python script GuiStart.py
OUTPUT: Main window GUI 
"""
class GuiMainWindow(object):
    """"""
    def gui_main_window(self, gui_window):
        self.stylesheethome = os.environ.get("STYLESHEETHOME", os.environ.get("HOME", "~/.AcmeAutomator/stylesheets/"))
        self.mainWindowWidget = GuiWindow(gui_window).create()
        self.gridLayoutMain = QtWidgets.QGridLayout(self.mainWindowWidget)
        self.gridLayoutMain.setObjectName("gridLayoutMain")
        self.buttonControlGroupBox, self.buttonControlGrouphorizontalLayout = \
            ButtonControlGroupBox(self).create(widget=QtWidgets.QGroupBox(self.mainWindowWidget),
                                               gridLayout=self.gridLayoutMain)
        self.startButton   = StartButton(self).create(button=QtWidgets.QPushButton(self.buttonControlGroupBox))
        self.stopButton    = StopButton(self).create(button=QtWidgets.QPushButton(self.buttonControlGroupBox))
        self.cancelButton  = CancelButton(self).create(button=QtWidgets.QPushButton(self.buttonControlGroupBox))
        self.pauseButton   = PauseButton(self).create(button=QtWidgets.QPushButton(self.buttonControlGroupBox))
        self.controlPanelMessageWidget, self.horizontalLayout = ControlPanelMessageWidget(self).create(widget=self.mainWindowWidget)
        self.controlPanelMessageLabel = ControlPanelMessageLabel(self).create(widget=self.controlPanelMessageWidget,
                                                                              layout=self.horizontalLayout,
                                                                              gridLayout=self.gridLayoutMain)
        self.consoleDutTabWidget = ConsoleDutTabWidget(self).create(widget=QtWidgets.QTabWidget(self.mainWindowWidget),
                                                                    layout=self.horizontalLayout)
        self.consoleDutTab, self.gridLayout = ConsoleDutTab(self).create()
        self.dutListWidget = DutListWidget(self).create(widget=self.consoleDutTab, layout=self.gridLayout)
        self.DutLabel = DutLabel(self).create(widget=self.consoleDutTab, layout=self.gridLayout)
        self.consoleListWidget, self.consoleLabel = ConsoleListWidget(self).create(widget=self.consoleDutTab,
                                                                                   layout=self.gridLayout,
                                                                                   tabwidget=self.consoleDutTabWidget)
        self.logsTab, self.logsListWidget = LogsTab(self).create()
        gui_window.setCentralWidget(self.mainWindowWidget)
        self.menubar = MenuBar(self, gui_window)
        self.menubar.create()
        self.menubar.set_actions()
        self.statusBarMessages = StatusBarMessages(self, gui_window).create()
        self.retranslate_gui(gui_window)
        self.consoleDutTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(gui_window)
        self.button_control = EnableDisableButtons()
        self.button_control.EnableDisableButtons(self.startButton, False)
        self.button_control.EnableDisableButtons(self.stopButton, False)
        self.button_control.EnableDisableButtons(self.cancelButton, False)
        self.button_control.EnableDisableButtons(self.pauseButton, True, color = "#008000")
        return()
    """
    Method: retranslate_gui
    """
    def retranslate_gui(self, gui_window):
        _translate = QtCore.QCoreApplication.translate
        gui_window.setWindowTitle(_translate("gui_window", "AcmeAutomator Data Collection Analysis Reporting Automation System"))
        self.buttonControlGroupBox.setToolTip(_translate("gui_window",
                                                         "Start: begins a test; Stop: halts a test; Cancel: terminates a test; Pause: halts any system actions until pressed again"))
        self.buttonControlGroupBox.setTitle(_translate("gui_window", "Control Panel"))
        self.startButton.setText(_translate("gui_window", "&Start"))
        self.stopButton.setText(_translate("gui_window", "S&top"))
        self.cancelButton.setText(_translate("gui_window", "&Cancel/Halt"))
        self.pauseButton.setText(_translate("gui_window", "&Pause"))
        self.controlPanelMessageLabel.setText(_translate("gui_window", "Acme Automator"))
        self.DutLabel.setText(_translate("gui_window", "Device Under Test"))
        self.consoleLabel.setText(_translate("gui_window", "Console"))
        self.consoleDutTabWidget.setTabText(self.consoleDutTabWidget.indexOf(self.consoleDutTab), _translate("gui_window", "Console "))
        self.consoleDutTabWidget.setTabText(self.consoleDutTabWidget.indexOf(self.logsTab), _translate("gui_window", "&Logs"))
"""**********************************************************************************************
End of GUI
**********************************************************************************************"""

