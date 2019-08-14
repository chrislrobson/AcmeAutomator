#################################################################################################
# BuildMasterFilesList"
#################################################################################################
import os
import sys
#------------------------------------------------------------------------------------------------
# Home grown methods
#------------------------------------------------------------------------------------------------
from Globals import Globals
#------------------------------------------------------------------------------------------------
class BuildMasterFileList( ):
  "Build Master File List"
  #-----------------------------------------------------------------------------------------------
  def __init__( self ):
    self.name = "Build Master File List"
  #-----------------------------------------------------------------------------------------------
  def build_master_file_list( self, master_files_path_directory ):
    #----------------------------------------------------------------------------------------------------------
    start_path = master_files_path_directory.get_template_directory()
    Globals.templates_file_list_dict.clear()
    try:
      for path,dirs,files in os.walk( start_path ):
        for filename in files:
          Globals.templates_file_list.append( filename )
    except:
      print( "BuildTemplatesList: System failure, directory walk failed, program terminated." )
      sys.exit()
    return()
################################################################################################################