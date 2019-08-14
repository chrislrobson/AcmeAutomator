####################################################################################################################
# Python Qt5 Testbed Tester Seed File List
# MODULE:  SeedFileList
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module provides
####################################################################################################################
import os
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
# Home grown methods
#------------------------------------------------------------------------------------------------
from Globals import Globals
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
class BuildSeedFileList():
  "Seed File List"
  #-----------------------------------------------------------------------------------------------
  def __init__( self ):
    self.name = "Seed File List"
  #-----------------------------------------------------------------------------------------------
  def seed_file_list( self ):
    #----------------------------------------------------------------------------------------------------------
    try:
      for self.path,self.dirs,self.files in os.walk( Globals.template_seed_directory ):
        for self.filename in self.files:
          try:
            Globals().template_seed_list.append( self.filename )
          except:
            pass
    except:
      raise Exception( "BUILDSEEDFILELIST: System failure, directory walk failed." )
    return()
################################################################################################################