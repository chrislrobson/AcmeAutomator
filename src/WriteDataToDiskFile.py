"""
FILE: WriteDiskFile
CLASS:  WriteDiskFile
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module writes data to a disk file.
"""
"""
LIBRARIES:  Python libraries
"""
import datetime
import os, sys, stat
from collections import OrderedDict
import ast
"""
LIBRARIES:  Testbed Tester specific libraries
"""
from Globals import *
from Exceptions import *
from SeedDictionary import SeedCommandDictionaryProcessor
"""
CLASS: WriteDiskFile
DESCRIPTION: Writes data to a disk file
INPUT: Data to save to a disk file
OUTPUT: None
"""
class WriteDataToDiskFile:
  "Write Disk File"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
  """"""
  def write_data_to_disk_file(self, dictionary = None, data = None, filename = None, descriptor = None):
    self.dictionary = dictionary
    self.data = data
    self.filename = filename
    self.fileFD = descriptor
    for self.line in self.data:
      try:
        self.fileFD.write(self.line + "\n")
        # todo-debug
        # todo-debug print( self.line )
        # todo-debug
      except Exception as error:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    return ()
"""
END of FILE
"""