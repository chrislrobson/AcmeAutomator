####################################################################################################################
# Python Qt5 Testbed Tester Build Master Seed File Processor
# MODULE:  BuildMasterSeedFileProcessor
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module creates Master Seed files from template files.
####################################################################################################################
from PyQt5 import QtCore
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
# Home grown stuff
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
from Globals import Globals
from BuildTemplateFileList import BuildTemplateFileList
from BuildSeedFileList import BuildSeedFileList
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
class BuildSeedFileProcessor( QtCore.QThread ):
  " Build Seed File Processor Processor"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    super( BuildSeedFileProcessor, self ).__init__( parent )
    self.name = "Build Seed File Processor"
    self.parent = parent
  #-----------------------------------------------------------------------------------------------------------------
  def build_seed_file_processor( self ):
    try:
      MakeSeedFile( self ).make_seed_file( Globals.template_file,
                                                                Globals.template_seed_file )
    except:
      message_str = Globals.RED_MESSAGE + \
                    "BUILDSEEDFILEPROCESSOR: Failed to build seed file." + \
                    Globals.SPAN_END_MESSAGE
      self.parent.reportScrollAreaWidgetContents.append( message_str )
    return ()
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
class MakeSeedFile:
  " Make Seed File"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Make Seed File"
    self.gparent = parent.parent
  #-----------------------------------------------------------------------------------------------------------------
  def make_seed_file( self, template_file, seed_file ):
    try:
      self.master_seed_file_FD = open( Globals.profiles_directory + \
        "0.0.0.0-master-profile.prf", "w+" )
      self.template_FD = open( Globals.templates_directory + \
                               Globals.template_file, 'r' )
      with open( Globals.template_seed_directory + \
                 Globals.template_seed_file, 'r' ) as self.seed_FD:
        for self.ip in self.seed_FD:
          self.ip_striped = self.ip.split( "\n" )[0]
          self.template_FD.seek( 0 )
          for self.template_line in self.template_FD:
            self.seed_line = self.template_line.replace( "IPADDRESS", self.ip_striped )
            self.master_seed_file_FD.write( self.seed_line )
          self.master_seed_file_FD.write( "\n" )
    except Exception as e:
      self.message_str = Globals.RED_MESSAGE + \
                         "BUILD: read file error {}".format( e.args ) + \
                         Globals.SPAN_END_MESSAGE
      self.gparent.reportScrollAreaWidgetContents.append( self.message_str )
    self.template_FD.close( )
    self.seed_FD.close( )
    self.master_seed_file_FD.seek( 0 )
    for self.line in self.master_seed_file_FD:
      self.gparent.logScrollAreaWidgetContents.append( self.line )
    self.message_str = "Seed file has been built."
    self.gparent.reportScrollAreaWidgetContents.append( self.message_str )
    self.master_seed_file_FD.close( )
    return ()
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
######################################################################################################################