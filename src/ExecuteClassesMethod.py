#####################################################################################################################
# Python Qt5 Testbed Tester Execute Classes Method
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  An importlib class method spawner.
#####################################################################################################################
import importlib
from PyQt5 import QtCore, QtWidgets, QtGui
#--------------------------------------------------------------------------------------------------------------------
# Home grown libraries
#--------------------------------------------------------------------------------------------------------------------
from Globals import *
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class ExecuteClassesMethod:
  " Execute Classes Method"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    super( ExecuteClassesMethod, self ).__init__( parent )
    self.name = " Execute Classes Method"
    self.parent = parent
    self.gparent = parent.parent
  #-----------------------------------------------------------------------------------------------------------------
  def execute_classes_method( self, method_to_run ):
    self.method_to_run = method_to_run
    try:
      self.module = importlib.import_module( "ExecuteClassessMethod" )
      self.module_class = getattr( self.module, self.method_to_run )
      self.module_method = self.module_class( self )
      self.results = self.module_method.execute()
    except Exception as error:
      self.message_ptr = Globals.RED_MESSAGE + \
                         error.args[0] + \
                         Globals.SPAN_END_MESSAGE
      self.parent.tplseed_logger_message_signal.emit( self.message_ptr )
      raise
    return()
#####################################################################################################################
