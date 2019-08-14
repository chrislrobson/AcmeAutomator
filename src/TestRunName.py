####################################################################################################################
# Python Qt5 Testbed Tester Test Run Name
# MODULE:  TestRunName
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module allows the operator to add a string to the report filename to designate a specific run name.
#            The segment runs files a datetime group is appended to the report filename.  The further destingous
#            test runs report filename within a suite of runs, this added name string helps segment the files by
#            sub-test runs.
####################################################################################################################
import random
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
from Exceptions import *
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
class testrunname:
  "Run Name"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Test Run Name"
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, cmd_dict ):
    try:
      Globals.test_run_name = cmd_dict['name']
    except:
      Globals.test_run_name = str( random.random() * 50 )
    return()
  #----------------------------------------------------------------------------------------------------------------
  def set_default( self ):
    Globals.test_run_name = str( random.random( ) * 50 )
    return()
  #----------------------------------------------------------------------------------------------------------------
  def set_name( self, name ):
    Globals.test_run_name = name
    return()
  #----------------------------------------------------------------------------------------------------------------
  def get_name( self ):
    return( Globals.test_run_name )
####################################################################################################################
