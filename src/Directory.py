"""**************************************************************************************************
FILE: Directory
MODULE: Directory
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module does all directory manipulation.
**************************************************************************************************"""
"""
Python Libraries
"""
import getpass, pwd, grp
import os, stat
"""
Script Libraries
"""
from Globals import *
"""
CLASS: Directory
DESCRIPTION: Creates, chown and chmod directories.
INPUT: filename and absolute path
OUTPUT: 
"""
class Directory:
  "Directory"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def create(self, directory=None):
    self.directory = directory
    self.username = getpass.getuser()
    self.uid = pwd.getpwnam(self.username).pw_uid
    self.gid = grp.getgrnam(self.username).gr_gid
    if not self.isdirectory(self.directory):
      try:
        os.makedirs(self.directory)
        os.chown(self.directory, self.uid, self.gid)
        os.chmod(self.directory, mode=stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
      except Exception as error:
        self.message = "{{{}{}: {} with {}{}}}".format(Globals.RED_MESSAGE, self.name, error, self.directory, Globals.SPAN_END_MESSAGE)
        self.parent.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    elif os.stat(self.directory).st_uid != pwd.getpwnam(self.username).pw_uid:
      self.message = "{{{}{}: {} is not owner of {}{}}}".format(Globals.RED_MESSAGE, self.name, self.username, self.directory, Globals.SPAN_END_MESSAGE)
      self.parent.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return()
  """"""
  def isdirectory(self, directory=None):
    self.directory = directory
    return(os.path.exists(self.directory))
"""*********************************************************************************************
End of File
********************************************************************************************"""
