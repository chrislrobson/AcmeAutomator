#!/usr/bin/python
"""
MODULE Pause Button Timed
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
"""
"""
LIBRARIES:  Python libraries
"""
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect, QDateTime
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QApplication, qApp
"""
LIBRARIES:  Testbed Tester specific libraries
"""
from Globals import *
"""
CLASS: PauseButton
DESCRIPTION: Pauses program execution until selected
INPUT: 
OUTPUT:
"""
#-------------------------------------------------------------------------------------------------------------------
class PauseButtonTimed( QtWidgets.QWidget ):
  # FIXME not required def __init__( self, time_delay ):
  def __init__( self ):
    QtWidgets.QWidget.__init__( self )
    """
    Only critical settings here is X/Y/Width, 
    Height doesnt do anything, setFixedHeigth required
    """
    self.setGeometry(900, 400, 900, 100 )
    self.setWindowFlag(Qt.FramelessWindowHint)
    layout = QtWidgets.QVBoxLayout( self )
    self.buttonContinue = QtWidgets.QPushButton( "",self )
    """
    self.buttonContinue.setFixedWidth(900) not needed but
    setFixedHeight required to get correct window displayed
    """
    self.buttonContinue.setFixedHeight(300)
    self.buttonContinue.setStyleSheet( Globals.pausebutton_stylesheet )
    self.buttonContinue.clicked.connect( self.handleContinue )
    layout.addWidget( self.buttonContinue )
    self.show()
    while(True):
      self.timer = "{}\n{}".format(QDateTime.currentDateTime().toString(), str(time.clock()))
      self.buttonContinue.setText( self.timer )
      qApp.processEvents()
      time.sleep(0.05)
  """"""
  def handleContinue( self ):
    self.buttonContinue.destroy()
    return
"""
End of File
"""
