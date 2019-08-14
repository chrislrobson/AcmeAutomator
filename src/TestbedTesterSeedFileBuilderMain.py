#!/usr/bin/python
#####################################################################################################################
# Python Qt5 Testbed Automator Seed File Builder
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
#--------------------------------------------------------------------------------------------------------------------
# Home Grown
#--------------------------------------------------------------------------------------------------------------------
import PyQt5TestbedAutomatorSeedFileBuilderGUI
from PyQt5TestbedAutomatorWalkIPAddresses import PyQt5TestbedAutomatorWalkIPAddresses
from PyQt5TestbedAutomatorWalkTemplateSeedDirectories import PyQt5TestbedAutomatorWalkTemplateAndSeedDirectories
from PyQt5TestbedAutomatorBuildMasterSeedFiles import PyQt5TestbedAutomatorBuildMasterSeedFiles
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# Main Window processor
#--------------------------------------------------------------------------------------------------------------------
class PyQt5TestbedAutomatorSeedFileBuilderMain( QtWidgets.QMainWindow,
                                               PyQt5TestbedAutomatorSeedFileBuilderGUI.GUISeedFileBuilderMainWindow):
  "PyQt5 Testbed Automator Seed File Builder Main"
  #------------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    super( PyQt5TestbedAutomatorSeedFileBuilderMain, self ).__init__( parent )
    self.name = "PyQt5 Testbed Automator Seed File Builder Main"
    self.parent = parent
    self.template_file_to_use = ""
    self.seed_file_to_use = ""
    self.ip_addresses = []
    #----------------------------------------------------------------------------------------------------------------
    self.setupGUI( self )
    #----------------------------------------------------------------------------------------------------------------
    self.actionListTemplateFiles.triggered.connect( self.list_template_files )
    self.actionListSeedFiles.triggered.connect( self.list_seed_files )
    self.actionPrintFiles.triggered.connect( self.print_files )
    self.actionBuild_Seed_Files.triggered.connect( self.build_seed_files )
    self.actionBuild_IP_Address_List.triggered.connect( self.build_ip_address_list )
    self.actionAbout.triggered.connect( self.about_the_system )
    self.actionExit.triggered.connect( self.exit_system )
    #---------------------------------------------------------------------------------------------------------------
    self.template_ListWidget.itemClicked.connect( self.select_template_file )
    self.seed_ListWidget.itemClicked.connect( self.select_seed_file )
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def build_ip_address_list( self ):
    PyQt5TestbedAutomatorWalkIPAddresses( self ).walk_ip_addresses()
    self.message_ListWidget.addItem( "IP Addresses List:" )
    cnt = 0
    for self.ip in self.ip_addresses:
      cnt += 1
      self.message_ListWidget.addItem( "{}. {}".format( cnt, self.ip ) )
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def build_seed_files( self ):
    if not self.template_file_to_use or not self.seed_file_to_use or not self.ip_addresses:
      self.message_ListWidget.addItem("Required Template and Seed files have not been selected.")
    else:
      PyQt5TestbedAutomatorBuildMasterSeedFiles( self ).build_master_seed_file()
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def list_template_files( self ):
    PyQt5TestbedAutomatorWalkTemplateAndSeedDirectories( self ).walk_template_directory()
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def select_template_file( self ):
    for self.item in self.template_ListWidget.selectedItems():
      self.template_file_to_use = self.item.text()
      self.message_ListWidget.addItem( "Template file selected: \"{}\".".format( self.template_file_to_use ))
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def list_seed_files( self ):
    PyQt5TestbedAutomatorWalkTemplateAndSeedDirectories( self ).walk_seed_directory()
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def select_seed_file( self ):
    for self.item in self.seed_ListWidget.selectedItems():
      self.seed_file_to_use = self.item.text()
      self.message_ListWidget.addItem( "Seed file selected: \"{}\".".format( self.seed_file_to_use ))
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def print_files( self ):
    self.message_ListWidget.addItem( "Template file selected: \"{}\".".format( self.template_file_to_use ))
    self.message_ListWidget.addItem( "Seed file selected: \"{}\".".format( self.seed_file_to_use ))
    self.message_ListWidget.addItem("IP Addresses List:")
    cnt = 0
    for self.ip in self.ip_addresses:
      cnt += 1
      self.message_ListWidget.addItem( "{}. {}".format( cnt, self.ip ) )
    # FIXME use when mulitple is working - >for self.file_to_use in self.template_file_to_use:
    # FIXME use when mulitple is working - >  self.message_ListWidget.addItem( "Template file selected: \"{}\".".format( self.file_to_use ))
    # FIXME use when mulitple is working - >for self.file_to_use in self.seed_file_to_use:
    # FIXME use when mulitple is working - >  self.message_ListWidget.addItem( "Seed file selected: \"{}\".".format( self.file_to_use ))
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def about_the_system( self ):
    self.message_ListWidget.addItem( "This is the Testbed Automator seed file generator." )
    return()
  #------------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def exit_system( self ):
    print( "Exit system!" )
    sys.exit()
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
  main_application = QtWidgets.QApplication( sys.argv )
  form = PyQt5TestbedAutomatorSeedFileBuilderMain()
  form.show()
  main_application.exec_()
  sys.exit()
#####################################################################################################################

