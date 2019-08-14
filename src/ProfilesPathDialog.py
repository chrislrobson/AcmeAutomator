"""***********************************************************************************************************
MODULE:   Profiles Path Dialog
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides seed file path dialog processing such as finding the path to a seed file
************************************************************************************************************"""
import os
import sys
from Globals import Globals
"""
CLASS: ProfilesPathDIalog
DESCRIPTION: Seed file path dialog processing
INPUT: seed files and paths
OUTPUT: Lists containg seed files to select
"""
class ProfilesPathDialog:
  "Profiles Path Dialog"
  """"""
  def __init__( self ):
    self.name = self.__class__.__name__
  """"""
  def profiles_dialog( self, directory_str ):
    try:
      if directory_str.startswith( "~" ):
        directory_str = os.path.expanduser('~') + directory_str.split( "~" )[1]
      elif directory_str.find(Globals.relativepath) == -1:
        directory_str = Globals.relativepath + directory_str
    except Exception as error:
      raise Exception( "Massive system error, profiles directory NOT defined {}".format(error) )
    try:
      with open( directory_str, 'r' ) as ppdFD:
        for path in ppdFD:
          if path.startswith("#"):
            pass
          elif path.startswith("\n"):
            pass
          elif path.startswith("~"):
            path = os.path.expanduser('~') + path.split("~")[1]
          elif Globals.relativepath:
            path = Globals.relativepath + path
          Globals.profiles_directory = path.split( "\n" )[0]
          return()
    except Exception as error:
      raise Exception ("Massive system error, profiles directory NOT defined: {} - {}".format( directory_str, error ) )
  """"""
  def diagram_dialog( self, diagram_str ):
    try:
      if diagram_str.startswith( "~" ):
        diagram_str = os.path.expanduser('~') + diagram_str.split( "~" )[1]
      else:
        diagram_str = Globals.relativepath + diagram_str
    except Exception as error:
      print( "Massive system error, profiles directory NOT defined {}".format(error) )
      sys.exit()
    try:
      with open( diagram_str, 'r') as ppdFD:
        for path in ppdFD:
          if path.startswith("#"):
            pass
          elif path.startswith("\n"):
            pass
          elif path.startswith("~"):
            path = os.path.expanduser('~') + path.split("~")[1]
          elif Globals.relativepath:
            path = Globals.relativepath + path
          Globals.diagram = path.split( "\n" )[0]
    except Exception as error:
      print( "Massive system error, profiles "
             "directory NOT defined: {} - {}".format( os.path.expanduser('~') + diagram_str, error) )
      sys.exit()
  """"""
  def set_profiles_directory( self, new_profiles_directory ):
    Globals.profiles_directory = new_profiles_directory
    return( Globals.profiles_directory )
  """"""
  def get_profiles_directory( self ):
    return ( Globals.profiles_directory )
  """"""
  def get_diagram(self):
    return( Globals.diagram )
  """"""
  def set_templates_directory( self, new_templates_directory ):
    Globals.templates_directory = new_templates_directory
    return ( Globals.templates_directory )
  """"""
  def get_templates_directory( self ):
    return ( Globals.templates_directory )
  """"""
  def get_template_seed_directory( self ):
    return ( Globals.template_seed_directory )
  """"""
  def templates_dialog( self, templates_str ):
    try:
      if templates_str.startswith("~"):
        templates_str = os.path.expanduser('~') + templates_str.split("~")[1]
      else:
        templates_str = Globals.relativepath + templates_str
    except Exception as error:
      print( "Massive system error, template directory NOT defined {}".format(error) )
      sys.exit()
    try:
      with open(templates_str, 'r') as ppdFD:
        for path in ppdFD:
          if path.startswith("#"):
            pass
          elif path.startswith("\n"):
            pass
          elif path.startswith("~"):
            path = os.path.expanduser('~') + path.split("~")[1]
          elif Globals.relativepath:
            path = Globals.relativepath + path
          Globals.templates_directory = path.split("\n")[0]
    except Exception as error:
      print("Massive system error, templates "
            "directory NOT defined: {} - {}".format(os.path.expanduser('~') + templates_str, error))
      sys.exit()
  """"""
  """"""
  def template_seed_dialog( self, template_seed_str ):
    try:
      if template_seed_str.startswith("~"):
        template_seed_str = os.path.expanduser('~') + template_seed_str.split("~")[1]
      else:
        template_seed_str = Globals.relativepath + template_seed_str
    except Exception as error:
      print("Massive system error, template seed directory NOT defined {}".format(error) )
      sys.exit()
    try:
      with open( template_seed_str, 'r' ) as ppdFD:
        for path in ppdFD:
          if path.startswith("#"):
            pass
          elif path.startswith("\n"):
            pass
          elif path.startswith("~"):
            path = os.path.expanduser('~') + path.split("~")[1]
          elif Globals.relativepath:
            path = Globals.relativepath + path
          Globals.template_seed_directory = path.split("\n")[0]
    except Exception as error:
      print("Massive system error, template seed "
            "directory NOT defined: {} - {}".format(os.path.expanduser('~') + template_seed_str, error))
      sys.exit()
"""*********************************************************************************************************
End of ProfilesPathDIalog
*********************************************************************************************************"""
