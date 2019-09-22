#!/usr/bin/python3
"""*******************************************************************************************************************
Testbed Tester PauseButtoneTimed
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
Yes I will sue your ass off if you decode, destribute or do ANYTHING without my expressed permission.
This includes any government agency, any company or any employee of those orgainizations.
THIS IS NOT FREE SOFTWARE
FUNCTION:  Forces a pause in the running of the TestbedTester until the user press the release button
******************************************************************************************************************"""
import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QApplication, qApp

"""
CLASS: PauseButtonTimed
DESCRIPTION: Executes comands passed from seed file.
INPUT: seed file with commands to execute
OUTPUT: device command output
"""
class PauseButtonTimed(QtWidgets.QWidget):
  "Pause Button Timed"
  def __init__(self):
    QtWidgets.QWidget.__init__(self)
    """
    Only critical settings here is X/Y/Width, 
    Height doesnt do anything, setFixedHeigth required
    """
    self.setGeometry(900, 400, 1100, 100)
    self.setWindowFlag(Qt.FramelessWindowHint)
    layout = QtWidgets.QVBoxLayout(self)
    self.buttonContinue = QtWidgets.QPushButton("",self)
    """
    self.buttonContinue.setFixedWidth(900) not needed but
    setFixedHeight required to get correct window displayed
    """
    self.buttonContinue.setFixedHeight(300)
    self.pausebutton_stylesheet = "color: darkred;" \
                                  "background-color: lightblue; " \
                                  "border-style: groove; " \
                                  "border-width: 4px; " \
                                  "border-radius: 6px; " \
                                  "border-color: green; " \
                                  "font: bold 50pt times new roman; " \
                                  "min-width: 8em; " \
                                  "background-image: url(/usr/local/TestbedTester/" \
                                  "images/ContinueButton.png);" \
                                  "padding: 16px;"
    self.buttonContinue.setStyleSheet(self.pausebutton_stylesheet)
    self.buttonContinue.clicked.connect(self.handleContinue)
    layout.addWidget(self.buttonContinue)
    self.show()
    while(True):
      self.timer = "{}\n{}".format(QDateTime.currentDateTime().toString(), str(time.process_time()))
      self.buttonContinue.setText("{}\n{}".format(self.timer, "Select when finished making changes."))
      qApp.processEvents()
      time.sleep(0.05)
  """"""
  def handleContinue(self):
    sys.exit(0)
"""
MAIN:
DESCRIPTION: Pause button with timeout timer
INPUT: 
OUTPUT:
"""
if __name__ == '__main__':
  app1 = QApplication(sys.argv)
  pausebutton = PauseButtonTimed()
  app1.exec_()
"""
End of File
"""
