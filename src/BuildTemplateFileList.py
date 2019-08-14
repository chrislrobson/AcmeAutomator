####################################################################################################################
# Python Qt5 Testbed Tester Templates File List
# MODULE:  TemplatesFileList
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module
####################################################################################################################
import os
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
# Home grown methods
#------------------------------------------------------------------------------------------------
from Globals import Globals
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
class BuildTemplateFileList():
  "Template File List"
  #-----------------------------------------------------------------------------------------------
  def __init__( self ):
    self.name = "Template File List"
  #-----------------------------------------------------------------------------------------------
  def template_file_list( self ):
    #----------------------------------------------------------------------------------------------------------
    try:
      for self.path,self.dirs,self.files in os.walk( Globals.templates_directory ):
        for self.filename in self.files:
          try:
            Globals().templates_list.append( self.filename )
          except:
            pass
    except:
      raise Exception( "BUILDTEMPLATEFILELIST: System failure, directory walk failed." )
    return()
################################################################################################################