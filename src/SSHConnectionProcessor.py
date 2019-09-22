"""******************************************************************************************
MODULE:  SSHConnectionProcessor
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module providessh connection logic
******************************************************************************************"""
"""
Python libraries
"""
import time
"""
Home grown libraries
"""
from Globals import *
from Exceptions import *
from SSHChannelProcessor import SSHChannel
"""
CLASS: Connect
DESCRIPTION: Establishes SSH connect
INPUT: Connect dictionary containing IP, repeat counter and delay (wait)
OUTPUT: Creates SSH session element in SSH Global connection lists
"""
class Connect:
  "Connect"
  """"""
  def __init__(self, parent):
    self.name = self.__class__.__name__
    self.parent = parent
    self.grandparent = parent.parent
    self.greatgrandparent = parent.parent.parent
    self.ssh_channel = SSHChannel(self.grandparent)
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.devicectl_dict = dictionary
    self.grandparent.ssh_handle = -1
    self.grandparent.scp_handle = -1
    self.loopcount = 1
    self.delay = .1
    try:
      self.ssh_channel_dict = self.devicectl_dict['sshchannel']
      self.ssh_channel_dict['processreply'] = self.devicectl_dict['processreply']
      self.retryctl_dict = self.devicectl_dict['retryconnection']
      self.loopcount = int(self.retryctl_dict['loopcount'])
      self.delay = float(self.retryctl_dict['delay'])
      self.verbose = self.ssh_channel_dict['verbose']
    except Exception as error:
      self.message = "{{{}{}: {}}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.devicectl_dict['loggerwidget'].emit(self.message)
      raise Exception
    try:
      self.ssh_channel.ssh_channel_initilization(self.ssh_channel_dict)
      Globals().ssh_connection_dict.append((self.grandparent.ssh_handle, self.devicectl_dict))
      if self.verbose:
        self.message = "Successfully connected to {}.".format(self.ssh_channel_dict["ip"])
        self.devicectl_dict['loggerwidget'].emit(self.message)
    except SSHSocketError as error:
      if self.verbose:
        self.message  = "{" + Globals.RED_MESSAGE
        self.message += "{}: {} ".format(self.name, error)
        self.message += "Retrying {} more attempts to {}".format(self.devicectl_dict['retryconnection']['loopcount'], self.ssh_channel_dict['ip'])
        self.message += Globals.SPAN_END_MESSAGE + "}"
        self.devicectl_dict['loggerwidget'].emit(self.message)
      for self.connection_attempt in range(int(self.devicectl_dict['retryconnection']['loopcount'])):
        try:
          self.ssh_channel.ssh_channel_initilization(self.ssh_channel_dict)
          Globals().ssh_connection_dict.append((self.grandparent.ssh_handle, self.devicectl_dict))
          if self.verbose:
            self.message = "Retry successfully connected to {}.".format(self.ssh_channel_dict["ip"])
            self.devicectl_dict['loggerwidget'].emit(self.message)
          return()
        except:
          time.sleep(self.delay)
          continue
      self.message = "{{{}{}: Connection failed to {}{}}}".format(Globals.RED_MESSAGE, self.name, self.ssh_channel_dict['ip'], Globals.SPAN_END_MESSAGE)
      self.devicectl_dict['loggerwidget'].emit(self.message)
      raise Exception
    except (CriticalFailure, SSHConnectionError, SSHReadAuthenicationError, Exception) as error:
      if error.args:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.devicectl_dict['loggerwidget'].emit(self.message)
      raise Exception
    return()
"""
CLASS: Disconnect
DESCRIPTION: Terminate SSH connect
INPUT: Disconnect dictionary containing IP of device
OUTPUT: None
"""
class Disconnect:
  "Disconnect"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.grandparent = self.parent.parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    try:
      self.ssh_channel_dict = self.dictionary['sshchannel']
      self.verbose = self.ssh_channel_dict['verbose']
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      return()
    self.ssh_handle = self.grandparent.ssh_handle
    self.message = "Successfully disconnected from {}.".format( self.ssh_channel_dict["ip"] )
    try:
      self.ssh_handle.close()
    except:
      self.message = "Failed to disconnect from {}.".format( self.ssh_channel_dict["ip"] )
    if self.verbose:
      self.dictionary['loggerwidget'].emit(self.message)
    return()
"""***********************************************************************************************************
End of File
***********************************************************************************************************"""
