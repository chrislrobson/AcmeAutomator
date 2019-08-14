"""*****************************************************************************************
FILE: HostCommand
MODULE:   Processor
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module issues host system commands via the Python "POpen" system call.
           Message passing between the GUI and the testing modules is accomplished
           using Qt5 "Signal and Slot" processing system.
#NOTE:
Because this uses the Python "Popen" "loopcnt can be set to "240" and "delay" set
to ".5"
****************************************************************************************"""
"""
Python libraries
"""
import subprocess
from PyQt5 import QtWidgets
import datetime
import socket
"""
Home grown libraries
"""
from Globals import *
from SeedCommandlinePreprocessor import SeedCommandlinePreprocessor
"""
CLASS: HostCommand
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class Hostcommand(QtWidgets.QWidget):
  "Host Command"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    if self.dictionary['verbose']:
      self.message = "{} started at: {}.".format(self.name.title(), datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S"))
      self.dictionary['loggerwidget'].emit(self.message)
    self.results = ""
    if self.dictionary['fileoutput']:
      try:
        self.archivefileFD = open(self.dictionary['archivefilename'], 'w+')
      except Exception as error:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    """"""
    try:
      with open(self.dictionary["relativepath"] + self.dictionary['commandpath'] + self.dictionary['commands'], 'r') as self.cmd_FD:
        try:
          self.cmd_FD.seek(0)
        except Exception as error:
          self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
          self.dictionary['loggerwidget'].emit(self.message)
          raise Exception
        for self.cmd_data in self.cmd_FD:
          if not SeedCommandlinePreprocessor(self).preprocessor(message_signal = self.dictionary['loggerwidget'], data = self.cmd_data):
            continue
          else:
            self.cmd = self.cmd_data
            if self.dictionary['verbose']:
              self.message = "{}: command to be executed is: {}".format(self.name, self.cmd.split("\n")[0])
              self.dictionary['loggerwidget'].emit(self.message)
            try:
              """
              Make sure stdin is piped and communicate pass nothing so call will not hang!
              """
              self.output = subprocess.Popen(self.cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
              try:
                self.outputresults, self.err = self.output.communicate(input = '')
              except Exception as error:
                self.message = "{{{}{} failed {}\n {}{}}}".format(Globals.RED_ONLY_MESSAGE, self.name, self.cmd, error, Globals.RED_ONLY_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                continue
              self.results = str(self.outputresults, "utf-8")
              self.err_str = str(self.err, "utf-8")
              if self.err_str != "":
                self.error = self.err_str.replace(":", " ").replace("\n", "").replace("\"", "")
                self.message = "{{{}{} failed error {}{}}}".format(Globals.RED_MESSAGE, self.name, self.error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise Exception
              """
              Print output here so it displays in a more realtime way and doesn't wait until every
              command has executed
              """
              if self.dictionary['fileoutput']:
                try:
                  self.dictionary['archivefilenameFD'].write("\nDUT({}/{})-> {}".format(socket.gethostbyaddr(self.dictionary['ip'])[0], self.dictionary['ip'], self.cmd_data + "\n"))
                  self.dictionary['archivefilenameFD'].write(self.results)
                except Exception as error:
                  self.message = "{{{}{} {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise Exception
              if self.dictionary['stdout']:
                self.dictionary['reportwidget'].emit(self.results)
            except Exception as error:
              if error.args:
                self.message = "{{{}{} {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
              raise Exception
    except OSError as error:
      if error.args:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    except Exception as error:
      if error.args:
        self.message = "{{{}{} {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    if self.dictionary['fileoutput']:
      self.dictionary['archivefilenameFD'].close()
    return()
"""
End of File
"""
