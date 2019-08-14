"""
Testbed Tester Seed Command Dictionary Processor
MODULE:  SeedCommandDictionaryProcessor
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module decodes the command line dictionary into a running dictionary.
By decoding into a runtime dictionary filenames can be constructed and openned prior to processing.
Another side benefit is preforming all "try/exception" processing in one location ahead of time.
"""
"""
Python libraries
"""
"""
Home libraries
"""
from Globals import *
"""
CLASS: SeedCommandDictionaryProcessor
DESCRIPTION: Executes comands passed from seed file.
INPUT: Seed file extracted line converted to dictionary
OUTPUT: Seed dictionary converted to runtime dictionary
"""
class SeedCommandDictionaryProcessor():
  "Seed Command Dictionary Processor"
  """"""
  def __init__(self, parent = None):
    super(SeedCommandDictionaryProcessor, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent
    self.ip = parent.ip
    self.filename_time_extension = parent.filename_time_extension
    self.logger_message_signal = self.parent.logger_message_signal
    self.process_reply = parent.process_reply
  """"""
  def seed_command_dictionary_processor(self, cmdline_dict):
    self.cmdline_dict = GetDictionary().get_dictionary(cmdline_dict)
    if not (self.cmdline_dict):
      return(cmdline_dict)
    try:
      self.cmdline_dict['commands'] = self.cmdline_dict['commands']
    except Exception as error:
      self.message = "{{{}{}: no {} file provided{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.logger_message_signal.emit(self.message)
      raise Exception
    try:
      self.cmdline_dict['prompt'] = self.cmdline_dict['prompt']
      self.process_reply.set_prompt_string(self.cmdline_dict['prompt'], "Continue")
    except:
      pass  # assume done by connect command
    try:
      self.cmdline_dict['delay'] = float(self.cmdline_dict['delay'])
    except:
      self.cmdline_dict['delay'] = .1
    try:
      self.cmdline_dict['loopcnt'] = int(float(self.cmdline_dict['loopcnt']))
    except:
      self.cmdline_dict['loopcnt'] = 240
    try:
      self.cmdline_dict['commandpath'] = self.cmdline_dict['commandpath']
    except:
      self.cmdline_dict['commandpath'] = "./"
    try:
      self.cmdline_dict['savepath'] = self.cmdline_dict['savepath']
    except:
      self.cmdline_dict['savepath'] = "./"
    try:
      self.cmdline_dict['issave'] = self.cmdline_dict['issave']
    except:
      self.cmdline_dict['issave'] = True
    try:
      self.cmdline_dict['stdout'] = self.cmdline_dict['stdout']
    except:
      self.cmdline_dict['stdout'] = False
    try:
      self.cmdline_dict['verbose'] = self.cmdline_dict['verbose']
    except:
      self.cmdline_dict['verbose'] = False
    try:
      self.cmdline_dict['fileoutput'] = self.cmdline_dict['fileoutput']
    except:
      self.cmdline_dict['fileoutput'] = False
    try:
      if self.cmdline_dict['user'] == "NONE":
        self.cmdline_dict['user'] = Globals().user_to_use
      else:
        self.cmdline_dict['user'] = self.cmdline_dict['user']
    except:
      self.cmdline_dict['user'] = Globals().user_to_use
    try:
      if self.cmdline_dict['pwd'] == "NONE":
        self.cmdline_dict['pwd'] = Globals().password_to_use
      else:
        self.cmdline_dict['pwd'] = self.cmdline_dict['pwd']
    except:
      self.cmdline_dict['pwd'] = Globals().password_to_use
    if self.cmdline_dict['fileoutput']:
      try:
        self.cmdline_dict['archivefilename'] = self.cmdline_dict['savepath'] + self.cmdline_dict['exactfilename']
      except:
        try:
          self.cmdline_dict['archivefilename'] = self.cmdline_dict['savepath'] + self.cmdline_dict['filename'] + self.filename_time_extension
        except:
          self.cmdline_dict['archivefilename'] = self.cmdline_dict['savepath'] + self.ip + self.filename_time_extension
      try:
        self.cmdline_dict['archivefiledescriptor'] = open( self.cmdline_dict['archivefilename'] , "w+")
      except (OSError, Exception) as error:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.logger_message_signal.emit(self.message)
        raise Exception
    else:
      self.cmdline_dict['archivefilename'] = ""
      self.cmdline_dict['archivefiledescriptor'] = None
    try:
      self.cmdline_dict['interfaces'] = self.cmdline_dict['interfaces']
    except:
      self.cmdline_dict['interfaces'] = ""
    try:
      self.cmdline_dict['device'] = self.cmdline_dict['device']
    except:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.logger_message_signal.emit(self.message)
      raise Exception
    try:
      self.cmdline_dict['initializedata'] = self.cmdline_dict['initializedata']
    except:
      self.cmdline_dict['initializedata'] = False
    try:
      self.cmdline_dict['detailedresults'] = self.cmdline_dict['detailedresults']
    except:
      self.cmdline_dict['detailedresults'] = 'Yes'
    """
    Return the original dictionary so the "RunCommand" class can morph the command to run
    which is extracted from the first key and used as the command classes keyword name. 
    """
    return(cmdline_dict)
"""
End of File
"""
