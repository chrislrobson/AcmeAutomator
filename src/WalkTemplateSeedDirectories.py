#####################################################################################################################
# Python Qt5 Testbed Tester Template and Seed Directory Walk
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
class WalkTemplateAndSeedDirectories:
  " Walk Template and Seed Directories"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None):
    self.name = " Walk Template and Seed Directories"
    self.parent = parent
  #-----------------------------------------------------------------------------------------------------------------
  def walk_template_directory( self, directory_path = None ):
    #---------------------------------------------------------------------------------------------------------------
    self.start_path = "./.template_files"
    try:
      self.parent.template_ListWidget.clear()
      for self.path, self.dirs, self.files in os.walk( self.start_path ):
        for self.filename in self.files:
          self.parent.template_ListWidget.addItem( self.start_path + "/" + self.filename )
          self.parent.template_ListWidget.sortItems( QtCore.Qt.AscendingOrder )
    except Exception as error:
      print( "Template directory listing failed - {}.".format( error.args[0] ) )
    return()
  #-----------------------------------------------------------------------------------------------------------------
  def walk_seed_directory(self, directory_path=None):
    #---------------------------------------------------------------------------------------------------------------
    self.start_path = "./.seed_files"
    try:
      self.parent.seed_ListWidget.clear()
      for self.path, self.dirs, self.files in os.walk( self.start_path ):
        for self.filename in self.files:
          self.parent.seed_ListWidget.addItem( self.start_path + "/" + self.filename )
          self.parent.seed_ListWidget.sortItems( QtCore.Qt.AscendingOrder )
    except Exception as error:
      print( "Seed directory listing failed - {}.".format( error.args[0] ) )
    return ()
####################################################################################################################