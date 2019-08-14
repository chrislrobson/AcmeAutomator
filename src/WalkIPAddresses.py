#####################################################################################################################
# Python Qt5 Testbed Tester IP Addresses File Walk
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Main GUI interface and processing for the Seed File Building process.
# Developed from QT-Designer, PCUIC4(5) and then heavely modified.
#####################################################################################################################
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# PyQt5 Libraries
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# Home grown methods
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# FIXME USIING "parent" so not needed from SeedFileBuilderGUI import GUISeedFileBuilderMainWindow
#--------------------------------------------------------------------------------------------------------------------
class WalkIPAddresses:
  " Walk IP Addresses File"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None):
    self.name = " Walk IP Addresses File"
    self.parent = parent
  #-----------------------------------------------------------------------------------------------------------------
  def walk_ip_addresses( self, directory_path = None ):
    #---------------------------------------------------------------------------------------------------------------
    self.ip_addressesFilename = "./.IPAddresses"
    self.parent.ip_addresses = []
    try:
      with open( self.ip_addressesFilename, 'r') as self.FD:
        for self.ip in self.FD:
          if self.ip.startswith("#"):
            pass
          elif self.ip.startswith("\n"):
            pass
          else:
            self.parent.ip_addresses.append( self.ip.split( "\n" )[0] )
    except Exception as error:
      self.parent.message_ListWidget.addItem( "File I/O error: {} - {}".\
                                              format( self.ip_addressesFilename, error.args[1] ) )
    return ()
####################################################################################################################